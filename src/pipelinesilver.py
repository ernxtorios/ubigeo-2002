from pyspark.sql import SparkSession
from extractors.extractor import Extract
from loaders.loader import Load
from transformers.transformer import Transform


class PipelineSilver():
    def __init__(self):
        self.layer = "SILVER"
        
        self.spark = SparkSession.builder.appName("UBIGEO2002-SILVER").master("local[*]").enableHiveSupport().getOrCreate()

        self.df_bronze_ccpp2002 = None
        self.df_bronze_ubigeo2002 = None

        self.df_silver_pais2002 = None
        self.df_silver_departamentos2002 = None
        self.df_silver_provincias2002 = None
        self.df_silver_distritos2002 = None
        self.df_silver_ccpp2002 = None
        self.df_silver_categorias2002 = None
    
    def extracting(self):
        try:
            extractor = Extract()
    
            self.df_bronze_ccpp2002 = extractor.dataframe_from_table(self.spark, "bronze_ccpp2002")
            self.df_bronze_ubigeo2002 = extractor.dataframe_from_table(self.spark, "bronze_ubigeo2002")
        except Exception as e:
            print(f"Error extracting data: {e}")

    def transforming(self):
        try:
            transformer = Transform()
    
            self.df_silver_pais2002 = transformer.get_country_2002(self.spark, self.df_bronze_ubigeo2002)
            self.df_silver_departamentos2002 = transformer.get_departments_2002(self.spark, self.df_bronze_ubigeo2002)
            self.df_silver_provincias2002 = transformer.get_provinces_2002(self.spark, self.df_bronze_ubigeo2002)
            self.df_silver_distritos2002 = transformer.get_districts_2002(self.spark, self.df_bronze_ubigeo2002)
            self.df_silver_ccpp2002 = transformer.get_ccpp_2002(self.spark, self.df_bronze_ccpp2002)
            self.df_silver_categorias2002 = transformer.get_categories_2002(self.spark, self.df_bronze_ccpp2002)
        except Exception as e:
            print(f"Error transforming data: {e}")
            
    def loading(self):
        try:
            loader = Load()
             
            loader.create_external_table_without_partition(
                self.layer,
                self.df_silver_pais2002,
                "pais2002"
            )
            print("Table was loaded.")
             
            loader.create_external_table_without_partition(
                self.layer,
                self.df_silver_departamentos2002,
                "departamentos2002"
            )
            print("Table was loaded.")
             
            loader.create_external_table_with_partition(
                self.layer,
                self.df_silver_provincias2002,
                "provincias2002",
                ["CODDPTO"]
            )
            print("Table was loaded.")

            loader.create_external_table_with_partition(
                self.layer,
                self.df_silver_distritos2002,
                "distritos2002",
                ["CODDPTO", "CODPROV"]
            )
            print("Table was loaded.")
             
            loader.create_external_table_with_partition(
                self.layer,
                self.df_silver_ccpp2002,
                "centrospoblados2002",
                ["CODDPTO", "CODPROV", "CODDIST"]
            )
            print("Table was loaded.")

            loader.create_external_table_without_partition(
                self.layer,
                self.df_silver_categorias2002,
                "categorias2002"
            )
            print("Table was loaded.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def exiting(self):
        try:
            self.spark.stop()

            print(f"Pipeline {self.layer} was successfully executed.")
        except Exception as e:
            print(f"Error exiting pipeline silver: {e}")

