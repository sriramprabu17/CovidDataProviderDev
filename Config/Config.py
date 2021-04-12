import os
cwd = os.path.abspath(os.getcwd())
#cwd = cwd[:-7]

srcCountyCaseCnt = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
srcCountyPopulation = "https://www2.census.gov/programs-surveys/popest/tables/2010-2019/counties/totals/co-est2019-annres.xlsx"
srcCountyZip = cwd + "/Data/SRC/COUNTY_ZIP_122020.xlsx"

DB = cwd + '/Data/DB/DataAPI.db'

RAW_PATH = cwd + '/Data/RAW'
STG_PATH = cwd + '/Data/STG'

TC_PATH = cwd + '/TestAPI/TestCases.json'