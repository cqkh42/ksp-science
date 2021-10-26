from dataclasses import dataclass, field
import importlib.resources
import json

import pandas as pd


@dataclass(frozen=True)
class Experiment:
    name: str
    max_value: float
    requires_atmosphere: bool
    global_situations: list = field(default_factory=list)
    biome_situations: list = field(default_factory=list)

    def global_table(self):
        index = pd.MultiIndex.from_product(
            [[self.name], self.global_situations],
            names=['experiment', 'situation']
        )
        return pd.DataFrame(
            {
                "requires_atmosphere": self.requires_atmosphere,
                "max_value": self.max_value,
                "scope": 'global',
            },
            index=index
        )

    def biome_table(self):
        index = pd.MultiIndex.from_product(
            [[self.name], self.biome_situations],
            names=['experiment', 'situation']
        )
        return pd.DataFrame(
            {
                "requires_atmosphere": self.requires_atmosphere,
                "max_value": self.max_value,
                "scope": 'biome',
            },
            index=index
        )


def load_experiments(path='default'):
    if path == 'default':
        path = importlib.resources.open_text("science", "experiments.json")
    with path as file:
        bodies_list = json.load(file)
    return [Experiment(**attrs) for attrs in bodies_list]
