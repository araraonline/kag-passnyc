import click
import pandas as pd


@click.command()
@click.argument('in-pickle', type=click.Path(exists=True))
@click.argument('out-csv', type=click.Path(writable=True))
def CLI(in_pickle, out_csv):
    """Converts a pickled DataFrame into a csv

    \b
    Inputs:
        pickle (pkl)

    \b
    Outputs:
        csv (csv)
    """
    df = pd.read_pickle(in_pickle)
    df.to_csv(out_csv)


if __name__ == '__main__':
    CLI()
