from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType
from pyspark.sql.functions import col, count
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

    def get_capitales_departamento_2002(self, spark: SparkSession, dataframe_1: DataFrame, dataframe_2: DataFrame):
        """
        Returns a dataframe with the department capitals of Peru
        
        Args:
            spark (SparkSession): The SparkSession object.
            dataframe_1 (DataFrame): The DataFrame object.
            dataframe_2 (DataFrame): The DataFrame object.
        """
        try:
            df_capitales_departamento2002 = (
                dataframe_1.alias("d").join(dataframe_2.alias("p"), "coddpto")
                .select(col("d.coddpto").alias("codigo_departamento"),
                        col("d.nombre").alias("departamento"),
                        col("p.nombre").alias("capital"))
                .where("codprov = '01'")
                .orderBy("codigo_departamento")
            )
    
            return df_capitales_departamento2002
        except Exception as e:
            print(f"Error getting dataframe of the department capitals: {e}")
            return None

    def get_cantidad_provincias_departamento_2002(self, spark: SparkSession, dataframe_1: DataFrame, dataframe_2: DataFrame):
        """
        Returns a dataframe with the number of provinces per department of Peru
        
        Args:
            spark (SparkSession): The SparkSession object.
            dataframe_1 (DataFrame): The DataFrame object.
            dataframe_2 (DataFrame): The DataFrame object.
        """
        try:
            df_cantidad_provincias_departamento2002 = (
                dataframe_1.alias("d").join(dataframe_2.alias("p"), "coddpto")
                .groupby("d.coddpto")
                .agg(count("p.codprov").alias("cantidad_provincias"))
                .select(col("coddpto").alias("codigo_departamento"), "cantidad_provincias")
                .orderBy("codigo_departamento")
            )
    
            return df_cantidad_provincias_departamento2002
        except Exception as e:
            print(f"Error getting dataframe of the department capitals: {e}")
            return None

    def get_departamentos_capitales_provincias_2002(self, spark: SparkSession, dataframe_1: DataFrame, dataframe_2: DataFrame):
        """
        Returns a dataframe with the number of provinces per department of Peru
        
        Args:
            spark (SparkSession): The SparkSession object.
            dataframe_1 (DataFrame): The DataFrame object.
            dataframe_2 (DataFrame): The DataFrame object.
        """
        try:
            df_capitales_departamento2002 = self.get_capitales_departamento_2002(spark, dataframe_1, dataframe_2)
            df_cantidad_provincias_departamento2002 = self.get_cantidad_provincias_departamento_2002(spark, dataframe_1, dataframe_2)
            
            df_departamentos_capitales_provincias2002 = (
                df_capitales_departamento2002.join(df_cantidad_provincias_departamento2002, "codigo_departamento")
                .select("*")
                .orderBy("codigo_departamento")
            )
    
            return df_departamentos_capitales_provincias2002
        except Exception as e:
            print(f"Error getting dataframe of the department capitals and provinces: {e}")
            return None
