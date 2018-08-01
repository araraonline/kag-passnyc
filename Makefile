ELA_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/school-ela-results-2013-2017-public.xlsx?sfvrsn=1434547_2'
MATH_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/school-math-results-2013-2017-public.xlsx?sfvrsn=6bc91980_2'
CHARTER_RESULTS_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/charter-school-results-2013-2017-public.xlsx?sfvrsn=4988028b_2'
QUALITY_REPORT_URL = 'http://infohub.nyced.org/docs/default-source/default-document-library/2016-17-elementary-middle-school-quality-report.xlsx?sfvrsn=8128a743_4'

MIDDLE_SCHOOL_DIRECTORY_URL = 'https://data.cityofnewyork.us/api/views/6kcb-9g8d/rows.csv?accessType=DOWNLOAD'
SHSAT_TABLE_URL = 'https://data.cityofnewyork.us/api/views/vsgi-eeb5/rows.csv?accessType=DOWNLOAD'
SCHOOL_LOCATIONS_URL = 'https://data.cityofnewyork.us/api/views/p6h4-mpyy/rows.csv?accessType=DOWNLOAD'

ARTICLE_URL = 'https://steinhardt.nyu.edu/scmsAdmin/media/users/sg158/PDFs/Pathways_to_elite_education/WorkingPaper_PathwaystoAnEliteEducation.pdf'
BOROUGHS_GEOJSON_URL = 'https://raw.githubusercontent.com/dwillis/nyc-maps/master/boroughs.geojson'


all: data/flags/raw \
	 data/flags/pre \
	 data/flags/interim \
	 data/flags/process \
	 data/flags/output

data/flags/raw:
	kaggle datasets download -d passnyc/data-science-for-good -p data/raw
	kaggle kernels output -k araraonline/retrieve-school-boroughs -p data/raw

	python -m src.util.download $(ARTICLE_URL) 'data/raw/PathwaystoAnEliteEducation.pdf'
	python -m src.util.download $(BOROUGHS_GEOJSON_URL) 'data/raw/boroughs.geojson'
	python -m src.util.download $(QUALITY_REPORT_URL) 'data/raw/quality_report_20162017.xlsx'
	python -m src.util.download $(ELA_RESULTS_URL) 'data/raw/ela_results_20132017.xlsx'
	python -m src.util.download $(MATH_RESULTS_URL) 'data/raw/math_results_20132017.xlsx'
	python -m src.util.download $(CHARTER_RESULTS_URL) 'data/raw/charter_results_20132017.xlsx'
	python -m src.util.download $(MIDDLE_SCHOOL_DIRECTORY_URL) 'data/raw/middle_school_directory.csv'
	python -m src.util.download $(SHSAT_TABLE_URL) 'data/raw/shsat_table.csv'
	python -m src.util.download $(SCHOOL_LOCATIONS_URL) 'data/raw/school_locations_20172018.csv'

	touch data/flags/raw

data/flags/pre: data/flags/raw \
				 src/data/pre/schools2016.py \
				 src/data/pre/test_results.py \
				 src/data/pre/school_demographics_20162017.py \
				 src/data/pre/shsat_table.py \
				 src/data/pre/school_locations.py
	python -m src.data.pre.schools2016 'data/raw/2016 School Explorer.csv' 'data/pre/schools2016.pkl'
	python -m src.data.pre.middle_school_base 'data/raw/middle_school_directory.csv' 'data/pre/middle_school_base.pkl'
	python -m src.data.pre.shsat_table 'data/raw/shsat_table.csv' 'data/pre/shsat_table.pkl'
	python -m src.data.pre.school_demographics_20162017 'data/raw/quality_report_20162017.xlsx' 'data/pre/school_demographics_20162017.pkl'
	python -m src.data.pre.school_locations 'data/raw/school_locations_20172018.csv' 'data/raw/boroughs.geojson' 'data/pre/school_locations.pkl'
	python -m src.data.pre.test_results 'data/raw/ela_results_20132017.xlsx' 'data/raw/math_results_20132017.xlsx' 'data/raw/charter_results_20132017.xlsx' 'data/pre/test_results.pkl'

	touch data/flags/pre

data/flags/interim: data/flags/raw \
					data/flags/pre

	touch data/flags/interim

data/flags/process: data/flags/raw \
					data/flags/pre \
					data/flags/interim \
					 src/data/process/schools2017.py
	python -m src.data.process.schools2017 'data/pre/school_locations.pkl' 'data/pre/test_results.pkl' 'data/pre/shsat_table.pkl' 'data/pre/school_demographics_20162017.pkl' 'data/process/schools2017.pkl'

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
