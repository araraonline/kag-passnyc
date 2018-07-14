DEMOGRAPHICS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/demographicsnapshot201314to201718public_final.xlsx'
ELA_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/school-ela-results-2013-2017-public.xlsx'
MATH_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/school-math-results-2013-2017-public.xlsx'
CHARTER_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/charter-school-results-2013-2017-public.xlsx'


all: data/flags/download \
	 data/flags/preprocess \
	 data/raw/nyt_table.csv

data/flags/download:
	kaggle datasets download -d passnyc/data-science-for-good -p data/raw
	wget -nc -P 'data/raw/' $(ELA_RESULTS_URL) $(MATH_RESULTS_URL) $(CHARTER_RESULTS_URL) $(DEMOGRAPHICS_URL)
	touch data/flags/download

data/flags/preprocess: data/flags/download \
					     src/data/pre/schools2016.py \
						 src/data/pre/schools_demographics.py
	python -m src.data.pre.schools2016 'data/raw/2016 School Explorer.csv' 'data/pre/schools2016.pkl'
	python -m src.data.pre.schools_demographics 'data/raw/demographicsnapshot201314to201718public_final.xlsx' 'data/pre/schools_demographics.pkl'
	touch data/flags/preprocess

data/raw/nyt_table.csv: src/data/raw/nyt_table.py
	python -m src.data.raw.nyt_table 'data/raw/nyt_table.csv'

.PHONY: notebooks
notebooks:
	jupyter nbconvert --output-dir='notebooks/html' --to=html "notebooks/*.ipynb"
