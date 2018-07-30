import click
import pandas as pd


def preprocess(df):
    columns = ['schooldbn', 'communityschool', 'Borough', 'Latitude', 'Longitude']

    # convert communityschool to integer (binary)
    df['communityschool'] = df['communityschool'].str.startswith('Yes').astype(int)

    # standardize boroughs
    df['Borough'] = df['Borough'].fillna('')
    df['Borough'] = df['Borough'].apply(lambda x: x.lower().strip())
    df['Borough'] = df['Borough'].replace('staten is', 'staten_island')

    # add missing info
    # coordinates are not perfect, but they are good enough
    missing_info = {
        '21K098': [ 'brooklyn', 40.583477, -73.953932],
        '05M046': ['manhattan', 40.831713, -73.936023],
        '10X308': [    'bronx', 40.885453, -73.878126],
    }
    for k, v in missing_info.items():
        df.loc[df['schooldbn'] == k, 'Borough'] = v[0]
        df.loc[df['schooldbn'] == k, 'Latitude'] = v[1]
        df.loc[df['schooldbn'] == k, 'Longitude'] = v[2]

    # choose columns and set index
    df = df[columns]
    df = df.rename({
        'schooldbn': 'DBN',
        'communityschool': 'Community School?',
    }, axis=1)
    df = df.set_index('DBN')

    return df


@click.command()
@click.argument('in-directory', type=click.Path(exists=True))
@click.argument('out-basic-info', type=click.Path(writable=True))
def CLI(in_directory, out_basic_info):
    """Extract basic information from schools directory

    \b
    Inputs:
        directory (csv)

    \b
    Outputs:
        basic-info (pkl)
    """
    df = pd.read_csv(in_directory)
    new_df = preprocess(df)
    new_df.to_pickle(out_basic_info)


if __name__ == '__main__':
    CLI()
