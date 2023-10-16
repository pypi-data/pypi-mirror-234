"""Logger Class"""
import os
import colorlog
# custom imports
from data_analytics_core.metaclasses.singleton import SingletonMetaClass


class DataAnalyticsLogger(metaclass=SingletonMetaClass):
    def __init__(self, project=None, tech_component=None):
        self.project = project
        self.tech_component = tech_component
        self.code = None
        self.logger = self._logger_config()

    def error(self, message: str, code: str = None):
        self.logger.setLevel(colorlog.ERROR)
        output = self.output(logger_type="Error", message=message, code=code)
        self.logger.error(output)

    def warning(self, message: str, code: str = None):
        self.logger.setLevel(colorlog.WARNING)
        output = self.output(logger_type="Warning", message=message, code=code)
        self.logger.warning(output)

    def debug(self, message: str, code: str = None):
        self.logger.setLevel(colorlog.DEBUG)
        output = self.output(logger_type="Debug", message=message, code=code)
        self.logger.debug(output)

    def info(self, message: str, code: str = None):
        self.logger.setLevel(colorlog.INFO)
        output = self.output(logger_type="Info", message=message, code=code)
        self.logger.info(output)

    def output(self, logger_type: str, message: str, code: str):
        """Message with code and value."""
        output = f"{logger_type} in {self.project}:{self.tech_component};"
        if code:
            output = output + f"{self.new_line()}{logger_type} code: {code};"
        return output + f"{self.new_line()}Message: {message}"

    @staticmethod
    def _logger_config():
        # define handler constraints and format
        handler = colorlog.StreamHandler()
        if "AWS_EXECUTION_ENV" not in os.environ:
            handler.setFormatter(
                fmt=colorlog.ColoredFormatter(
                    "%(log_color)s[%(levelname)s %(asctime)s] %(yellow)s- %(green)s%(message)s",
                    datefmt=None,
                    reset=True,
                    log_colors={
                        "DEBUG": "green",
                        "INFO": "blue",
                        "WARNING": "yellow",
                        "ERROR": "red",
                        "CRITICAL": "white",
                    },
                    secondary_log_colors={},
                    style="%",
                )
            )
        logger = colorlog.getLogger(__name__)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def new_line():
        """
        This function returns the needed new line type for each environment
        """
        return "\n" if "LOCALSTACK_ENDPOINT_URL" in os.environ else "\r"

    def file_key_and_provider_message_addition(self, file_key: str, provider_name: str):
        message = f"{self.new_line()}"\
                  f"{file_key}{self.new_line()}"\
                  f"From provider:{self.new_line()}"\
                  f"{provider_name}{self.new_line()}"
        return message


da_logger = DataAnalyticsLogger()
