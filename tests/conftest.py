import pytest

from science.bodies import Body
from science import bodies
from science.experiments import Experiment


@pytest.fixture
def body_1():
    return Body(
        'body_1',
        True,
        ['biome_1', 'biome_2'],
        {'SrfLanded': 0.5},
        1
    )


@pytest.fixture
def body_2():
    return Body(
        'body_2',
        False,
        ['biome_a', 'biome_b'],
        {'InSpaceLow': 1, "InSpaceHigh": 2},
        7
    )


@pytest.fixture
def experiment_1():
    return Experiment(
        'experiment_1',
        1,
        True,
        ["FlyingHigh", "InSpaceLow"],
        ["SrfLanded"]
    )


@pytest.fixture
def experiment_2():
    return Experiment(
        'experiment_2',
        2,
        False,
        ["SrfLanded"],
        ['InSpaceLow', 'InSpaceHigh']
    )


@pytest.fixture
def roc_experiment():
    return Experiment(
        name="ROCExperiment",
        max_value=30,
        requires_atmosphere=False,
        global_situations=['SrfLanded'],
        body='Kerbin'

    )


@pytest.fixture
def kerbin():
    # TODO fix
    KERBIN = [body for body in bodies.load_bodies() if body.name == 'Kerbin'][
        0]
    return KERBIN
