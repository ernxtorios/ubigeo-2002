import sys
import pipelinebronze as pb
import pipelinesilver as ps
import pipelinegold as pg


class Pipeline():
    def __init__(self):
        try:
            if len(sys.argv) > 1:
                self.layer = sys.argv[1].strip().upper()
                print(f"Argument layer: {self.layer}")
            else:
                print("No argument was provided.")
        except Exception as e:
            print(f"Error, no argument was provided: {e}")
            
    def validate_layer(self):
        """
        Throws an ValueError if the layer argument is not included or is not correct.
        """
        if self.layer not in ["BRONZE", "SILVER", "GOLD"]:
            raise ValueError("The layer argument is not correct.")

    def execute_pipeline(self):
        try:
            self.validate_layer()

            if self.layer.strip().upper() == "BRONZE":
                pipeline_bronze = pb.PipelineBronze()

                pipeline_bronze.extracting()

                pipeline_bronze.loading(True)

                pipeline_bronze.exiting()
            elif self.layer.strip().upper() == "SILVER":
                pipeline_silver = ps.PipelineSilver()

                pipeline_silver.extracting()

                pipeline_silver.transforming()

                pipeline_silver.loading()

                pipeline_silver.exiting()
            elif self.layer.strip().upper() == "GOLD":
                pipeline_gold = pg.PipelineGold()

                pipeline_gold.extracting()

                pipeline_gold.transforming()

                pipeline_gold.loading()
                
                pipeline_gold.exiting() 
            print("The pipeline was executed successfully.")
        except ValueError as e1:
            print(f"Error in layer argument: {e1}")
        except Exception as e2:
            print(f"Error in layer argument: {e2}")


if __name__ == "__main__":
    pipeline = Pipeline()

    pipeline.execute_pipeline()

