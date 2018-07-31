import json
import re

import click
import pandas as pd
import shapely.geometry as geo
from src.util import snakecase


def load_preprocess_locations(in_locations_table):
    df = pd.read_csv(in_locations_table)

    # columns
    columns = [
        'ATS SYSTEM CODE',
        'LOCATION_CODE',
        'LOCATION_NAME',
        'MANAGED_BY_NAME',
        'PRIMARY_BUILDING_CODE',
        'COMMUNITY_SCHOOL_SUP_NAME',
        'Location 1',
    ]
    df = df[columns]

    # set index
    df['ATS SYSTEM CODE'] = df['ATS SYSTEM CODE'].str.strip()
    df = df.set_index('ATS SYSTEM CODE')
    df.index.name = 'DBN'

    # remove school not present in NYC
    df = df[df['Location 1'].notnull()]

    return df


def load_preprocess_geojson(in_boroughs):
    # load
    with open(in_boroughs) as f:
        geojson = json.load(f)

    # precompute shapes
    for feature in geojson['features']:
        feature['polygon'] = geo.shape(feature['geometry'])

    return geojson


def extract_coordinates(addr):
    """Extract coordinates from address"""
    coordinates = map(float, re.findall(r'\((.*), (.*)\)$', addr)[0])
    return tuple(coordinates)


def get_borough(school):
    point = geo.Point(school['Longitude'], school['Latitude'])

    for feature in geojson['features']:
        polygon = feature['polygon']
        if polygon.contains(point):
            return feature['properties']['BoroName']


@click.command()
@click.argument('in-locations-table', type=click.Path(exists=True))
@click.argument('in-boroughs', type=click.Path(exists=True))
@click.argument('out-school-locations', type=click.Path(writable=True))
def CLI(in_locations_table,in_boroughs, out_school_locations):
    """Retrieve schools Lat/Lon and Borough

    Borough information is retrieved comparing a geojson file containing the
    boroughs to the school coordinates.

    \b
    Inputs:
        locations-table (csv)
        boroughs (geojson)

    \b
    Ouputs:
        school-locations (pkl)
    """
    df = load_preprocess_locations(in_locations_table)
    geojson = load_preprocess_geojson(in_boroughs)

    coordinates = pd.DataFrame([extract_coordinates(x) for x in df['Location 1']], index=df.index, columns=['Latitude', 'Longitude'])
    coordinates.loc['84X497', ['Latitude', 'Longitude']] = [40.816698, -73.918099]  # bad entry

    def get_borough(school):
        point = geo.Point(school['Longitude'], school['Latitude'])
        for feature in geojson['features']:
            polygon = feature['polygon']
            if polygon.contains(point):
                return feature['properties']['BoroName']
    boroughs = coordinates.apply(get_borough, axis=1)
    boroughs = boroughs.apply(snakecase)  # convert to snake_case for easy dummifying
    boroughs.name = 'Borough'

    results = coordinates.join(boroughs)
    results.to_pickle(out_school_locations)


if __name__ == '__main__':
    CLI()
