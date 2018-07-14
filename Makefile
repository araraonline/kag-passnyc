all: data/flags/download \
	 data/flags/preprocess \
	 data/raw/nyt_table.csv

data/flags/download:
	kaggle datasets download -d passnyc/data-science-for-good -p data/raw
	touch data/flags/download

data/flags/preprocess: data/flags/download \
					     src/data/pre/schools2016.py
	python -m src.data.pre.schools2016 'data/raw/2016 School Explorer.csv' 'data/pre/schools2016.pkl'
	touch data/flags/preprocess

data/raw/nyt_table.csv: src/data/raw/nyt_table.py
	python -m src.data.raw.nyt_table 'data/raw/nyt_table.csv'

.PHONY: notebooks
notebooks:
	jupyter nbconvert --output-dir='notebooks/html' --to=html "notebooks/*.ipynb"
