"""This model will use all features available for us and is trained in all of
the data of 2017
"""
import pickle

import click
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.special import logit
from sklearn.decomposition import PCA


np.random.seed(1)


def preprocess_df(df):
    # drop schools with missing test data
    df = df[df.loc[:, 'Mean Scale Score - ELA':'% Level 4 - Math'].notnull().all(axis=1)]

    # drop schools with missing attendance data
    df = df[df['Percent of Students Chronically Absent'].notnull()]

    # schools with 0-5 SHSAT testers have this value set to NaN
    df = df[df['# SHSAT Testers'].notnull()]

    return df


def get_inputs(df):
    base_df = df[[  # explanatory variables
        'Charter School?',
        'Percent Asian',
        'Percent Black',
        'Percent Hispanic',
        'Percent Other',
        'Percent English Language Learners',
        'Percent Students with Disabilities',
        'Economic Need Index',
        'Percent of Students Chronically Absent',
        
        'Mean Scale Score - ELA',
        '% Level 2 - ELA',
        '% Level 3 - ELA',
        '% Level 4 - ELA',
        'Mean Scale Score - Math',
        '% Level 2 - Math',
        '% Level 3 - Math',
        '% Level 4 - Math',
    ]]

    # transform the variables (apply the PCA)
    n_components = 8
    pca = PCA(n_components)
    transformed = pca.fit_transform(base_df)
    transformed = pd.DataFrame(transformed, index=base_df.index, columns=["PC{}".format(i+1) for i in range(n_components)])

    # add a constant column (needed for our model with statsmodels)
    inputs = transformed
    inputs.insert(0, 'Constant', 1.0)

    return inputs


def get_outputs(df):
    outputs = logit(df['% SHSAT Testers'])
    return outputs


@click.command()
@click.argument('in-schools2017', type=click.Path(exists=True))
@click.argument('out-model', type=click.Path(writable=True))
def CLI(in_schools2017, out_model):
    """Create a model for the percentage of shsat applicants

    \b
    Inputs:
        schools2017 (pkl)

    \b
    Outputs:
        model (pkl): A statsmodels.RLM instance. Must be fitted later.
    """
    df = pd.read_pickle(in_schools2017)
    df = preprocess_df(df)

    inputs = get_inputs(df)
    outputs = get_outputs(df)
    model = sm.RLM(outputs, inputs, M=sm.robust.norms.HuberT())

    with open(out_model, mode='wb') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    CLI()
