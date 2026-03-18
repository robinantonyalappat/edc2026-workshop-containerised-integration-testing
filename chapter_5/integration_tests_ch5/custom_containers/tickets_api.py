from typing import Tuple

from testcontainers.core.container import DockerContainer
from testcontainers.core.image import DockerImage

class TicketsAPI:
    def __init__(
        self,
        container: DockerContainer,
        backend_url: str,
        name: str,
        port: int,
        alias: str,
    ) -> None:
        self.container: DockerContainer = container
        self.backend_url: str = backend_url
        self.name: str = name
        self.port: int = port
        self.alias: str = alias


def create_tickets_api_container(connection_string: str) -> Tuple[DockerImage, DockerContainer]:
    #with DockerImage(path="./core/tests/image_fixtures/sample/", tag="test-image") as image:
    image = DockerImage(path="tickets_api", tag="development")
    container = DockerContainer(image=str(image)).with_exposed_ports(3000).with_env('TICKETS_DATABASE_URL', connection_string)
    
    return image, container


def wait_for_tickets_api_to_be_ready(backend_url: str, timeout: int = 20) -> None:
    raise NotImplementedError
