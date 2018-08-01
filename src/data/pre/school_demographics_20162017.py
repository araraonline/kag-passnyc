import click
import pandas as pd


def read_excel_file(path):
    return pd.read_excel(path, sheet_name='Summary', skiprows=[0])

def preprocess(df):
    columns = [
        'DBN',
        'School Name',
        'Percent Asian',
        'Percent Black',
        'Percent Hispanic',
        'Percent White',
        'Percent English Language Learners',
        'Percent Students with Disabilities',
        'Percent of Students Chronically Absent',
        'Economic Need Index',
    ]
    df = df[columns]
    df = df.set_index('DBN')
    return df


@click.command()
@click.argument('in-quality-report', type=click.Path(exists=True))
@click.argument('out-dataframe', type=click.Path(writable=True))
def CLI(in_quality_report, out_dataframe):
    """Extract basic info from NY schools Quality  Report

    \b
    Inputs:
        quality-report (xlsx): The quality report, an excel file

    \b
    Outputs:
        dataframe (pkl): The resulting DataFrame
    """
    df = read_excel_file(in_quality_report)
    df = preprocess(df)
    df.to_pickle(out_dataframe)


if __name__ == '__main__':
    CLI()
