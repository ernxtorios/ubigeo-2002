from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType
from .config import PROJECT_NAME


class Transform():
    def get_country_2002(self, spark: SparkSession, dataframe: DataFrame):
        """
        Returns a dataframe with the country (Peru)
        
        Args:
            spark (SparkSession): The SparkSession object.
            dataframe (DataFrame): The DataFrame object.
        """
        try:
            df_pais = dataframe \
            .filter("CODDPTO == 0") \
            .filter("CODPROV == 0") \
            .filter("CODDIST == 0") \
            .select("CODDPTO", "NOMBRE") \
            .orderBy("CODDPTO")
    
            return df_pais
        except Exception as e:
            print(f"Error getting dataframe of country: {e}")
            return None
    
    def get_departments_2002(self, spark: SparkSession, dataframe: DataFrame):
        """
        Returns a dataframe with the departments of Peru
        
        Args:
            spark (SparkSession): The SparkSession object.
            dataframe (DataFrame): The DataFrame object.
        """
        try:
            df_departamentos = dataframe \
            .filter("CODDPTO != 0") \
            .filter("CODPROV == 0") \
            .filter("CODDIST == 0") \
            .select("CODDPTO", "NOMBRE") \
            .orderBy("CODDPTO")
    
            return df_departamentos
        except Exception as e:
            print(f"Error getting dataframe of departments: {e}")
            return None

    def get_provinces_2002(self, spark: SparkSession, dataframe: DataFrame):
        """
        Returns a dataframe with the provinces of Peru
        
        Args:
            spark (SparkSession): The SparkSession object.
            dataframe (DataFrame): The DataFrame object.
        """
        try:
            df_provincias = dataframe \
            .filter("CODDPTO != 0") \
            .filter("CODPROV != 0") \
            .filter("CODDIST == 0") \
            .select("CODDPTO", "CODPROV", "NOMBRE") \
            .orderBy("CODDPTO", "CODPROV")
    
            return df_provincias
        except Exception as e:
            print(f"Error getting dataframe of provinces: {e}")
            return None 

    def get_districts_2002(self, spark: SparkSession, dataframe: DataFrame):
        """
        Returns a dataframe with the districts of Peru
        
        Args:
            spark (SparkSession): The SparkSession object.
            dataframe (DataFrame): The DataFrame object.
        """
        try:
            df_distritos = dataframe \
            .filter("CODDPTO != 0") \
            .filter("CODPROV != 0") \
            .filter("CODDIST != 0") \
            .select("CODDPTO", "CODPROV", "CODDIST", "NOMBRE") \
            .orderBy("CODDPTO", "CODPROV", "CODDIST")
    
            return df_distritos
        except Exception as e:
            print(f"Error getting dataframe of districts: {e}")
            return None

    def get_ccpp_2002(self, spark: SparkSession, dataframe: DataFrame):
        """
        Returns a dataframe with the ccpp of Peru
        
        Args:
            spark (SparkSession): The SparkSession object.
            dataframe (DataFrame): The DataFrame object.
        """
        try:
            df_ccpp2002 = dataframe \
            .select("CCDD",
                    "CCPP",
                    "CCDI",
                    "CODCCPP02",
                    "NOMCCPP02",
                    "CLASIFCCPP",
                    "P02_06",
                    "CATCCPP02") \
            .orderBy("CCDD", "CCPP", "CCDI", "CODCCPP02")

            df_ccpp2002 = df_ccpp2002 \
            .withColumnRenamed("CCDD", "CODDPTO") \
            .withColumnRenamed("CCPP", "CODPROV") \
            .withColumnRenamed("CCDI", "CODDIST") \
            .withColumnRenamed("CODCCPP02", "CODCCPP") \
            .withColumnRenamed("NOMCCPP02", "NOMCCPP") \
            .withColumnRenamed("P02_06", "NUMVVDA") \
            .withColumnRenamed("CATCCPP02", "CATCCPP") \
            .orderBy("CODDPTO", "CODPROV", "CODDIST", "CODCCPP")
    
            return df_ccpp2002
        except Exception as e:
            print(f"Error getting dataframe of ccpp: {e}")
            return None

    def get_categories_2002(self, spark: SparkSession, dataframe: DataFrame):
        """
        Returns a dataframe with the categiories ccpp of Peru
        
        Args:
            spark (SparkSession): The SparkSession object.
            dataframe (DataFrame): The DataFrame object.
        """
        try:    
            df_categorias = dataframe \
            .select("CATCCPP02",
                    "NOMCAT02") \
            .distinct() \
            .orderBy("CATCCPP02")

            df_categorias = df_categorias \
            .withColumnRenamed("CATCCPP02", "CATCCPP") \
            .withColumnRenamed("NOMCAT02", "NOMCAT") \
            .orderBy("CATCCPP")
    
            return df_categorias
        except Exception as e:
            print(f"Error getting dataframe of categories: {e}")
            return None

