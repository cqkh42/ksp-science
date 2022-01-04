# TODO asteroid
# TODO comet
# TODO Where can you be 'splasheddown'
# TODO the sun - special cases

from dataclasses import dataclass
import importlib.resources
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
        index = pd.MultiIndex.from_product(
            [[self.name], self.biomes, self.science_multipliers],
            names=['body', 'biome', 'situation']
        )
        df = pd.DataFrame(index=index)
        df['multiplier'] = df.index.map(lambda x: self.science_multipliers[x[2]])
        df['has_atmosphere'] = self.has_atmosphere
        return df


def load_bodies(path='default'):
    if path == 'default':
        path = importlib.resources.open_text("science", "bodies.json")
        with path as file:
            bodies_list = json.load(file)
    return [Body(**attrs) for attrs in bodies_list]
