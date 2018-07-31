import click
import pandas as pd


def preprocess_tests(tests):
    tests = tests.reset_index()
    tests = tests[(tests['Grade'] == 7) &
                  (tests['Year'] == 2017)]
    tests = tests.set_index('DBN')
    tests = tests[[
        'Charter School?',
        'Mean Scale Score - ELA',
        '% Level 2 - ELA',
        '% Level 3 - ELA',
        '% Level 4 - ELA',
        'Mean Scale Score - Math',
        '% Level 2 - Math',
        '% Level 3 - Math',
        '% Level 4 - Math',
    ]]

    return tests


def join_data(locations, tests, shsat, demographics):
    joined = shsat.join(locations).join(tests).join(demographics)
    joined['Percent Other'] = 1 - joined.loc[:, 'Percent Asian':'Percent White'].sum(axis=1, skipna=False)
    joined = joined[[
        'School Name',
        'Charter School?',
        'Borough',
        'Latitude',
        'Longitude',

        'Percent Asian',
        'Percent Black',
        'Percent Hispanic',
        'Percent White',
        'Percent Other',

        'Percent English Language Learners',
        'Percent Students with Disabilities',
        'Percent of Students Chronically Absent',
        'Economic Need Index',

        'Mean Scale Score - ELA',
        '% Level 2 - ELA',
        '% Level 3 - ELA',
        '% Level 4 - ELA',
        'Mean Scale Score - Math',
        '% Level 2 - Math',
        '% Level 3 - Math',
        '% Level 4 - Math',

        '# Students in HS Admissions',
        '# SHSAT Testers',
        '# SHSAT Offers',
        '% SHSAT Testers',
        '% SHSAT Offers',
    ]]
    return joined


@click.command()
@click.argument('in-locations', type=click.Path(exists=True))
@click.argument('in-tests', type=click.Path(exists=True))
@click.argument('in-shsat', type=click.Path(exists=True))
@click.argument('in-demographics', type=click.Path(exists=True))
@click.argument('out-joined', type=click.Path(writable=True))
def CLI(in_locations, in_tests, in_shsat, in_demographics, out_joined):
    """Join information about schools and students that took the SHSAT in 2017

    \b
    Inputs:
        locations (pkl): School Locations (2017-2018)
        tests (pkl): NYS test results (2013-2017)
        shsat (pkl): SHSAT Testers and Offers (2017-18)
        demographics (pkl): Demographics from the School Quality Report (2016-17)

    \b
    Outputs:
        joined (pkl): The resulting dataframe
    """
    locations = pd.read_pickle(in_locations)
    tests = preprocess_tests(pd.read_pickle(in_tests))
    shsat = pd.read_pickle(in_shsat)
    demographics = pd.read_pickle(in_demographics)

    joined = join_data(locations, tests, shsat, demographics)
    joined.to_pickle(out_joined)


if __name__ == '__main__':
    CLI()
