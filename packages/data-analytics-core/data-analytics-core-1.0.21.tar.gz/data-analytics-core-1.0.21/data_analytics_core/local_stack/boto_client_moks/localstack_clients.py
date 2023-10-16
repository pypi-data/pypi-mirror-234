import os
import boto3


def boto3_client_localstack(service_name: str, region_name: str = "eu-central-1") -> boto3.session.Session.client:
    """
    boto3 client for setup environment
    """
    session = boto3.session.Session()
    client = session.client(
        service_name=service_name,
        endpoint_url=os.getenv("LOCALSTACK_ENDPOINT_URL"),
        use_ssl=False,
        verify=False,
        aws_access_key_id="localstack",
        aws_secret_access_key="test",
        region_name=region_name,
    )
    return client


def boto3_resource_localstack(service_name: str, region_name: str = "eu-central-1") -> boto3.session.Session.resource:
    session = boto3.session.Session()
    resource = session.resource(
            service_name=service_name,
            endpoint_url=os.getenv("LOCALSTACK_ENDPOINT_URL"),
            use_ssl=False,
            verify=False,
            aws_access_key_id="localstack",
            aws_secret_access_key="test",
            region_name=region_name,
        )
    return resource
