from dbfread import DBF
import csv
import subprocess
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from .config import USER_SERVER_ORIGIN, SSH_PORT_ORIGIN, SERVER_DESTINATION, PROJECT_NAME


class Extract():
    def copy_datasources_files(self, source_files_path, destination_files_path):
        """
        Copying files from Windows to Linux
        
        Args:
            source_files_path (str): The full path to the input files.
            destination_files_path (str): The full path to the output files.
        
        Using WSL, we copy the data source files to the cluster's master node.

        Source Files (Windows):
            Example:
            /mnt/d/DatabasesProjects/Databases/ubigeo/ubigeo2002.DBF
            /mnt/d/DatabasesProjects/Databases/ubigeo/ccpp2002.DBF
        
        Destination Files (Linux):
            Example:
            /home/ernestosegundo/projects/ubigeo/data/
        """    
        try:
            server_destination_files_colon = SERVER_DESTINATION + ":" + destination_files_path
            cmd = ["ssh", USER_SERVER_ORIGIN, "-p", SSH_PORT_ORIGIN, "scp", source_files_path, server_destination_files_colon]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8")

            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Error output: {e.stderr}")
            return None


    def create_csv_from_dbf(self, dbf_file_path, csv_file_path):
        """
        Create a CSV file from a DBF file.

        Args:
            dbf_file_path (str): The full path to the input DBF file.
            csv_file_path (str): The full path to the output CSV file.
        """
        try:
            table = DBF(dbf_file_path)

            with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(table.field_names)

                for record in table:
                    writer.writerow(list(record.values()))
            
            print(f"Successfully created '{csv_file_path}' from '{dbf_file_path}'")
        except Exception as e:
            print(f"Error creating CSV from DBF: {e}")


    def dataframe_from_csv(self, spark: SparkSession, file_path, schema: StructType):
        """
        Get a Spark dataframe from a CSV file on the Linux file system.
        
        Args:
            spark (SparkSession): The SparkSession object.
            file_path (str): The full path to the input CSV file.
            schema (StructType): The definition of the expected dataframe schema.
        """
        try:
            df = spark.read.csv("file://" + file_path, header=True, schema=schema)

            print(f"Data extracted successfully from {file_path}.")

            return df
        except Exception as e:
            print(f"Error getting dataframe: {e}")
            return None

    def dataframe_from_table(self, spark: SparkSession, table_name):
        """
        Returns a dataframe from a table of the database
        
        Args:
            spark (SparkSession): The SparkSession object.
            table_name (str): The name of the database table.
        """
        try:
            database_table = PROJECT_NAME + "." + table_name
            df_from_table = spark.read.table(database_table)
    
            return df_from_table
        except Exception as e:
            print(f"Error getting dataframe: {e}")
            return None

