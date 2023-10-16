######### WIP #########
######### WIP #########
######### WIP #########
######### WIP #########
######### WIP #########

import os
import subprocess
import sys
# custom imports
from data_analytics_core.aws.s3 import AmazonWebServicesS3
from data_analytics_core.logger.da_core_logger import da_logger
from data_analytics_core.local_stack.set_up.config import TESTS_FIXTURES_RAW_PATH, OUTPUTS_PATH


class LocalstackCommonInfrastructure:
    def __init__(self, s3_port):
        self.raw_bucket = os.environ.get(key="raw_bucket_name")
        self.processed_bucket = os.environ.get(key="processed_bucket_name")
        self.aws_s3 = AmazonWebServicesS3()
        self.aws_s3.s3_client.create_bucket(Bucket=self.processed_bucket)
        self.aws_s3.s3_client.create_bucket(Bucket=self.raw_bucket)
        # upload fixtures
        self.fixture_upload()
        self.s3_port = s3_port
        da_logger.info(f"{sys.path}{da_logger.new_line()}{sys.path[1]}")

    def fixture_upload(self, fixture_list: list = None):
        if not fixture_list:
            fixture_list = self._recursive_provider_iterator(directory=TESTS_FIXTURES_RAW_PATH)
        for fixture in fixture_list:
            fixture_path = f"{TESTS_FIXTURES_RAW_PATH}/{fixture}"
            self.aws_s3.s3_client.upload_file(
                fixture_path,
                self.raw_bucket,
                fixture,
            )
            # TODO: refactor iterating sub-levels of fixtures
            # try:
            # except IsADirectoryError:
            #     fixture_flattened_path_list = self._recursive_provider_iterator(directory=fixture_path)
            #     for flattened_fixture in fixture_flattened_path_list:
            #         flattened_fixture_path = fixture_path + flattened_fixture
            #         self.aws_s3.s3_client.upload_file(
            #             flattened_fixture_path,
            #             self.raw_bucket,
            #             fixture,
            #         )

    def get_s3_file_as_output(self,
                              aws_s3: AmazonWebServicesS3,
                              bucket=None,
                              prefix: str = '',
                              suffix: str = ''):
        """
        Function to extract data from buckets.
        If there are specified filter_buckets,only those in the list will be copied (or tuple, or set)
        """
        try:
            files_list = aws_s3.get_list_of_objects(bucket=bucket, prefix=prefix, suffix=suffix)
            for file in files_list:
                da_logger.info(f"Downloading file:{file}{da_logger.new_line()}"
                                f"From bucket {bucket}")
                command = (f"awslocal s3 cp s3://{bucket}/{file} "
                           f"{OUTPUTS_PATH}/{bucket}/ --endpoint http://localhost:"
                           f"{self.s3_port}"
                           )
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                p.communicate()
        except Exception as e:
            da_logger.error(f"Exception in {__name__} e: {e}")

    def _recursive_provider_iterator(self, directory: str) -> list:
        providers = os.listdir(directory)
        files_list = []
        for provider in providers:
            files = os.listdir(f"{directory}/{provider}")
            files_list.append([(provider + "/" + unflattened) for unflattened in files])
        files_list = self._list_flatten(files_list)
        return files_list

    def _list_flatten(self, nested_lists: list) -> list:
        flat_list = []
        self._flattener(flat_list, nested_lists)
        return flat_list

    def _flattener(self, flat_list, nested_lists):
        for subelement in nested_lists:
            if type(subelement) == list:
                self._flattener(flat_list, subelement)
            else:
                flat_list.append(subelement)
