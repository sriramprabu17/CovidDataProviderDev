from CovidDataProvider.Scripts.ETL import ETLWrap

DP = ETLWrap.DataPipeline
DP.ExtractData()

DP.TransformData()

DP.FullLoadData()

#ETLWrap.DataPipeline.IncrementalLoadData()