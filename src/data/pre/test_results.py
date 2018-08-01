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
    c_ela = charters['ELA']
    c_math = charters['Math']

    # remove unused columns
    ela = ela.drop(['School Name', 'Category'], axis=1)
    math = math.drop(['School Name', 'Category'], axis=1)
    c_ela = c_ela.drop(['School Name', 'Category'], axis=1)
    c_math = c_math.drop(['School Name', 'Category'], axis=1)

    # create charter school flag
    ncharter_dbn = set(ela['DBN']) | set(math['DBN'])
    charter_flags1 = pd.Series(0, index=ncharter_dbn)

    charter_dbn = set(c_ela['DBN']) | set(c_math['DBN'])
    charter_flags2 = pd.Series(1, index=charter_dbn)

    charter_flags = pd.concat([charter_flags1, charter_flags2])
    charter_flags.name = 'Charter School?'
    charter_flags.index.name = 'DBN'

    # create empty DataFrame with correct index
    DBN = sorted(charter_flags.index)
    Grade = [3, 4, 5, 6, 7, 8, 'All Grades']
    Year = [2013, 2014, 2015, 2016, 2017]
    index = pd.MultiIndex.from_product([DBN, Grade, Year], names=['DBN', 'Grade', 'Year'])
    base_df = pd.DataFrame(index=index)

    # concatenate grades
    f_ela = pd.concat([ela, c_ela]).set_index(['DBN', 'Grade', 'Year'])
    f_math = pd.concat([math, c_math]).set_index(['DBN', 'Grade', 'Year'])

    # join everything
    grades = f_ela.join(f_math, how='outer', lsuffix=' - ELA', rsuffix=' - Math')
    everything = base_df.join(charter_flags).join(grades)

    # fix values for missing rows
    everything.loc[everything['Number Tested - ELA'].isnull(), 'Number Tested - ELA'] = 0
    everything.loc[everything['Number Tested - Math'].isnull(), 'Number Tested - Math'] = 0

    return everything


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
