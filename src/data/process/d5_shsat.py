import click
import pandas as pd


def preprocess_centralh(centralh):
    centralh = centralh.drop('School Name', axis=1)
    return centralh


def preprocess_tests(tests):
    tests = tests.reset_index()
    tests = tests[tests['Grade'] == 7]
    tests = tests.drop('Grade', axis=1)
    tests = tests.set_index(['DBN', 'Year'])
    return tests


@click.command()
@click.argument('in-d5', type=click.Path(exists=True))
@click.argument('in-results', type=click.Path(exists=True))
@click.argument('out-merged', type=click.Path(writable=True))
def CLI(in_d5, in_results, out_merged):
    """Merge D5 dataframe into common core test results

    \b
    Inputs:
        d5 (pkl): Preprocessed SHSAT data for D5 (Central Harlem)
        results (pkl): Preprocessed test results

    \b
    Outputs:
        merged (pkl)
    """
    centralh = pd.read_pickle(in_d5)
    centralh = preprocess_centralh(centralh)
    tests = pd.read_pickle(in_results)
    tests = preprocess_tests(tests)

    merged = tests.join(centralh, how='right')
    merged.to_pickle(out_merged)


if __name__ == '__main__':
    CLI()
