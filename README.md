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

1. Copy Entire Folder Structure to local
2. Update **Config.py** with path updates
3. run **/Scripts/ETL/FullLoad.py** to do a initial load
4. run **crontab crontab** to schedule daily load
5. run **/Scripts/API/app.py** to spin up Flask Webserver
6. run **/TestAPI/RunTestCases.py** to test the Flask API Endpoint
