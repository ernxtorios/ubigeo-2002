from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType
from .config import PROJECT_NAME, HDFS_PATH_BRONZE, HDFS_PATH_SILVER, HDFS_PATH_GOLD, PREFIX_BRONZE, PREFIX_SILVER, PREFIX_GOLD


class Load():
    def validate_list(self, list_object):
        """
        Throws an ValueError if list_object is not a list or is empty.

        Args:
            list_object: The object list.
        """
        if not isinstance(list_object, list):
            raise ValueError("The object is not a list.")

        if (isinstance(list_object, list) and len(list_object) == 0):
            raise ValueError("The list is empty.")
            
    def create_database(self, spark: SparkSession):
        """
        Create a database in Hive metastore.
        
        Args:
            spark (SparkSession): The SparkSession object. The name of the database is the name of the project.
        """
        try:
            spark.sql(f"DROP DATABASE IF EXISTS {PROJECT_NAME} CASCADE;")
            
            spark.sql(f"CREATE DATABASE IF NOT EXISTS {PROJECT_NAME};")
    
            print(f"The database {PROJECT_NAME} was created.")
        except Exception as e:
            print(f"Error creating database: {e}")

    def create_external_table_with_partition(self,
                                        layer,
                                        dataframe: DataFrame,
                                        table_name,
                                        partition_by,
                                        mode="overwrite",
                                        format="parquet"):
        """
        Create an external table, with partition, in the Hive metastore.
        
        Args:
            layer (str): One of the layers of medallion architecture (bronze, silver, gold)
            dataframe (DataFrame): The DataFrame object.
            table_name (str): The name of the table.
            partition_by (str): A list of partition fields by which the table will be partitioned.
            mode (str): Table writing mode (overwrite, append, ignore, error). Optional. Overwrite default.
            format (str): Table format. Optional. Parquet default.
        """
        try:
            self.validate_list(partition_by)

            if layer.upper() == "BRONZE":
                external_location = HDFS_PATH_BRONZE + table_name + "/external/"
                external_table = PROJECT_NAME + "." + PREFIX_BRONZE + table_name
            elif layer.upper() == "SILVER":
                external_location = HDFS_PATH_SILVER + table_name + "/external/"
                external_table = PROJECT_NAME + "." + PREFIX_SILVER + table_name
            elif layer.upper() == "GOLD":
                external_location = HDFS_PATH_GOLD + table_name + "/external/"
                external_table = PROJECT_NAME + "." + PREFIX_GOLD + table_name

            (
                dataframe
                .write
                .partitionBy(partition_by)
                .mode(mode)
                .format(format)
                .option("path", external_location)
                .saveAsTable(external_table, external=True)
            )

            print(f"The table {external_table} was created.")
        except ValueError as e1:
            print(f"Error: {e1}")
        except Exception as e2:
            print(f"Error creating the external table: {e2}")

    def create_external_table_without_partition(self,
                                                layer,
                                                dataframe: DataFrame,
                                                table_name,
                                                mode="overwrite",
                                                format="parquet"):
        """
        Create an external table, without partition, in the Hive metastore.
        
        Args:
            layer (str): One of the layers of medallion architecture (bronze, silver, gold)
            dataframe (DataFrame): The DataFrame object.
            table_name (str): The name of the table.
            mode (str): Table writing mode (overwrite, append, ignore, error). Optional. Overwrite default.
            format (str): Table format. Optional. Parquet default.
        """
        try:
            if layer.upper() == "BRONZE":
                external_location = HDFS_PATH_BRONZE + table_name + "/external/"
                external_table = PROJECT_NAME + "." + PREFIX_BRONZE + table_name
            elif layer.upper() == "SILVER":
                external_location = HDFS_PATH_SILVER + table_name + "/external/"
                external_table = PROJECT_NAME + "." + PREFIX_SILVER + table_name
            elif layer.upper() == "GOLD":
                external_location = HDFS_PATH_GOLD + table_name + "/external/"
                external_table = PROJECT_NAME + "." + PREFIX_GOLD + table_name

            (
                dataframe
                .write
                .mode(mode)
                .format(format)
                .option("path", external_location)
                .saveAsTable(external_table, external=True)
            )

            print(f"The table {external_table} was created.")
        except Exception as e:
            print(f"Error creating the external table: {e}")

