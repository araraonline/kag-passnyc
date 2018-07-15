import click
import numpy as np
import pandas as pd


# the character '—' is pretty close, but not equal to '-'

def parse_int(x):
    return np.nan if x == '—' else int(x)

def parse_pct(x):
    return np.nan if x == '—' else float(x[:-1]) / 100.0


# core

def preprocess(df):
    df['testers'] = df['testers'].apply(parse_int)
    df['offers'] = df['offers'].apply(parse_int)

    df['offers_per_student'] = df['offers_per_student'].apply(parse_pct)
    df['pct_hispanic_black'] = df['pct_hispanic_black'].apply(parse_pct)

    return df


# CLI

@click.command()
@click.argument('in-table', type=click.Path(exists=True))
@click.argument('out-dataframe', type=click.Path(writable=True))
def cli(in_table, out_dataframe):
    """Preprocess NYT table data

    \b
    Inputs:
        table (csv): raw table data extracted from the site

    \b
    Outputs:
        dataframe (pkl): the DataFrame with parsed values
    """
    df = pd.read_csv(in_table)
    parsed_df = preprocess(df)
    parsed_df.to_pickle(out_dataframe)


if __name__ == '__main__':
    cli()
