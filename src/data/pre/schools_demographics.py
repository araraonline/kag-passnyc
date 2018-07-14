import click
import pandas as pd


def read_file(in_excel):
    df = pd.read_excel(in_excel, sheet_name='School', header=0)
    return df


@click.command()
@click.argument('in-excel', type=click.Path(exists=True))
@click.argument('out-dataframe', type=click.Path(writable=True))
def cli(in_excel, out_dataframe):
    """Parses an excel file containing school demographics

    \b
    Inputs:
        excel (xlsx): The excel data from the NYC site.

    \b
    Outputs:
        dataframe (pkl): The parsed DataFrame.
    """
    df = read_file(in_excel)
    df.to_pickle(out_dataframe)


if __name__ == '__main__':
    cli()
