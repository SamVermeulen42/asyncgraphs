# AsyncGraphs

<p>
<a href="https://github.com/SamVermeulen42/asyncgraphs/actions?query=workflow%3ATests+event%3Apush+branch%3Amain" target="_blank" >
  <img src="https://github.com/SamVermeulen42/asyncgraphs/workflows/Tests/badge.svg?event=push&branch=main" alt="Test"/>
</a>
<a href="https://codecov.io/gh/SamVermeulen42/asyncgraphs" target="_blank" >
  <img src="https://codecov.io/gh/SamVermeulen42/asyncgraphs/branch/main/graph/badge.svg?token=17MW83L23M" alt="Coverage"/> 
</a>
<a href="https://pypi.org/project/asyncgraphs" target="_blank">
  <img src="https://img.shields.io/pypi/v/asyncgraphs" alt="Package version"/>
</a>
<a href="https://pypi.org/project/asyncgraphs" target="_blank">
  <img src="https://img.shields.io/pypi/pyversions/asyncgraphs.svg" alt="Supported Python versions">
</a>
</p>

---

AsyncGraphs is a tiny ETL framework that leverages asyncio to make the execution concurrent whilst blocked on I/O.

**Source:** <a href=https://github.com/SamVermeulen42/asyncgraphs target="_blank">https://github.com/SamVermeulen42/asyncgraphs</a>

**Documentation:** <a href=https://samvermeulen42.github.io/asyncgraphs/ target="_blank">https://samvermeulen42.github.io/asyncgraphs/</a>

---

## Features

- Typed
- Simple concurrency based on asyncio
- Easy construction of ETL graphs


## Installation

```commandline
pip install asyncgraphs
```

## Example

The following example prints random Pokémon and the games they appear in.

It does this every 10 seconds and uses [PokéApi](https://pokeapi.co/).

```python
import aiohttp
from asyncgraphs import Graph, run
import asyncio
from functools import partial
from random import randint
from typing import Dict, Any


async def random_pokemon_id():
    while True:
        yield randint(1, 151)
        await asyncio.sleep(10)

async def get_pokemon_info(session: aiohttp.ClientSession, pokemon_id: int) -> Dict[str, Any]:
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    async with session.get(pokemon_url) as response:
        yield await response.json()
                
def format_pokemon(pokemon_info: Dict[str, Any]) -> str:
    name = pokemon_info["name"]
    versions = (game['version']['name'] for game in pokemon_info['game_indices'])
    return f"{name}: {', '.join(versions)}"

async def main():
    async with aiohttp.ClientSession() as session:
        g = Graph()
        g | random_pokemon_id() | partial(get_pokemon_info, session) | format_pokemon | print
        await run(g)

asyncio.run(main())
```

## Dev notes

This library is not yet stable. I'm still figuring out my preferred way of handling things.

### local setup

```shell
pyenv install 3.12
pyenv local 3.12
pyenv virtualenv asyncgraphs
pyenv activate asyncgraphs
pip install .[dev,docs]
```
