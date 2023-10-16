import requests

from correos_seguimiento.errors import (
    InvalidApiResponse,
    InvalidCredentials,
    InvalidEndpoint,
    TimeOut,
    UndefinedCredentials,
)
from correos_seguimiento.responses.shipment import ShipmentResponse

URL = "https://localizador.correos.es/canonico/eventos_envio_servicio_auth/{}?indUltEvento=S"


class TrackingShipment:
    def __init__(self, user, pwd, shipment_number, timeout=2):
        self.shipment_number = shipment_number
        self.user = user
        self.pwd = pwd
        self.timeout = timeout

    def _send_request(self):
        if not self.user or not self.pwd:
            raise UndefinedCredentials
        try:
            response = requests.get(
                URL.format(self.shipment_number),
                auth=(self.user, self.pwd),
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise TimeOut
        if response.status_code == 401:
            raise InvalidCredentials
        elif response.status_code != 200:
            raise InvalidEndpoint
        try:
            json = response.json()
        except requests.JSONDecodeError:
            raise InvalidApiResponse
        return json

    def build(self):
        return ShipmentResponse(self._send_request())
