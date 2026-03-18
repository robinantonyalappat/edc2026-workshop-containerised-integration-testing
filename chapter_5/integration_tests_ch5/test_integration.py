from loguru import logger
import time

from integration_tests_ch5.custom_containers.postgres import PostgresDatabase
from integration_tests_ch5.custom_containers.tickets_api import TicketsAPI

import pytest

import requests
from datetime import datetime

from pydantic import BaseModel, Field

def test_startup_of_custom_tickets_api_container(
    tickets_api: TicketsAPI, 
    postgres_database: PostgresDatabase
) -> None:
    logger.info(f"Started Tickets API with image {tickets_api.container.image}")
    logger.info(f"Started Tickets API with port {tickets_api.port}")

    logger.info(f"Started database with name {postgres_database.container.dbname}")
    logger.info(
        f"Started database with username {postgres_database.container.username}"
    )
    logger.info(
        f"Started database with password {postgres_database.container.password}"
    )
    logger.info(f"Started database with port {postgres_database.container.port}")
    #time.sleep(20)

class TicketDto(BaseModel):
    id: int
    train_code: str
    passenger_name: str
    seat_number: int | None
    expiration_date: datetime

@pytest.mark.parametrize(
    "train_code,passenger_name,seat_number",
    [
        ("The Orient Express", "Leonardo DaVinci", 14),
        # ("Bergensbanen", "Jonas Gahr Støre", 1),
        # ("Raumabanen", "Kong Harald", None),
    ],
)
def test_buy_ticket(
    tickets_api: TicketsAPI, train_code: str, passenger_name: str, seat_number: str | int
) -> None:
    # buy_ticket_payload: TicketBuyRequest = TicketBuyRequest(
    #     train_code=train_code,
    #     passenger_name=passenger_name,
    #     seat_number=seat_number,
    # )
    logger.info(f"Started Tickets API with image {tickets_api.container.image}")
    #logger.info(f"Started Tickets API with port {tickets_api.port}")
    logger.info(f"Started Tickets API with exposed port {tickets_api.container.get_exposed_port(3000)}")
    port=tickets_api.container.get_exposed_port(3000)

    url = f'http://localhost:{port}/tickets/buy' # A service that echoes POST requests
    #payload = f'{'train_code': {train_code}, 'passenger_name': passenger_name, 'seat_number': seat_number}'
    payload = {'train_code': train_code, 'passenger_name': passenger_name, 'seat_number': seat_number}
    logger.info(f"Response status code: {payload}")

    # Send the POST request with form data
    r = requests.post(url, json=payload)

    # buy_ticket_response: Response = tickets_api(
    #     "/tickets/buy/", json=buy_ticket_payload.model_dump()
    # )
    logger.info(f"Response status code: {r.status_code}")
    logger.info(f"Response status code: {r.json()}")
    ticket: TicketDto = TicketDto.model_validate(r.json())

    assert ticket.id
    assert ticket.train_code == train_code
    assert ticket.passenger_name == passenger_name
    assert ticket.seat_number == seat_number