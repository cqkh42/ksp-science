import pandas as pd

from science.possible_science import load_situations, load_experiments, load_recovery
from science import bodies


def test_load_situations(body_1, body_2):
    bodies = [body_1, body_2]
    expected = pd.DataFrame([
            ['body_1', 'biome_1', 'SrfLanded', 0.5, True],
            ['body_1', 'biome_2', 'SrfLanded', 0.5, True],
            ['body_2', 'biome_a', 'InSpaceLow', 1, False],
            ['body_2', 'biome_a', 'InSpaceHigh', 2, False],
            ['body_2', 'biome_b', 'InSpaceLow', 1, False],
            ['body_2', 'biome_b', 'InSpaceHigh', 2, False]
        ],
        columns=['body', 'biome', 'situation', 'multiplier', 'has_atmosphere']
    ).set_index(['body', 'biome', 'situation'])
    output = load_situations(bodies)
    pd.testing.assert_frame_equal(output, expected)


def test_load_experiments(experiment_1, experiment_2, body_1, body_2):
    experiments = [experiment_1, experiment_2]
    bodies = [body_1, body_2]
    expected = pd.DataFrame(
        [
            ['body_2', 'biome_a', 'InSpaceHigh', 'experiment_2', 4.],
            ['body_2', 'biome_b', 'InSpaceHigh', 'experiment_2', 4.],
            ['body_2', 'biome_a', 'InSpaceLow', 'experiment_2', 2.],
            ['body_2', 'biome_b', 'InSpaceLow', 'experiment_2', 2.],
            ['body_1', 'global', 'SrfLanded', 'experiment_2', 1.],
            ['body_1', 'biome_1', 'SrfLanded', 'experiment_1', 0.5],
            ['body_1', 'biome_2', 'SrfLanded', 'experiment_1', 0.5],
        ],
        columns=['body', 'biome', 'situation', 'experiment', 'max_science']
    ).set_index(['body', 'biome', 'situation', 'experiment']).sort_index()
    output = load_experiments(bodies, experiments).sort_index()
    pd.testing.assert_frame_equal(output, expected)


def test_load_recovery(body_1, body_2, kerbin):
    # TODO fix
    bodies = [body_1, body_2, kerbin]
    expected = pd.DataFrame([
        ['body_1', 'recovery', 'FlewBy', 1*7.2, 'global'],
        ['body_1', 'recovery', 'Orbited', 1*9.6, 'global'],
        ['body_1', 'recovery', 'SubOrbited', 1*12, 'global'],
        ['body_1', 'recovery', 'Flew', 1*14.4, 'global'],
        ['body_1', 'recovery', 'Landed', 1*18, 'global'],
        ['body_2', 'recovery', 'FlewBy', 7*7.2, 'global'],
        ['body_2', 'recovery', 'Orbited', 7*9.6, 'global'],
        ['body_2', 'recovery', 'SubOrbited', 7*12, 'global'],
        ['body_2', 'recovery', 'Flew', 7*14.4, 'global'],
        ['body_2', 'recovery', 'Landed', 7*18, 'global'],
        ['Kerbin', 'recovery', 'FlewBy', 0, 'global'],
        ['Kerbin', 'recovery', 'Orbited', 12, 'global'],
        ['Kerbin', 'recovery', 'SubOrbited', 9.6, 'global'],
        ['Kerbin', 'recovery', 'Flew', 6, 'global'],
        ['Kerbin', 'recovery', 'Landed', 0, 'global']
    ], columns=['body', 'experiment', 'situation', 'max_science', 'biome']).set_index(['body', 'biome','situation', 'experiment'])
    output = load_recovery(bodies)
    pd.testing.assert_frame_equal(output, expected)