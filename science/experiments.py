from dataclasses import dataclass, field
import importlib.resources
import json

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Experiment:
    name: str
    max_value: float
    requires_atmosphere: bool
    global_situations: list = field(default_factory=list)
    biome_situations: list = field(default_factory=list)
    body: np.nan = np.nan

    def _create_table(self, situations, scope):
        index = pd.MultiIndex.from_product(
            [[self.name], situations],
            names=['experiment', 'situation']
        )
        return pd.DataFrame(
            {
                "requires_atmosphere": self.requires_atmosphere,
                "max_value": self.max_value,
                "scope": scope,
                "body": self.body
            },
            index=index
        )

    @property
    def global_table(self):
        return self._create_table(self.global_situations, 'global')

    @property
    def biome_table(self):
        return self._create_table(self.biome_situations, 'biome')

    @property
    def table(self):
        return pd.concat([self.global_table, self.biome_table])


def load_experiments(path='default'):
    if path == 'default':
        path = importlib.resources.open_text("science", "experiments.json")
    with path as file:
        bodies_list = json.load(file)
    return [Experiment(**attrs) for attrs in bodies_list]
