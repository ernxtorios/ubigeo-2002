from pyspark.sql import SparkSession
from extractors.extractor import Extract
from loaders.loader import Load
from transformers.transformer import Transform


class PipelineGold():
    def __init__(self):
        self.layer = "GOLD"
        
        self.spark = SparkSession.builder.appName("UBIGEO2002-GOLD").master("local[*]").enableHiveSupport().getOrCreate()
    
    def extracting(self):
        try:
            pass
        except Exception as e:
            print(f"Error extracting data: {e}")

    def transforming(self):
        try:
            pass
        except Exception as e:
            print(f"Error transforming data: {e}")

    def loading(self, create_database=False):
        try:
            pass
        except Exception as e:
            print(f"Error loading data: {e}")

    def exiting(self):
        try:
            self.spark.stop()

            print(f"Pipeline {self.layer} was successfully executed.")
        except Exception as e:
            print(f"Error exiting pipeline gold: {e}")

