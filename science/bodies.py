# TODO asteroid
# TODO comet
# TODO Where can you be 'splasheddown'
# TODO the sun

from dataclasses import dataclass
import importlib.resources
import itertools
import json

import pandas as pd


@dataclass(frozen=True)
class Body:
    name: str
    has_atmosphere: bool
    biomes: list
    science_multipliers: dict
    recovery_multiplier: float

    def situations(self):
        products = itertools.product(self.biomes, self.science_multipliers)
        df = pd.DataFrame(products, columns=['biome', 'situation'])
        df['multiplier'] = df.situation.map(self.science_multipliers)
        df[['body', 'has_atmosphere']] = [self.name, self.has_atmosphere]
        df = df.set_index(['body', 'biome', 'situation'])
        return df


def load_bodies(path='default'):
    if path == 'default':
        with importlib.resources.open_text("science", "bodies.json") as file:
            bodies_list = json.load(file)
    return [Body(**attrs) for attrs in bodies_list]
