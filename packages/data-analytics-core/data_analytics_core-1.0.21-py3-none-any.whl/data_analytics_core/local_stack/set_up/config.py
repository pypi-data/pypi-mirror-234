import os

# TODO: Refactor project name

ENVIRONMENT_TAG = "localstack"

_CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
TESTS_PATH = f"{os.path.split(os.environ['VIRTUAL_ENV'])[0]}/tests"


UNIT_TESTS_PATH = f"{TESTS_PATH}/unit"
TESTS_FIXTURES_PATH = f"{TESTS_PATH}/fixtures"
OUTPUTS_PATH = f"{TESTS_PATH}/outputs"
TESTS_FIXTURES_RAW_PATH = f'{TESTS_FIXTURES_PATH}/raw_data'
INTEGRATION_TESTS_PATH = f"{TESTS_PATH}/integration"


