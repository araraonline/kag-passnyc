import click
import pandas as pd


# all read functions prepare the DataFrame for merging

def read_basic(in_basic):
    columns = [
        'DBN',
        'School Name',
        'Grade 8',
        '% Female',
        '% Male',
        '% Asian',
        '% Black',
        '% Hispanic',
        '% Multiple Race Categories Not Represented',
        '% White',
        '% Students with Disabilities',
        '% English Language Learners',
        '% Poverty',
        'Economic Need Index'
    ]
    basic = pd.read_pickle(in_basic)
    basic = basic[(basic['Year'] == '2017-18') &
                  (basic['Grade 8'] > 0)]
    basic = basic[columns]
    return basic

def read_results(in_results):
    columns = [
        'DBN',
        'Charter School',
        'Number Tested - ELA',
        'Mean Scale Score - ELA',
        '# Level 1 - ELA',
        '% Level 1 - ELA',
        '# Level 2 - ELA',
        '% Level 2 - ELA',
        '# Level 3 - ELA',
        '% Level 3 - ELA',
        '# Level 4 - ELA',
        '% Level 4 - ELA',
        '# Level 3+4 - ELA',
        '% Level 3+4 - ELA',
        'Number Tested - Math',
        'Mean Scale Score - Math',
        '# Level 1 - Math',
        '% Level 1 - Math',
        '# Level 2 - Math',
        '% Level 2 - Math',
        '# Level 3 - Math',
        '% Level 3 - Math',
        '# Level 4 - Math',
        '% Level 4 - Math',
        '# Level 3+4 - Math',
        '% Level 3+4 - Math'
    ]
    results = pd.read_pickle(in_results)
    results = results[(results['Grade'] == 7) &
                      (results['Year'] == 2017)]
    results = results[columns]
    return results

def read_applicants(in_applicants):
    columns = [
        'DBN',
        'borough',
        'testers',
    ]
    applicants = pd.read_pickle(in_applicants)
    applicants = applicants[columns]
    return applicants

def merge_data(basic, results, applicants):
    # merging
    d1 = basic.set_index('DBN')
    d2 = results.set_index('DBN')
    d3 = applicants.set_index('DBN')

    df = d1.join(d2, how='inner').join(d3, how='inner')
    df.shape

    # renaming columns
    new_names = {
        'borough': 'Borough',
        'testers': '# SHSAT Testers',
        'Grade 8': '# Students Grade 8'
    }
    df = df.rename(columns=new_names)

    # reordering columns
    columns = [
        'School Name',
        'Borough',
        'Charter School',
        'Economic Need Index',
        '% Female',
        '% Male',
        '% Asian',
        '% Black',
        '% Hispanic',
        '% Multiple Race Categories Not Represented',
        '% White',
        '% Students with Disabilities',
        '% English Language Learners',
        '% Poverty',
        'Number Tested - ELA',
        'Mean Scale Score - ELA',
        '# Level 1 - ELA',
        '% Level 1 - ELA',
        '# Level 2 - ELA',
        '% Level 2 - ELA',
        '# Level 3 - ELA',
        '% Level 3 - ELA',
        '# Level 4 - ELA',
        '% Level 4 - ELA',
        '# Level 3+4 - ELA',
        '% Level 3+4 - ELA',
        'Number Tested - Math',
        'Mean Scale Score - Math',
        '# Level 1 - Math',
        '% Level 1 - Math',
        '# Level 2 - Math',
        '% Level 2 - Math',
        '# Level 3 - Math',
        '% Level 3 - Math',
        '# Level 4 - Math',
        '% Level 4 - Math',
        '# Level 3+4 - Math',
        '% Level 3+4 - Math',
        '# Students Grade 8',
        '# SHSAT Testers'
    ]
    df = df[columns]

    return df


@click.command()
@click.argument('in-basic', type=click.Path(exists=True))
@click.argument('in-results', type=click.Path(exists=True))
@click.argument('in-applicants', type=click.Path(exists=True))
@click.argument('out-merged', type=click.Path(writable=True))
def cli(in_basic, in_results, in_applicants, out_merged):
    """Merges all schools data to 2017

    \b
    Inputs:
        basic (pkl): The basic schools demographics file.
        results (pkl): The NYS test results files.
        applicants (pkl): The SHSAT applicants table from the NYT.

    \b
    Outputs:
        merged (pkl): A DataFrame containing all merged data for the SHSAT
            applicants of 2017.
    """
    basic = read_basic(in_basic)
    results = read_results(in_results)
    applicants = read_applicants(in_applicants)

    merged = merge_data(basic, results, applicants)    
    merged.to_pickle(out_merged)


if __name__ == '__main__':
    cli()
