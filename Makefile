DEMOGRAPHICS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/demographicsnapshot201314to201718public_final.xlsx'
ELA_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/school-ela-results-2013-2017-public.xlsx'
MATH_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/school-math-results-2013-2017-public.xlsx'
CHARTER_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/charter-school-results-2013-2017-public.xlsx'

ARTICLE_URL = 'https://steinhardt.nyu.edu/scmsAdmin/media/users/sg158/PDFs/Pathways_to_elite_education/WorkingPaper_PathwaystoAnEliteEducation.pdf'

BOROUGHS_KERNEL_URL = 'https://www.kaggleusercontent.com/kf/4643812/eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..2fm9WrpPxTkLeHe2we2Bhg.4ERx0D4arB6hMnagYqXbu9LpFNmRP685Y5gJ9nDpb-9a6xxf7oySr_3LVrh-UwW8aSIPo2VX1sUVLkt1XUc-_TpgtNogNp1PD1nB2kRWbPnGm06pMy8FvRRV060Oy2BT1FxGy2RloW3FuFPSeliu6bfrkBO3cKr8tanHTZNjDY0.BU8mKhlddidc31eeD7COhg/NYC%20Schools%20Boroughs.csv'


all: data/flags/external \
	 data/flags/raw \
	 data/flags/pre \
	 data/flags/interim \
	 data/flags/process

data/flags/external:
	wget -nc -P 'data/external/' $(BOROUGHS_KERNEL_URL)
	wget -nc -P 'data/external/' $(ARTICLE_URL)
	touch data/flags/external

data/flags/raw: src/data/raw/nyt_table.py
	kaggle datasets download -d passnyc/data-science-for-good -p data/raw
	wget -nc -P 'data/raw/' $(ELA_RESULTS_URL) $(MATH_RESULTS_URL) $(CHARTER_RESULTS_URL) $(DEMOGRAPHICS_URL)
	python -m src.data.raw.nyt_table 'data/raw/nyt_table.csv'
	touch data/flags/raw

data/flags/pre: data/flags/external \
				data/flags/raw \
				 src/data/pre/schools2016.py \
				 src/data/pre/schools_demographics.py \
				 src/data/pre/test_results.py \
				 src/data/pre/nyt_table.py
	python -m src.data.pre.schools2016 'data/raw/2016 School Explorer.csv' 'data/pre/schools2016.pkl'
	python -m src.data.pre.schools_demographics 'data/raw/demographicsnapshot201314to201718public_final.xlsx' 'data/pre/schools_demographics.pkl'
	python -m src.data.pre.test_results 'data/raw/school-ela-results-2013-2017-public.xlsx' 'data/raw/school-math-results-2013-2017-public.xlsx' 'data/raw/charter-school-results-2013-2017-public.xlsx' 'data/pre/test_results.pkl'
	python -m src.data.pre.nyt_table 'data/raw/nyt_table.csv' 'data/pre/nyt_table.pkl'

	pdfimages -png -f 22 -l 22 data/external/WorkingPaper_PathwaystoAnEliteEducation.pdf plots
	rm plots-000.png
	rm plots-001.png
	mv plots-002.png data/pre/percent-applying-and-receiving-offers.png

	touch data/flags/pre

data/flags/interim: data/flags/external \
					data/flags/raw \
					data/flags/pre \
					 src/data/interim/zip_to_borough.py
	python -m src.data.interim.zip_to_borough 'data/interim/zip_to_borough.pkl'
	touch data/flags/interim

data/flags/process: data/flags/external \
					data/flags/raw \
					data/flags/pre \
					data/flags/interim \
					 src/data/process/schools2017.py
	python -m src.data.process.schools2017 'data/pre/schools_demographics.pkl' 'data/pre/test_results.pkl' 'data/pre/nyt_table.pkl' 'data/process/schools2017.pkl'
	touch data/flags/process

.PHONY: notebooks
notebooks:
	jupyter nbconvert --output-dir='notebooks/html' --to=html "notebooks/*.ipynb"
