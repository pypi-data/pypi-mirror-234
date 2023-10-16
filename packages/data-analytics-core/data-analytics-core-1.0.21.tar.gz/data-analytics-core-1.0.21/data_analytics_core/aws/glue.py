"""
AWS_Glue Class
Class containing all the needed AWS Glue service elements, actions and the client itself.
"""
import os
import boto3
from botocore.exceptions import ClientError
# custom imports
from data_analytics_core.local_stack.boto_client_moks.localstack_clients import boto3_client_localstack


class AmazonWebServicesGlue:

    def __init__(self, region_name="eu-central-1"):
        # env aws connections generation
        self.region_name = region_name
        if os.getenv("LOCALSTACK_ENDPOINT_URL"):
            self.glue_client = boto3_client_localstack(service_name="glue", region_name=self.region_name)
        else:
            self.glue_client = boto3.client('glue', region_name=self.region_name)

    def run_job(self, job_name, job_arguments):
        self.glue_client.start_job_run(JobName=job_name, Arguments=job_arguments)

    def get_job_status(self, job_name) -> str:
        try:
            job_run_id = self.glue_client.get_job_runs(JobName=job_name, MaxResults=1).get("JobRuns")[0].get("Id")
            status_detail = self.glue_client.get_job_run(JobName=job_name, RunId=job_run_id, PredecessorsIncluded=False)
            status = status_detail.get("JobRun").get("JobRunState")
            return status
        except ClientError as e:
            raise ClientError("boto3 client error in run_glue_job_get_status: " + e.__str__(),
                              operation_name="get_job_runs")
        except IndexError:
            return 'STOPPED'
        except Exception as e:
            raise Exception("Unexpected error in run_glue_job_get_status: " + e.__str__())
