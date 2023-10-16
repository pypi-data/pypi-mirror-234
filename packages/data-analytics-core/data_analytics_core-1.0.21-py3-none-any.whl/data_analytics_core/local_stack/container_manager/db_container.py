####### WIP ############
####### WIP ############
####### WIP ############
####### WIP ############
####### WIP ############
from testcontainers.core.container import DockerContainer
from testcontainers.mysql import MySqlContainer
# custom imports
from data_analytics_core.logger.da_core_logger import da_logger

DB_CONTAINER: DockerContainer
DB_URL: str = ""

da_logger.info(f"Starting {__file__}")


# TODO: extract outside (not localstack part)
def _setup_db_container() -> MySqlContainer:
    db_container = MySqlContainer(
        image="mysql:latest",
        MYSQL_USER="user",
        MYSQL_PASSWORD="supersecretpassword",
        MYSQL_DATABASE="igsmysql",
        MYSQL_ROOT_PASSWORD="root"
    ).with_command(
        command="mysqld --default-authentication-plugin=mysql_native_password"
    )
    db_container.start()
    da_logger.info("DB container started")

    return db_container


def start_test_run():
    global DB_CONTAINER
    global DB_URL

    DB_CONTAINER = _setup_db_container()
    DB_URL = DB_CONTAINER.get_connection_url()

    # setup_localstack_common_infrastructure()
