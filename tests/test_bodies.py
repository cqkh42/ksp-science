import pandas as pd


def test_situations(body_2):
    expected = pd.DataFrame([
        ['body_2', 'biome_a', 'InSpaceLow', 1, False],
        ['body_2', 'biome_a', 'InSpaceHigh', 2, False],
        ['body_2', 'biome_b', 'InSpaceLow', 1, False],
        ['body_2', 'biome_b', 'InSpaceHigh', 2, False],
    ], columns=['body', 'biome', 'situation', 'multiplier', 'has_atmosphere']
    ).set_index(['body', 'biome', 'situation'])

    output = body_2.situations()
    pd.testing.assert_frame_equal(expected, output)
