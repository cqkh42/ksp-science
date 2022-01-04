import numpy as np
import pandas as pd


def test_experiment_global_table(experiment_1):
    expected = pd.DataFrame([
        ['FlyingHigh', 'experiment_1', True, 1, 'global', np.nan],
        ['InSpaceLow', 'experiment_1', True, 1, 'global', np.nan],
    ],
    columns=['situation', 'experiment', 'requires_atmosphere', 'max_value', 'scope', 'body']).set_index(['experiment', 'situation'])
    output = experiment_1.global_table
    pd.testing.assert_frame_equal(output, expected)


def test_roc_experiment_global_table(roc_experiment):
    expected = pd.DataFrame([
        ['SrfLanded', 'ROCExperiment', False, 30, 'global', 'Kerbin'],
    ],
        columns=['situation', 'experiment', 'requires_atmosphere', 'max_value',
                 'scope', 'body']).set_index(['experiment', 'situation'])
    output = roc_experiment.global_table
    pd.testing.assert_frame_equal(output, expected)


def test_experiment_biome_table(experiment_1):
    expected = pd.DataFrame([
        ['SrfLanded', 'experiment_1', True, 1, 'biome', np.nan],
    ],
    columns=['situation', 'experiment', 'requires_atmosphere', 'max_value', 'scope', 'body']).set_index(['experiment', 'situation'])
    output = experiment_1.biome_table
    pd.testing.assert_frame_equal(output, expected)


def test_experiment_table(experiment_1):
    expected = pd.DataFrame([
        ['SrfLanded', 'experiment_1', True, 1, 'biome', np.nan],
        ['FlyingHigh', 'experiment_1', True, 1, 'global', np.nan],
        ['InSpaceLow', 'experiment_1', True, 1, 'global', np.nan],
    ],
        columns=['situation', 'experiment', 'requires_atmosphere', 'max_value',
                 'scope', 'body']).set_index(['experiment', 'situation']).sort_index()
    output = experiment_1.table.sort_index()
    pd.testing.assert_frame_equal(output, expected)
