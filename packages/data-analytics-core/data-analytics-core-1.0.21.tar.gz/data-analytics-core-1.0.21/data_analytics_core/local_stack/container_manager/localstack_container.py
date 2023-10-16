"""
Local Stack container manager Class
"""
import os
import requests
from docker.errors import APIError
# custom imports
from testcontainers.localstack import LocalStackContainer
from data_analytics_core.logger.da_core_logger import da_logger
from data_analytics_core.local_stack.set_up.config import TESTS_PATH
from data_analytics_core.local_stack.set_up.infrastructure import LocalstackCommonInfrastructure


class LocalStackContainerManager:
    local_stack_container = None
    os.environ["LOCALSTACK_ENDPOINT_URL"] = ''

    def __init__(self, list_of_environment_variables: list, project_name: str, persists=False):
        version = "0.14.2"
        self.local_stack_container = (
            LocalStackContainer(f"localstack/localstack:{version}").with_env("DATA_DIR", "/tmp/set_up/data").
            with_exposed_ports(4566).with_name("AWSMockWithPersistence")
        )
        if persists:
            self.local_stack_container.with_volume_mapping(
                host=f"{TESTS_PATH}/localstack_data",
                container="/tmp/localstack/data",
                mode="rw",
            )
        self.project_name = project_name
        self._start()
        self.s3_port = self.local_stack_container.get_exposed_port(4566)
        self._generate_internal_env_vars()
        self.generate_env_vars_from_dict_list(list_of_environment_variables)
        self.common_infra = LocalstackCommonInfrastructure(self.s3_port)
        da_logger.info("Common infra emulated")

    def add_fixtures(self, fixture_list: list):
        self.common_infra.fixture_upload(fixture_list=fixture_list)

    def _start(self):
        try:
            self.local_stack_container.start()
            da_logger.info("No previous docker was mounted")
        except (AttributeError, APIError, requests.exceptions.HTTPError):
            # TODO: evaluate below bash to check on alternatives to kill doc command
            os.system("docker rm -f $(docker container ls -q --filter name='AWS*')")
            da_logger.info("Previous docker was mounted and running. It has been succesfully terminated")
            self.local_stack_container.start()
        da_logger.info("Localstack container started")

    def stop(self):
        """
        https://docs.python.org/3/library/unittest.html#unittest.TestResult.stopTestRun
        Called once after all tests are executed.
        :return:
        """
        self.local_stack_container.stop()
        da_logger.info("Localstack container stopped")

    def _generate_internal_env_vars(self) -> None:
        os.environ["LOCALSTACK_ENDPOINT_URL"] = f"http://localhost:{self.s3_port}"
        os.environ["env"] = "localstack"
        os.environ["project"] = self.project_name

    @staticmethod
    def generate_env_vars_from_dict_list(list_of_dicts):
        for dictionary in list_of_dicts:
            for key,value in dictionary:
                os.environ[key] = value