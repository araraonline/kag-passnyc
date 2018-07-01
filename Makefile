all: data/flags/download \
	 data/flags/preprocess

data/flags/download:
	kaggle datasets download -d passnyc/data-science-for-good -p data/raw
	touch data/flags/download

data/flags/preprocess: data/flags/download \
					     src/data/pre/schools2016.py
	python -m src.data.pre.schools2016 'data/raw/2016 School Explorer.csv' 'data/pre/schools2016.pkl'
	touch data/flags/preprocess
