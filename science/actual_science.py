import warnings
from pathlib import Path
import re

import pandas as pd
import parse

from science import bodies


_PARSE_FORMAT = (
    r'Science {{ id = {experiment}@{situation_string} title = {} dsc = {} '
    r'scv = {} sbv = {} sci = {current_science:g} asc = {} '
    r'cap = {max_science:g} }}'
)

VALID_SITUATIONS = (
    'SrfLanded', 'SrfSplashed', 'FlyingLow', 'FlyingHigh', 'InSpaceLow',
    'InSpaceHigh', 'FlewBy', 'Flew', 'SubOrbited', 'Orbited', 'Surfaced'
)

SITUATION_REGEX = re.compile(
    r'(?P<body>[A-Z][a-z]+?)(?P<situation>'
    + '|'.join(VALID_SITUATIONS) + ')'
    + r'(?P<biome>.*)'
)


def parse_save_text(text):
    content = re.sub(r'\s+', ' ', text)
    science = [
        experiment.named for experiment in
        parse.findall(_PARSE_FORMAT, content)
    ]
    df = pd.DataFrame(science)
    df[['body', 'situation', 'biome']] = parse_situation(df.situation_string)
    df = df.drop(columns=['situation_string'])
    df = df.set_index(['body', 'biome', 'situation', 'experiment'])
    return df


def parse_situation(situation: pd.Series):
    # TODO fix

    KSC = [body for body in bodies.load_bodies() if body.name == 'KSC'][0]
    df = situation.str.extract(SITUATION_REGEX)
    # Fix KSC vs Kerbin
    df.loc[
        (df.body == 'Kerbin') & (df.biome.isin(KSC.biomes)),
        'body'
    ] = 'KSC'

    # address global biomes
    df.loc[df.biome == '', 'biome'] = 'global'

    bad_indices = df.loc[~df.situation.isin(VALID_SITUATIONS)].index
    if not bad_indices.empty:
        bad_strings = situation.loc[bad_indices].unique()
        warnings.warn(f'Unexpected situations detected - {bad_strings}')
    return df


def load(save='career'):
    file = (
        Path(r'/') / 'Applications' / 'KSP_osx' / 'saves' /
        save / 'persistent.sfs'
    )
    content = file.read_text()
    df = parse_save_text(content)

    assert len(df) == len(re.findall(r'Science.\s+?{.\s+?id', content, flags=re.DOTALL|re.MULTILINE))
    return df
