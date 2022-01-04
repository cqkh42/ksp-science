# TODO asteroid
# TODO comet
# TODO transmission
# TODO deployable science - ionographer
# TODO Where can you be 'splasheddown'

import warnings
from science import actual_science, possible_science


def science():
    actual = actual_science.load()
    possible = possible_science.load()

    df = possible.merge(actual, how='outer', left_index=True, right_index=True,
                        suffixes=('_possible', '_actual'))
    missing_possibles = df.loc[df.max_science_possible.isnull()]
    if not missing_possibles.empty:
        warnings.warn(f'Actual science not in possible: {missing_possibles.index.to_list()}', UserWarning)
    df['max_science'] = df.max_science_actual.fillna(df.max_science_possible)
    df = df.drop(columns=['max_science_actual', 'max_science_possible'])
    df.current_science = df.current_science.fillna(0)
    df['remaining'] = df.max_science - df.current_science
    df = df.loc[df.current_science != df.max_science]

    return df
