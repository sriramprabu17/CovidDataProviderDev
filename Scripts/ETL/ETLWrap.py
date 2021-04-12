from CovidDataProvider.Config import Config
import pandas as pd

import sqlite3
import requests


class DataPipeline():

    
    def ExtractData():
    #Read Data
        try:
            raw_CountyCaseCnt = pd.read_csv(Config.srcCountyCaseCnt)
            raw_CountyPopulation = pd.read_excel(Config.srcCountyPopulation,header = 3)
            raw_CountyZip = pd.read_excel(Config.srcCountyZip)
        except requests.exceptions.RequestException as e:
                        print('Failed to extract files: exception {}'.format(e))
            
        pd.to_pickle(raw_CountyCaseCnt,'{}/raw_CountyCaseCnt.pkl'.format(Config.RAW_PATH))
        pd.to_pickle(raw_CountyPopulation,'{}/raw_CountyPopulation.pkl'.format(Config.RAW_PATH))
        pd.to_pickle(raw_CountyZip,'{}/raw_CountyZip.pkl'.format(Config.RAW_PATH))
        print("Completed Read Data")
        
    def TransformData():
        raw_CountyCaseCnt = pd.read_pickle('{}/raw_CountyCaseCnt.pkl'.format(Config.RAW_PATH))
        raw_CountyPopulation = pd.read_pickle('{}/raw_CountyPopulation.pkl'.format(Config.RAW_PATH))
        raw_CountyZip = pd.read_pickle('{}/raw_CountyZip.pkl'.format(Config.RAW_PATH))
        #Cleanse Case Count Data

        #unpivot to convert Dates from Columns to Rows and Remove unused Columns. 
        dates = raw_CountyCaseCnt.columns[11:]
        STG_CountyCaseCnt = raw_CountyCaseCnt.melt(
                                                        id_vars=[
                                                            #'UID',
                                                       # 'iso2',
                                                       # 'iso3',
                                                       # 'code3',
                                                        'FIPS',
                                                       # 'Admin2',
                                                       # 'Province_State',
                                                       # 'Country_Region',
                                                       # 'Lat',
                                                       # 'Long_',
                                                        'Combined_Key'],
                                                        value_vars=dates, 
                                                        var_name='Date', 
                                                        value_name='EstimatedCnt')
        #Rename Columns
        STG_CountyCaseCnt.rename( {"Combined_Key": "County"} , axis = 'columns',inplace = True)

        #Remove US from County to Match with CountyPopulation DataSet
        STG_CountyCaseCnt["County"] = STG_CountyCaseCnt["County"].replace(', US', '', regex=True)

        #Clean FIPS Data to match County to ZIP
        STG_CountyCaseCnt["FIPS"]= STG_CountyCaseCnt["FIPS"].fillna(-1).astype(int)

        #Convert Date to Date
        STG_CountyCaseCnt['Date'] = pd.to_datetime(STG_CountyCaseCnt['Date'],infer_datetime_format = True)


        # Cleanse Population Data
        #Take 2019 Population
        STG_CountyPopulation = raw_CountyPopulation[["Unnamed: 0","Estimates Base","Census",2019]][1:3143]

        #Rename Columns
        STG_CountyPopulation.rename( {"Unnamed: 0": "County",2019:"PopulationCnt"} , axis = 'columns',inplace = True)

        #Cleanse County Data to Match with 
        STG_CountyPopulation["County"] = STG_CountyPopulation["County"].replace(' County,', ',', regex=True).replace('\.','', regex=True)

        #Drop Unused Columns
        STG_CountyPopulation.drop(columns={ 'Estimates Base','Census'},inplace=True)

        # Cleanse Population Data
        STG_CountyZip = raw_CountyZip.drop(columns={ 'BUS_RATIO','OTH_RATIO','TOT_RATIO'})
        STG_CountyZip=STG_CountyZip.rename(columns = {"COUNTY":"FIPS2"})

        # Merge Covid Data and Population
        STG_CountyCasePopulation = pd.merge(STG_CountyCaseCnt, STG_CountyPopulation, how="left", on=["County", "County"])
        
        pd.to_pickle(STG_CountyCasePopulation,'{}/CountyCasePopulation.pkl'.format(Config.STG_PATH))
        pd.to_pickle(STG_CountyZip,'{}/CountyZip.pkl'.format(Config.STG_PATH))
        
        print("Completed Transform  Data")
        
    def FullLoadData():
        STG_CountyCasePopulation = pd.read_pickle('{}/CountyCasePopulation.pkl'.format(Config.STG_PATH))
        STG_CountyZip = pd.read_pickle('{}/CountyZip.pkl'.format(Config.STG_PATH))
        #Load Full Load Data
        conn = sqlite3.connect(Config.DB)
        c = conn.cursor() 
        c.execute("Drop table If exists FactCovidCounts")
        c.execute("Drop table If exists LkpZip")

        print(Config.DB)

        STG_CountyCasePopulation.to_sql("FactCovidCounts",conn)
        STG_CountyZip.to_sql("LkpZip",conn)

        c.execute("Create index ix_FactCovidCounts ON FactCovidCounts (county,Date);")
        c.execute("create index ix_lkp on LkpZip(FIPS2);")

        conn.commit()
        c.close()
        conn.close()
        
                
        print("Full Data Load Completed")
    
    def IncrementalLoadData():
        STG_CountyCasePopulation = pd.read_pickle('{}/CountyCasePopulation.pkl'.format(Config.STG_PATH))
        #Load Full Load Data
        conn = sqlite3.connect(Config.DB)
        c = conn.cursor() 
        
        results = c.execute("Select max(Date) from FactCovidCounts")
        for row in results:
            maxDate = row[0]
        STG_CountyCasePopulation = STG_CountyCasePopulation[STG_CountyCasePopulation["Date"]> maxDate]
        
        STG_CountyCasePopulation.to_sql("FactCovidCounts",conn,if_exists='append')
        
        conn.commit()
        c.close()
        conn.close()
        print("Incremental Data Load Completed")

