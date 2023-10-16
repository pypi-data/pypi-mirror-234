"""
AWS_BatchJob Class
Class containing all the needed AWS Service Manager actions and the client itself.
"""
import os
import boto3
# custom imports
from data_analytics_core.logger.da_core_logger import da_logger
from data_analytics_core.local_stack.boto_client_moks.localstack_clients import boto3_client_localstack


class AmazonWebServicesBatchJobs:

    def __init__(self, region_name="eu-central-1", environment_default_parameters_dict: dict = None):
        # env aws connections generation
        self.region_name = region_name
        if os.getenv("LOCALSTACK_ENDPOINT_URL"):
            self.batch_client = boto3_client_localstack(service_name="batch", region_name=self.region_name)
        else:
            self.batch_client = boto3.client('batch')
        # custom variables
        self.environment_default_parameters_dict = environment_default_parameters_dict

    def run_batch_with_parameters(self):
        if self.environment_default_parameters_dict:
            response = self.batch_client.submit_job(
                jobName=self.environment_default_parameters_dict.get("job_name"),
                jobQueue=self.environment_default_parameters_dict.get("job_queue_name"),
                jobDefinition=self.environment_default_parameters_dict.get("job_definition_name"),
                propagateTags=True,
                timeout={"attemptDurationSeconds": int(self.environment_default_parameters_dict.get("batch_job_timeout"))},
            )
            da_logger.info(message=f"Batch Job started succesfully with:{da_logger.new_line()}"
                                    f"Job name:{response.get('jobName')}{da_logger.new_line()}"
                                    f"Job ID:{response.get('jobId')}")
        else:
            # TODO: change this to a try except
            da_logger.error("We have missing parameters!")

