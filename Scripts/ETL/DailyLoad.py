from CovidDataProvider.Scripts.ETL import ETLWrap

ETLWrap.DataPipeline.ExtractData()

ETLWrap.DataPipeline.TransformData()

#ETLWrap.DataPipeline.FullLoadData()

ETLWrap.DataPipeline.IncrementalLoadData()