import click
import pandas as pd


@click.command()
@click.argument('in-demo2015', type=click.Path(exists=True))
@click.argument('in-demo2016', type=click.Path(exists=True))
@click.argument('in-demo2017', type=click.Path(exists=True))
@click.argument('out-merged', type=click.Path(writable=True))
def CLI(in_demo2015, in_demo2016, in_demo2017, out_merged):
    """Join demographics from all the available years

    \b
    Inputs:
        in_demo2015 (pkl): School demographics from the year 2014-2015
        in_demo2016 (pkl): same
        in_demo2017 (pkl): same

    \b
    Outputs:
        out_merged (pkl): Merged school demographics from 2015 to 2017
    """
    # load
    sd2015 = pd.read_pickle(in_demo2015)
    sd2016 = pd.read_pickle(in_demo2016)
    sd2017 = pd.read_pickle(in_demo2017)

    # set years
    sd2015['Year'] = 2015
    sd2016['Year'] = 2016
    sd2017['Year'] = 2017

    # set indexes
    sd2015 = sd2015.reset_index().set_index(['DBN', 'Year'])
    sd2016 = sd2016.reset_index().set_index(['DBN', 'Year'])
    sd2017 = sd2017.reset_index().set_index(['DBN', 'Year'])

    # merge
    sd = pd.concat([sd2015, sd2016, sd2017])

    # export
    sd.to_pickle(out_merged)


if __name__ == '__main__':
    CLI()
