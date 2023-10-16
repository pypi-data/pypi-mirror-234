"""
AWS_SSM Class
Class containing all the needed AWS Service Manager actions and the client itself.
"""
import io
import os
from typing import Optional
import boto3
import urllib.parse
import re
import botocore.exceptions
import botocore.client
import pandas as pd
from pandas.errors import EmptyDataError
# custom imports
from data_analytics_core.exceptions.infrastructure.aws_infrastructure_exceptions import FileDialectEncodingNotExpectedError, \
    ProviderPrefixError
from data_analytics_core.logger.da_core_logger import da_logger
from data_analytics_core.local_stack.boto_client_moks.localstack_clients import boto3_client_localstack, boto3_resource_localstack


class AmazonWebServicesS3:

    def __init__(self, event=None, bucket=None, region_name="eu-central-1", get_provider_prefix: bool = False):
        # env aws connections generation
        self.region_name = region_name
        if os.getenv("LOCALSTACK_ENDPOINT_URL"):
            self.s3_client = boto3_client_localstack(service_name="s3", region_name=self.region_name)
            self.s3_resource = boto3_resource_localstack(service_name="s3", region_name=self.region_name)
        else:
            self.s3_client = boto3.client('s3')
            self.s3_resource = boto3.resource('s3')
        # custom variables
        self.bucket = bucket
        self.event = event
        if self.event:
            # from eventbridge s3 event
            self.key = urllib.parse.unquote_plus(self.event['detail']['object']['key'], encoding='utf-8')
            self.bucket = self.event['detail']['bucket']['name']
        if get_provider_prefix:
            if re.match(pattern=r"year", string=self.key):
                self.provider_prefix = re.match(pattern=r"^(.(?!year))*",
                                                string=self.key).group(0)
            else:
                self.provider_prefix = re.match(pattern=r"(\w+)",
                                                string=self.key).group(0)
            if not self.provider_prefix:
                raise ProviderPrefixError(f'Error in file with key: {self.key}{da_logger.new_line()}'
                                          f'It is not a provider from the expected ones,'
                                          f'or this file is not inside the prefix it should')

    def get_file_content_from_excel(self, sheet_name_re: str) -> pd.DataFrame:
        # Download file from bucket
        file_body = self._get_s3_object(self.bucket, self.key)
        # Parse file
        xlsx = pd.ExcelFile(path_or_buffer=io.BytesIO(file_body.read()), engine="openpyxl")
        if sheet_name_re:
            for sheet_num in range(len(xlsx.sheet_names)):
                sheet_name = re.search(pattern=sheet_name_re, string=xlsx.sheet_names[sheet_num]).group(0)
                if sheet_name:
                    return xlsx.parse(sheet_name)
        return xlsx.parse()

    def upload_dataframe(self, dataframe: pd.DataFrame, key=None, bucket=None, is_csv=True):
        if not key:
            key = self.key
        if not bucket:
            bucket = self.bucket
        if is_csv is True:
            dataframe = dataframe.to_csv(encoding="UTF-8", sep=";", decimal=".", index=False)
            self.s3_client.upload_fileobj(io.BytesIO(bytes(dataframe, "UTF-8")), bucket, key)

    # TODO: refactor to reduce complexity
    def get_file_content_from_csv(self,
                                  encoding: str = None,
                                  file_body=None,
                                  separator: str = None,
                                  decimal: str = None
                                  ) -> pd.DataFrame:
        # Download file from bucket
        if not file_body:
            file_body = self._get_s3_object(self.bucket, self.key)
        # Parse file
        if not encoding:
            encoding_list = ["utf-8", "latin-1", "mac-latin2", "ISO-8859-1"]
        else:
            encoding_list = [encoding]
        if not separator:
            separator_list = [";", ",", "."]
        else:
            separator_list = [separator]
        if not decimal:
            decimal_list = [".", ","]
        else:
            decimal_list = [decimal]
        warnings_list = []
        for encoder in encoding_list:
            for separator in separator_list:
                for decimal in decimal_list:
                    try:
                        return pd.read_csv(
                            io.BytesIO(file_body.read()),
                            sep=separator,
                            encoding=encoding,
                            decimal=decimal
                        )
                    except (pd.errors.ParserError, UnicodeDecodeError, EmptyDataError):
                        warnings_list.append([f"Encoder: {encoder}", f"Separator: {separator}", f"Decimal: {decimal}"])
        raise FileDialectEncodingNotExpectedError(
            f"Found no encoder and separator combination to fit in file:"
            f"{da_logger.file_key_and_provider_message_addition(self.key, self.provider_prefix)}"
            f"Combinations searched:{da_logger.new_line()}{warnings_list}")

    def get_file_content_from_txt(self):
        # Download file from bucket
        file_body = self._get_s3_object(self.bucket, self.key)
        # Parse file
        return io.BytesIO(file_body.read()).read().decode('utf-8')

    def move_file(self, key: str = None, bucket: str = None,
                  new_key=None, new_bucket=None, delete_origin_file=True) -> None:
        # Prepare copying config
        if key and bucket:
            copy_source = {'Key': key, 'Bucket': bucket}
        else:
            copy_source = {'Key': self.key, 'Bucket': self.bucket}
        # Handling bucket and empty move file exceptions
        try:
            self.s3_client.list_objects_v2(Bucket=self.bucket, Prefix=self.key)
            # This step is used because boto3 does not raise anything if the response inside the bucket is empty
            if self.s3_client.list_objects_v2(Bucket=self.bucket, Prefix=self.key)["KeyCount"] == 0:
                raise da_logger.error(f"The prefix used: {self.key} was not found inside the bucket: {self.bucket}")
        except (botocore.exceptions.ClientError, botocore.client.ClientError):
            da_logger.error(f"The bucket: {self.bucket} was not found, does not exist or is misswriten")
        except AttributeError:
            self.s3_client.list_objects_v2(Bucket=bucket, Prefix=key)
            # This step is used because boto3 does not raise anything if the response inside the bucket is empty
            if self.s3_client.list_objects_v2(Bucket=bucket, Prefix=key)["KeyCount"] == 0:
                raise da_logger.error(f"The prefix used: {key} was not found inside the bucket: {bucket}")
        # Executing possible move configs
        if new_key and new_bucket is None:
            self.s3_client.copy_object(Bucket=copy_source.get("Bucket"), Key=new_key, CopySource=copy_source)
            da_logger.info(f"The file: {key}{da_logger.new_line()}From bucket: {bucket}"
                            f"{da_logger.new_line()}Has been copied to prefix: "
                            f"{new_key}{da_logger.new_line()}And bucket: {bucket}")
        elif new_key and new_bucket:
            self.s3_client.copy_object(Bucket=new_bucket, Key=new_key, CopySource=copy_source)
            da_logger.info(f"The file: {key}{da_logger.new_line()}From bucket: "
                            f"{bucket}{da_logger.new_line()}Has been copied to prefix: "
                            f"{new_key}{da_logger.new_line()}And bucket: {new_bucket}")
        elif new_key is None and new_bucket:
            self.s3_client.copy_object(Bucket=new_bucket, Key=copy_source.get("Key"), CopySource=copy_source)
            da_logger.info(f"The file: {self.key}{da_logger.new_line()}From bucket: "
                            f"{self.bucket}{da_logger.new_line()}Has been copied to prefix: "
                            f"{self.key}{da_logger.new_line()}And bucket: {new_bucket}")
        # Delete old file (if specified)
        if delete_origin_file:
            self.s3_resource.Object(copy_source.get("Bucket"), copy_source.get("Key")).delete()
            da_logger.info("The original file has been deleted.")

    def extract_year_from_key(self) -> int:
        year_and_month_grouped = re.search('/year=(\d{4})/', self.key)
        return int(year_and_month_grouped.group(1))

    def extract_month_from_key(self) -> str:
        year_and_month_grouped = re.search('/month=(\d{2})/', self.key)
        return str(year_and_month_grouped.group(1)).zfill(2)

    def _get_s3_object(self, bucket_name: str, object_key: str):
        response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
        return response['Body']

    def get_list_of_objects(self, bucket, prefix='', suffix='') -> Optional[list]:
        keys_list = list(self._get_generator_list_matching_s3_keys(bucket, prefix, suffix))
        if len(keys_list):
            result_list = []
            for key in keys_list:
                result_list.append(key)
            return result_list
        else:
            return None

    # TODO: get yield information to optimize below function

    def _get_generator_list_matching_s3_keys(self, bucket: str, prefix='', suffix=''):
        """
        Generate the keys in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch keys that start with this prefix (optional).
        :param suffix: Only fetch keys that end with this suffix (optional).
        """
        kwargs = {'Bucket': bucket}
        # If the prefix is a single string (not a tuple of strings), we can
        # do the filtering directly in the S3 API.
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix

        while True:

            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = self.s3_client.list_objects_v2(**kwargs)
            if resp["KeyCount"] == 0:
                return None
            else:
                for obj in resp['Contents']:
                    key = obj['Key']
                    if key.startswith(prefix) and key.endswith(suffix):
                        yield key

            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break
