import time
from datetime import datetime
from typing import Generator
from loguru import logger
from testcontainers.core.container import DockerContainer, LogMessageWaitStrategy
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.core.network import Network

import pytest

from integration_tests_ch5.custom_containers.postgres import (
    PostgresDatabase,
    create_postgres_container,
)
from integration_tests_ch5.custom_containers.tickets_api import TicketsAPI, create_tickets_api_container


@pytest.fixture
def network():
    with Network() as network:
        yield network

@pytest.fixture
def tickets_api(postgres_database: PostgresDatabase, network: Network) -> Generator[TicketsAPI]:
    #image, container = create_tickets_api_container(postgres_database.connection_string)
    network_alias: str = "tickets-api"
    container = create_tickets_api_container(postgres_database.connection_string, network, network_alias)
    #with image:
    with container:
        wait_for_port_mapping_to_be_available(container=container, port=3000)   
        #strategy = LogMessageWaitStrategy("3000")
        #wait_for_logs(container, strategy) 
        yield TicketsAPI(
            container=container,
            backend_url=postgres_database.connection_string,
            name="tickets-api",
            port=3000,
            alias="tickets-api",
        )
        #raise NotImplementedError

@pytest.fixture
def postgres_database(network: Network) -> Generator[PostgresDatabase]:
    network_alias: str = "postgres"
    with create_postgres_container(network, network_alias=network_alias) as postgres:
        wait_for_port_mapping_to_be_available(container=postgres, port=5432)
        psql_url: str = (
            f"postgresql{postgres.driver}://{postgres.username}:{postgres.password}@{network_alias}:{postgres.port}/{postgres.dbname}"
        )
        yield PostgresDatabase(
            container=postgres, connection_string=psql_url, alias=network_alias
        )


def wait_for_port_mapping_to_be_available(
    container: DockerContainer, port: int, timeout: int = 60, delay: int = 2
) -> None:
    now: datetime = datetime.now()
    while (datetime.now() - now).seconds < timeout:
        try:
            container.get_exposed_port(port)
            return
        except ConnectionError, TimeoutError:
            logger.warning(
                f"Port {port} not yet available, waiting for {delay} seconds..."
            )
            time.sleep(delay)
            continue

    raise ConnectionError(
        f"Port mapping for container {container.image} on port {port} not available within timeout"
    )
