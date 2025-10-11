from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from extractors.extractor import Extract
from loaders.loader import Load
from transformers.transformer import Transform


class PipelineBronze():
    def __init__(self):
        self.layer = "BRONZE"
        
        self.spark = SparkSession.builder.appName("UBIGEO2002-BRONZE").master("local[*]").enableHiveSupport().getOrCreate()

        self.schema_ccpp2002 = StructType(
            [
                StructField("CCDD", StringType(), True),
                StructField("NOMBREDD", StringType(), True), 
                StructField("CCPP", StringType(), True), 
                StructField("NOMBREPV", StringType(), True),
                StructField("CCDI", StringType(), True), 
                StructField("NOMBREDI", StringType(), True), 
                StructField("CODCCPP02", StringType(), True), 
                StructField("NOMCCPP02", StringType(), True), 
                StructField("CLASIFCCPP", StringType(), True), 
                StructField("P02_06", IntegerType(), True), 
                StructField("CATCCPP02", StringType(), True), 
                StructField("NOMCAT02", StringType(), True)
            ]
        )

        self.schema_ubigeo2002 = StructType(
            [
                StructField("CODDPTO", StringType(), True),
                StructField("CODPROV", StringType(), True), 
                StructField("CODDIST", StringType(), True), 
                StructField("NOMBRE", StringType(), True)
            ]
        )

        self.dict_dataframes = {
            "ccpp2002": None,
            "ubigeo2002": None
        }
    
    def extracting(self):
        try:
            extractor = Extract()
    
            list_dbf_files = ["/mnt/d/DatabasesProjects/Databases/ubigeo/ubigeo2002.DBF",
                              "/mnt/d/DatabasesProjects/Databases/ubigeo/ccpp2002.DBF"]
    
            linux_path_dbf_files = "/home/ernestosegundo/projects/ubigeo/data/"
    
            for dbf_file in list_dbf_files:
                extractor.copy_datasources_files(dbf_file, linux_path_dbf_files)
    
            dict_dbf_csv_files = {
                "/home/ernestosegundo/projects/ubigeo/data/ccpp2002.DBF": "/home/ernestosegundo/projects/ubigeo/data/ccpp2002.csv",
                "/home/ernestosegundo/projects/ubigeo/data/ubigeo2002.DBF": "/home/ernestosegundo/projects/ubigeo/data/ubigeo2002.csv"
            }
    
            for key, value in dict_dbf_csv_files.items():
                extractor.create_csv_from_dbf(key, value)
    
            list_schemas = [self.schema_ccpp2002, self.schema_ubigeo2002]
            dict_csv_schema = dict(zip(dict_dbf_csv_files.values(), list_schemas))
    
            list_dataframes = list()
            for key, value in dict_csv_schema.items():
                list_dataframes.append(extractor.dataframe_from_csv(self.spark, key, value))
    
            self.dict_dataframes = dict(zip(self.dict_dataframes.keys(), list_dataframes))
    
            return self.dict_dataframes
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None

    def transforming(self):
        pass

    def loading(self, create_database=False):
        try:
            loader = Load()
            
            if create_database:
                loader.create_database(self.spark)
    
            for table, dataframe in self.dict_dataframes.items():
                loader.create_external_table_without_partition(
                    self.layer,
                    dataframe,
                    table
                )
                print("Table was loaded.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def exiting(self):
        try:
            self.spark.stop()

            print(f"Pipeline {self.layer} was successfully executed.")
        except Exception as e:
            print(f"Error exiting pipeline bronze: {e}")

