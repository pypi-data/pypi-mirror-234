"""
AWS_SSM Class
Class containing all the needed AWS Service Manager actions and the client itself.
"""
import os
from typing import Optional
import json
import boto3

from data_analytics_core.local_stack.boto_client_moks.localstack_clients import boto3_client_localstack


class AmazonWebServicesSSM:

    def __init__(self, region_name="eu-central-1"):
        # env aws connections generation
        self.region_name = region_name
        if os.getenv("LOCALSTACK_ENDPOINT_URL"):
            self.ssm_client = boto3_client_localstack(service_name="ssm", region_name=region_name)
        else:
            self.ssm_client = boto3.client('ssm', region_name=region_name)

    def extract_param_value_as_dict(self, param_name: str) -> Optional[dict]:
        return eval(json.loads(json.dumps(self.ssm_client.get_parameter(Name=param_name)["Parameter"]["Value"])))

    def extract_param_value_as_string(self, param_name: str) -> Optional[str]:
        return self.ssm_client.get_parameter(Name=param_name)["Parameter"]["Value"]
