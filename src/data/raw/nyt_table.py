from collections import OrderedDict

import click
import pandas as pd
import parsel
import requests


def retrieve_table():
    URL = r'https://www.nytimes.com/interactive/2018/06/29/nyregion/nyc-high-schools-middle-schools-shsat-students.html?rref=collection%2Fbyline%2Fjasmine-c.-lee&action=click&contentCollection=undefined&region=stream&module=stream_unit&version=latest&contentPlacement=1&pgtype=collection'

    # make request
    r = requests.get(URL)
    s = parsel.Selector(r.text)

    # extract rows
    schools = []

    for _row in s.css('.g-main tr'):
        school = OrderedDict()
        school['DBN'] = _row.css('::attr(data-dbn)').extract_first()
        school['school_name_number'] = _row.css('.g-school-name-number::text').extract_first()
        school['school_name_details'] = _row.css('.g-school-name-details::text').extract_first()
        school['borough'] = _row.css('.g-borough::text').extract_first()
        school['testers'] = _row.css('.g-testers::text').extract_first()
        school['offers'] = _row.css('.g-offers::text').extract_first()
        school['offers_per_student'] = _row.css('.g-offers-per-student::text').extract_first()
        school['pct_hispanic_black'] = _row.css('.g-pct::text').extract_first()    
        schools.append(school)

    df = pd.DataFrame(schools)
    assert df.shape == (589, 8)

    return df


@click.command()
@click.argument('out-table', type=click.Path(writable=True))
def cli(out_table):
    """Retrieve the SHSAT applicants/admission table from 2017

    This information was present in The New York Times...

    \b
    Outputs:
        table (csv): A table containing the raw data extracted from the NYT
    """
    df = retrieve_table()
    df.to_csv(out_table, index=False)
    

if __name__ == '__main__':
    cli()
