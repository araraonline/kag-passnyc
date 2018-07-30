DEMOGRAPHICS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/demographicsnapshot201314to201718public_final.xlsx'
QUALITY_REPORT_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/2016-17-elementary-middle-school-quality-report.xlsx?sfvrsn=8128a743_4'
ELA_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/school-ela-results-2013-2017-public.xlsx'
MATH_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/school-math-results-2013-2017-public.xlsx'
CHARTER_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/charter-school-results-2013-2017-public.xlsx'

ARTICLE_URL = 'https://steinhardt.nyu.edu/scmsAdmin/media/users/sg158/PDFs/Pathways_to_elite_education/WorkingPaper_PathwaystoAnEliteEducation.pdf'


all: data/flags/raw \
	 data/flags/pre \
	 data/flags/interim \
	 data/flags/process \
	 data/flags/output

data/flags/raw: src/data/raw/nyt_table.py
	kaggle datasets download -d passnyc/data-science-for-good -p data/raw
	kaggle kernels output -k araraonline/retrieve-school-boroughs -p data/raw

	python -m src.util.download $(ARTICLE_URL) 'data/raw/PathwaystoAnEliteEducation.pdf'
	python -m src.util.download $(DEMOGRAPHICS_URL) 'data/raw/demographics_snapshot_20132017.xlsx'
	python -m src.util.download $(QUALITY_REPORT_URL) 'data/raw/quality_report_20162017.xlsx'
	python -m src.util.download $(ELA_RESULTS_URL) 'data/raw/ela_results_20132017.xlsx'
	python -m src.util.download $(MATH_RESULTS_URL) 'data/raw/math_results_20132017.xlsx'
	python -m src.util.download $(CHARTER_RESULTS_URL) 'data/raw/charter_results_20132017.xlsx'
	python -m src.data.raw.nyt_table 'data/raw/nyt_table.csv'

	touch data/flags/raw

data/flags/pre: data/flags/raw \
				 src/data/pre/schools2016.py \
				 src/data/pre/schools_demographics.py \
				 src/data/pre/test_results.py \
				 src/data/pre/nyt_table.py
	python -m src.data.pre.schools2016 'data/raw/2016 School Explorer.csv' 'data/pre/schools2016.pkl'
	python -m src.data.pre.schools_demographics 'data/raw/demographics_snapshot_20132017.xlsx' 'data/pre/schools_demographics.pkl'
	python -m src.data.pre.test_results 'data/raw/ela_results_20132017.xlsx' 'data/raw/math_results_20132017.xlsx' 'data/raw/charter_results_20132017.xlsx' 'data/pre/test_results.pkl'
	python -m src.data.pre.nyt_table 'data/raw/nyt_table.csv' 'data/pre/nyt_table.pkl'

	touch data/flags/pre

data/flags/interim: data/flags/raw \
					data/flags/pre

	touch data/flags/interim

data/flags/process: data/flags/raw \
					data/flags/pre \
					data/flags/interim \
					 src/data/process/schools2017.py
	python -m src.data.process.schools2017 'data/pre/schools_demographics.pkl' 'data/pre/test_results.pkl' 'data/pre/nyt_table.pkl' 'data/process/schools2017.pkl'

	touch data/flags/process

data/flags/output: data/flags/raw \
				   data/flags/pre \
				   data/flags/interim \
				   data/flags/process
	pdfimages -png -f 22 -l 22 'data/raw/PathwaystoAnEliteEducation.pdf' plots
	rm plots-000.png
	rm plots-001.png
	mv plots-002.png 'data/output/shsat_offers_by_grade.png'

	touch data/flags/output

.PHONY: notebooks
notebooks:
	jupyter nbconvert --output-dir='notebooks/html' --to=html "notebooks/*.ipynb"
