# CovidDataProviderDev
 
Installation Instructions
============================

### Folder Structure

    CovidDataAPI
    ├── Config                  # Config for Src and Pickle Files
    ├── crontab                 # Cron Scheduler for DailyLoads  
    ├── Data                    ## Data Files 
         ├── SRC                     # Source files County ZIP File
         ├── RAW                     # Landing Layer Pickle for Files Downloaded 
         ├── STG                     # Staging Layer Pickle File for Transformed Data
         ├── DB                      
             ├── DataAPI.db          # Model and Serve DB
    ├── Scripts                    ## Sripts fot ETL and API 
            ├── ETL                   
                 ├── ETLWrap.py       # Wrapper for Extract, Transform and Load (Initial and Incremental Loads)
                 ├── FullLoad.py      # Initial Setups and Full Load Historical Data
                 ├── DailyLoad.py     # Incrementaly Load Missing Data
            ├── API                   
                 ├── app.py           # Python for Building API using Flask with Validations
    ├── TestAPI                   ## Automated TestScript
            ├── TestCases.json                   # Json File with Test Cases for API
            ├── RunTestCases.py                   # Test Case Executor
    ├── LICENSE
    ├── dockerfile
    └── README.md
    

> Use short lowercase names at least for the top-level files and folders except
> `LICENSE`, `README.md`

### Prerequisites
1. Python 
2. Pandas
3. Flask
4. SQLite

### Installation Instructions

Using the Folder
1. Copy Entire Folder Structure to local ./CovidDataProvider/
2. Build Docker image 
3. Run the Docker Image
4. Goto Local Host:5000
5. API Usage  **Local Host:5000?<ZIPCODE>?StartDate=YYYY-MM-DD&EndDate=YYYY-MM-DD**

## API Testing

1. Open Docker Container 
2. Run **./TestAPI/RunTestCases.py**
3. This will execute Testcases in Json File TestCases.json

### API Test Cases 
1. Ping Test
2. Sanity Test Data for one ZIP & Date
3. Invalid ZIP Code
4. Invalid Start Date 
5. Invalid End Date

#### To be added - Not Handled in API
1.Missind Data for a ZIP/Date

## Data Model
**FactCovidCounts
  |- LkpZipCode 
