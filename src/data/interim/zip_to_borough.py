import pickle
import re

import click
import parsel
import requests


URL = r'https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm'


def create_dict():
    results = {}  # dictionary the maps (zip code => borough)

    r = requests.get(URL)
    s = parsel.Selector(r.text)

    # scrap results
    cur_borough = None
    _rows = s.css('tr')[1:]
    for _r in _rows:
        borough = _r.css('[headers="header1"]::text').extract_first()
        if borough:
            cur_borough = borough
        zip_codes = _r.css('[headers="header3"]::text').extract_first()
        zip_codes = zip_codes.strip()  # remove beginning space
        zip_codes = re.split(r',\s?', zip_codes)  # split on the comma
        for zc in zip_codes:
            results[zc] = cur_borough

    # input missing values
    missing = {
        '10282': 'Manhattan',
        '11001': 'Queens',
        '11109': 'Queens',
        '10311': 'Staten Island'
    }
    results.update(missing)

    return results


@click.command()
@click.argument('out-dict', type=click.Path(writable=True))
def cli(out_dict):
    """Creates a dictionary that maps (zip code => borough)

    Data is retrieved from https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm

    \b
    Outputs:
        dict (pkl): Dictionary that maps (zip code => borough)
    """
    d = create_dict()
    pickle.dump(d, open(out_dict, mode='wb'))


if __name__ == '__main__':
    cli()
