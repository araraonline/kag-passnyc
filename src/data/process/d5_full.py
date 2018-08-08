import click
import numpy as np
import pandas as pd


def preprocess_d5(df):
    df = df.drop('School Name', axis=1)
    return df


def preprocess_demo(demo):
    demo['Percent Other'] = 1 - demo.loc[:, 'Percent Asian':'Percent White'].sum(axis=1, skipna=False)
    return demo


def preprocess_tests(tests):
    tests = tests.reset_index()
    tests = tests[tests['Grade'] == 7]
    tests = tests.drop('Grade', axis=1)
    tests = tests.set_index(['DBN', 'Year'])

    return tests


def join_dfs(d5, demo, tests):
    joined = d5.join(demo).join(tests)

    # remove rows from 2013 and 2014
    joined = joined.reset_index()
    joined = joined[joined['Year'].isin([2015, 2016])]
    joined = joined.set_index(['DBN', 'Year'])

    # reorder columns
    joined = joined[[
        'School Name',
        'Percent Asian',
        'Percent Black',
        'Percent Hispanic',
        'Percent White',
        'Percent Other',
        'Percent English Language Learners',
        'Percent Students with Disabilities',
        'Percent of Students Chronically Absent',
        'Economic Need Index',
        'Charter School?',
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
        'Enrollment on 10/31',
        '# SHSAT Registrants',
        '# SHSAT Testers',
        '% SHSAT Registrants',
        '% SHSAT Testers',
    ]]

    return joined


@click.command()
@click.argument('in-d5', type=click.Path(exists=True))
@click.argument('in-demographics', type=click.Path(exists=True))
@click.argument('in-test-results', type=click.Path(exists=True))
@click.argument('out-joined', type=click.Path(writable=True))
def CLI(in_d5, in_demographics, in_test_results, out_joined):
    d5 = pd.read_pickle(in_d5)
    demo = pd.read_pickle(in_demographics)
    tests = pd.read_pickle(in_test_results)

    d5 = preprocess_d5(d5)
    demo = preprocess_demo(demo)
    tests = preprocess_tests(tests)

    joined = join_dfs(d5, demo, tests)
    joined.to_pickle(out_joined)


if __name__ == '__main__':
    CLI()
