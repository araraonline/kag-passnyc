import click
import pandas as pd

COLUMNS = [
    'DBN',
    'School Name',
    'Grade',
    'Year',
    'Category',
    'Number Tested',
    'Mean Scale Score',
    '# Level 1',
    '% Level 1',
    '# Level 2',
    '% Level 2',
    '# Level 3',
    '% Level 3',
    '# Level 4',
    '% Level 4',
    '# Level 3+4',
    '% Level 3+4'
]

def read_ela(in_ela_excel):
    click.echo("Reading ELA excel...")
    df = pd.read_excel(in_ela_excel, sheet_name='All Students', skiprows=7, na_values='s')
    df = df.iloc[:,1:]  # drop first column
    df.columns = COLUMNS
    return df

def read_math(in_math_excel):
    click.echo("Reading Math excel...")
    df = pd.read_excel(in_math_excel, sheet_name='All Students', skiprows=7, na_values='s')
    df = df.iloc[:,1:]  # drop first column
    df.columns = COLUMNS
    return df

def read_charters(in_charter_excel):
    click.echo("Reading charter excel...")
    charters = pd.read_excel(in_charter_excel, sheet_name=['ELA', 'Math'], skiprows=7, na_values='s')
    charters['ELA'].columns = COLUMNS
    charters['Math'].columns = COLUMNS
    return charters

def read_all(in_ela_excel, in_math_excel, in_charter_excel):
    ela = read_ela(in_ela_excel)
    math = read_math(in_math_excel)
    charters = read_charters(in_charter_excel)

    click.echo("Joining test results...")

    # charter file is divided in 2 sheets
    charter_ela = charters['ELA']
    charter_math = charters['Math']

    # add charter school flag before concatenation
    ela['Charter School'] = 0
    charter_ela['Charter School'] = 1

    # concat usual + charter
    ela_all = pd.concat([ela, charter_ela], ignore_index=True)
    math_all = pd.concat([math, charter_math], ignore_index=True)

    # join ELA + Math
    d1 = ela_all.drop('Category', axis=1)
    d2 = math_all.drop(['Category', 'School Name'], axis=1)  # School Name already present in ELA dataframe
    # Charter School flag present in ELA dataframe
    d2 = d2.set_index(['DBN', 'Grade', 'Year'])
    merged = d1.join(d2, how='inner', on=['DBN', 'Grade', 'Year'], lsuffix=" - ELA", rsuffix=" - Math")

    return merged


@click.command()
@click.argument('in-ela-excel', type=click.Path(exists=True))
@click.argument('in-math-excel', type=click.Path(exists=True))
@click.argument('in-charter-excel', type=click.Path(exists=True))
@click.argument('out-dataframe', type=click.Path(writable=True))
def cli(in_ela_excel, in_math_excel, in_charter_excel, out_dataframe):
    """Read test results files and merge them into one big DataFrame

    While both ELA and Math files contain statistics for different sectors of
    students, we are only gonna use the general statistics, that is,
    considering all students as if they were the same.

    \b
    Inputs:
        ela-excel (xlsx): NYC ELA test results
        math-excel (xlsx): NYC Math test results
        charter-excel (xlsx): NYC ELA and Math results for charter schools

    \b
    Outputs:
        dataframe (pkl): The place to dump the result
    """
    df = read_all(in_ela_excel, in_math_excel, in_charter_excel)

    click.echo("Saving joined results...")
    df.to_pickle(out_dataframe)


if __name__ == '__main__':
    cli()
