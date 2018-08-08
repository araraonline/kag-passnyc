import click
import numpy as np
import pandas as pd


def preprocess(df):
    # keep grade 8
    df = df[df['Grade level'] == 8]
    df = df.drop('Grade level', axis=1)

    # rename columns
    df = df.rename({
        'School name': 'School Name',
        'Year of SHST': 'Year',
        'Number of students who registered for the SHSAT': '# SHSAT Registrants',
        'Number of students who took the SHSAT': '# SHSAT Testers'
    }, axis=1)

    # create columns
    df['% SHSAT Registrants'] = df['# SHSAT Registrants'] / df['Enrollment on 10/31']
    df['% SHSAT Testers'] = df['# SHSAT Testers'] / df['Enrollment on 10/31']

    # clip percentage values
    df['% SHSAT Registrants'] = np.clip(df['% SHSAT Registrants'], 0.0, 1.0)
    df['% SHSAT Testers'] = np.clip(df['% SHSAT Testers'], 0.0, 1.0)

    # set index
    df = df.set_index(['DBN', 'Year'])

    return df


@click.command()
@click.argument('in-d5', type=click.Path(exists=True))
@click.argument('out-d5', type=click.Path(writable=True))
def CLI(in_d5, out_d5):
    """Preprocess SHSAT data from D5 (Central Harlem)

    \b
    Inputs:
        d5 (csv)

    \b
    Ouputs(
        d5 (pkl)
    """
    df = pd.read_csv(in_d5)
    new_df = preprocess(df)
    new_df.to_pickle(out_d5)


if __name__ == '__main__':
    CLI()
