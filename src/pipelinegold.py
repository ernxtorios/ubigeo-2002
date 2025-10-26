from pyspark.sql import SparkSession
from extractors.extractor import Extract
from loaders.loader import Load
from transformers.transformer import Transform


class PipelineGold():
    def __init__(self):
        self.layer = "GOLD"
        
        self.spark = SparkSession.builder.appName("UBIGEO2002-GOLD").master("local[*]").enableHiveSupport().getOrCreate()

        self.df_silver_departamentos2002 = None
        self.df_silver_provincias2002 = None

        self.df_departamentos_capitales_provincias2002 = None
        self.df_departamentos_provincias_distritos2002 = None
    
    def extracting(self):
        try:
            extractor = Extract()
    
            self.df_silver_departamentos2002 = extractor.dataframe_from_table(self.spark, "silver_departamentos2002")
            self.df_silver_provincias2002 = extractor.dataframe_from_table(self.spark, "silver_provincias2002")
        except Exception as e:
            print(f"Error extracting data: {e}")

    def transforming(self):
        try:
            transformer = Transform()
    
            self.df_departamentos_capitales_provincias2002 = (
                transformer.get_departamentos_capitales_provincias_2002(
                    self.spark, 
                    self.df_silver_departamentos2002,
                    self.df_silver_provincias2002
                )
            )
        except Exception as e:
            print(f"Error transforming data: {e}")

    def loading(self, create_database=False):
        try:
            loader = Load()
             
            loader.create_external_table_without_partition(
                self.layer,
                self.df_departamentos_capitales_provincias2002,
                "departamentos_capitales_cantidad_provincias2002"
            )
            print("Table was loaded.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def exiting(self):
        try:
            self.spark.stop()

            print(f"Pipeline {self.layer} was successfully executed.")
        except Exception as e:
            print(f"Error exiting pipeline gold: {e}")

