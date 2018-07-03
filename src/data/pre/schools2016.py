"""Clean and format the dataframe containing information from 2016 schools

Steps taken here:

- Remove rows where 'Adjusted Grade', 'New?' or 'Other Location Code in LCGMS'
  are null.
- Drop these columns.
- Remove rows where there is at least one NA that is not in the 'School Income
  Estimate' column

- Convert percentage columns (which are str) to float values
- Convert ratings into numerical values
- Convert the 'School Income Estimate' str into a float

**Call this script from the base directory**

"""
import click
import numpy as np
import pandas as pd

# converter functions

def p_to_f(p):
    # percentage to float
    return float(p[:-1])

def r_to_v(r):
    # rating to value
    return {
        'Not Meeting Target': 1,
        'Approaching Target': 2,
        'Meeting Target': 3,
        'Exceeding Target': 4
    }[r]

def g_to_v(g):
    # grade to value
    if g == 'PK':
        return -1
    elif g == '0K':
        return 0
    else:
        return int (g)

def d_to_f(d):
    # dollar to float
    if isinstance(d, str):
        return float(d.replace('$', '').replace(',', ''))
    else:
        return np.nan


# main function

def clean_df(df):
    # remove different values
    df = df[df['Adjusted Grade'].isnull()]
    df = df[df['New?'].isnull()]
    df = df[df['Other Location Code in LCGMS'].isnull()]
    df = df.drop(['Adjusted Grade', 'New?', 'Other Location Code in LCGMS'], axis=1)

    # drop rows with any NA
    # except when in the column School Income Estimate
    sie = df['School Income Estimate']
    df = df.drop(['School Income Estimate'], axis=1).dropna()
    df['School Income Estimate'] = sie

    # format columns
    df['Community School?'] = df['Community School?'].apply(lambda x: int(x == 'Yes'))
    df['School Income Estimate'] = df['School Income Estimate'].apply(d_to_f)
    df['Grade Low'] = df['Grade Low'].apply(g_to_v)
    df['Grade High'] = df['Grade High'].apply(g_to_v)

    # format percentage columns
    percentage_cols = [
        'Percent ELL',
        'Percent Asian',
        'Percent Black',
        'Percent Hispanic',
        'Percent Black / Hispanic',
        'Percent White',
        'Student Attendance Rate',
        'Percent of Students Chronically Absent',
        'Rigorous Instruction %',
        'Collaborative Teachers %',
        'Supportive Environment %',
        'Effective School Leadership %',
        'Strong Family-Community Ties %',
        'Trust %',
    ]

    for col in percentage_cols:
        df[col] = df[col].apply(p_to_f)

    # format rating columns
    rating_cols = [
        'Student Achievement Rating',
        'Rigorous Instruction Rating',
        'Collaborative Teachers Rating',
        'Supportive Environment Rating',
        'Effective School Leadership Rating',
        'Strong Family-Community Ties Rating',
        'Trust Rating'
    ]

    for col in rating_cols:
        df[col] = df[col].apply(r_to_v)

    return df


@click.command()
@click.argument('in-dataframe', type=click.Path(exists=True))
@click.argument('out-dataframe', type=click.Path(writable=True))
def cli(in_dataframe, out_dataframe):
    """Format and clean 2016 schools dataframe

    \b
    Inputs:
        dataframe (csv): The raw csv file from Kaggle

    \b
    Outputs:
        dataframe (pkl): The cleaned DataFrame, as a pickle file
    """
    df = pd.read_csv(in_dataframe)
    out_df = clean_df(df)
    out_df.to_pickle(out_dataframe)


if __name__ == '__main__':
    cli()
