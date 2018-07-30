import click
import numpy as np
import pandas as pd

def preprocess(df):
    # set columns
    columns = [
        'Feeder School DBN',
        'Count of Students in HS Admissions',
        'Count of Testers',
        'Count of Offers',
    ]
    df = df[columns].copy()
    df.columns = ['DBN', '# Students in HS Admissions', '# SHSAT Testers', '# SHSAT Offers']

    # convert counts to numbers (were originally string)
    df['# Students in HS Admissions'] = df['# Students in HS Admissions'].apply(lambda x: np.nan if x == '0-5' else int(x))
    df['# SHSAT Testers'] = df['# SHSAT Testers'].apply(lambda x: np.nan if x == '0-5' else int(x))
    df['# SHSAT Offers'] = df['# SHSAT Offers'].apply(lambda x: np.nan if x == '0-5' else int(x))

    # create percentage values
    df['% SHSAT Testers'] = df['# SHSAT Testers'] / df['# Students in HS Admissions']  # percentage of testers among students that want to go to HS
    df['% SHSAT Offers'] = df['# SHSAT Offers'] / df['# Students in HS Admissions']

    # set index
    df = df.set_index('DBN')

    return df


@click.command()
@click.argument('in-table', type=click.Path(exists=True))
@click.argument('out-table', type=click.Path(writable=True))
def CLI(in_table, out_table):
    """Preprocess SHSAT table, calculating percentages

    \b
    Inputs:
        table (csv)

    \b
    Outputs:
        table (pkl)
    """
    df = pd.read_csv(in_table)
    new_df = preprocess(df)
    new_df.to_pickle(out_table)


if __name__ == '__main__':
    CLI()
