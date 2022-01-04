import pandas as pd
import pytest

from science.actual_science import parse_situation, parse_save_text


@pytest.fixture
def situations():
    df = pd.DataFrame(data=[
        # Kerbin
        ['KerbinSrfLanded', 'Kerbin', 'SrfLanded', 'global'],
        ['KerbinSrfLandedDeserts', 'Kerbin', 'SrfLanded', 'Deserts'],
        ['KerbinSrfSplashed', 'Kerbin', 'SrfSplashed', 'global'],
        ['KerbinSrfSplashedWater', 'Kerbin', 'SrfSplashed', 'Water'],
        ['KerbinFlyingLow', 'Kerbin', 'FlyingLow', 'global'],
        ['KerbinFlyingLowWater', 'Kerbin', 'FlyingLow', 'Water'],
        ['KerbinFlyingHigh', 'Kerbin', 'FlyingHigh', 'global'],
        ['KerbinFlyingHighWater', 'Kerbin', 'FlyingHigh', 'Water'],
        ['KerbinInSpaceLow', 'Kerbin', 'InSpaceLow', 'global'],
        ['KerbinInSpaceLowWater', 'Kerbin', 'InSpaceLow', 'Water'],
        ['KerbinInSpaceHigh', 'Kerbin', 'InSpaceHigh', 'global'],
        ['KerbinInSpaceHighWater', 'Kerbin', 'InSpaceHigh', 'Water'],
        ['KerbinFlyingLowIceCaps', 'Kerbin', 'FlyingLow', 'IceCaps'],
        # KSC
        ['KerbinSrfLandedRunway', 'KSC', 'SrfLanded', 'Runway'],
        ['KerbinSrfLandedLaunchPad', 'KSC', 'SrfLanded', 'LaunchPad'],
        # recovery situations
        ['MunFlewBy', 'Mun', 'FlewBy', 'global'],
        ['MunOrbited', 'Mun', 'Orbited', 'global'],
        ['MunSubOrbited', 'Mun', 'SubOrbited', 'global'],
        ['KerbinFlew', 'Kerbin', 'Flew', 'global'],
        # TODO test for landed and splashed (once we know what these are)
        # ['MunLanded', 'Mun', 'Landed', ''],
        # ['MunSplashed', 'Mun', 'Splashed', ''],

    ])
    df.columns = ['situation_string', 'body', 'situation', 'biome']
    return df


def test_parse_situation(situations):
    output = parse_situation(situations.situation_string)
    pd.testing.assert_frame_equal(
        output, situations.drop(columns='situation_string')
    )


def test_parse_situation_raises_warning():
    ser = pd.Series(['MunNothing'])
    with pytest.warns(UserWarning):
        parse_situation(ser)


def test_parse_save_text():
    text = (
        "a b \n\n "
        "Science { id = mysteryGoo@KerbinSrfLandedLaunchPad title = Mystery Goo™ Observation from LaunchPad dsc = 1 scv = 0.0532544553 sbv = 0.300000012 sci = 3.69230771 asc = True cap = 3.9000001 } "
        "Science { id = crewReport@KerbinFlyingLowShores title = Crew Report while flying over Kerbin's Shores dsc = 1 scv = 0 sbv = 0.699999988 sci = 3.5 asc = True cap = 3.5 } "
        "Science { id = mysteryGoo@KerbinFlyingLow title = Mystery Goo™ Observation while flying at Kerbin dsc = 1 scv = 0 sbv = 0.699999988 sci = 9.09999943 asc = True cap = 9.09999943 } "
        "Science { id = recovery@KerbinFlew title = Recovery of a vessel that survived a flight. dsc = 1 scv = 0 sbv = 5 sci = 6 asc = True cap = 6 } "
        "Science { id = temperatureScan@KerbinSrfLandedLaunchPad title = Temperature Scan from LaunchPad dsc = 1 scv = 0 sbv = 0.300000012 sci = 2.4000001 asc = True cap = 2.4000001 } "
        "abc"
    )
    output = parse_save_text(text)

    expected = pd.DataFrame([
        ['KSC', 'LaunchPad', 'SrfLanded', 'mysteryGoo', 3.69230771, 3.9000001],
        ['Kerbin', 'Shores', 'FlyingLow', 'crewReport', 3.5, 3.5],
        ['Kerbin', 'global', 'FlyingLow', 'mysteryGoo', 9.09999943, 9.09999943],
        ['Kerbin', 'global', 'Flew', 'recovery', 6, 6],
        ['KSC', 'LaunchPad', 'SrfLanded', 'temperatureScan', 2.4000001, 2.4000001]
    ], columns=['body', 'biome', 'situation', 'experiment', 'current_science', 'max_science']
    ).set_index(['body', 'biome', 'situation', 'experiment'])
    pd.testing.assert_frame_equal(output, expected)
