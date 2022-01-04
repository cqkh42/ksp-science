# TODO asteroid
# TODO comet
# TODO transmission
# TODO deployable science
# TODO Where can you be 'splasheddown'
# TODO flew


import pandas as pd

from science import bodies
from science import experiments


def load_recovery(bodies):
    situation_multipliers = {
        "FlewBy": 7.2,
        'Orbited': 9.6,
        "SubOrbited": 12,
        "Flew": 14.4,
        "Surfaced": 18
    }
    a = []
    for body in bodies:
        if body.name == 'Kerbin':
            m = {
                "FlewBy": 0,
                "Orbited": 12,
                "SubOrbited": 9.6,
                "Flew": 6,
                "Landed": 0
            }
            for situation, multiplier in m.items():
                z = [body.name, 'recovery', situation,
                     body.recovery_multiplier * multiplier, 'global']
                a.append(z)
        else:
            for situation, multiplier in situation_multipliers.items():
                z = [body.name, 'recovery', situation, body.recovery_multiplier * multiplier, 'global']
                a.append(z)
    return pd.DataFrame(a, columns=['body', 'experiment', 'situation', 'max_science', 'biome']
                        ).set_index(['body', 'biome', 'situation', 'experiment'])


def load_situations(bodies):
    return pd.concat(body.situations() for body in bodies)


def load_experiments(bodies, experiments):
    # TODO test with ROC
    experiments = pd.concat(
        [experiment.table for experiment in experiments]).reset_index()
    situations = load_situations(bodies).reset_index()
    df = experiments.merge(situations, how='outer', on=['situation'],
                           suffixes=['_experiment', '_situation'])
    df = df.loc[
        df.body_experiment.fillna(df.body_situation) == df.body_situation]

    df = df.loc[~(df.requires_atmosphere) | (
            df.requires_atmosphere & df.has_atmosphere)]
    df = df.rename(columns={'body_situation': 'body'})

    df.loc[df.scope == 'global', 'biome'] = 'global'
    df = df.loc[(df.body != 'KSC') | (df.biome != 'global')]
    df['max_science'] = df.multiplier * df.max_value
    df = df.loc[:, ['body', 'biome', 'situation', 'experiment',
                    'max_science']].drop_duplicates()
    df = df.set_index(['body', 'biome', 'situation', 'experiment'])
    return df


def load():
    b = bodies.load_bodies()
    e = experiments.load_experiments()
    EE = load_experiments(b, e)
    recovery = load_recovery(b)
    return pd.concat([EE, recovery])
    # return df
