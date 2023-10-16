from correos_seguimiento.errors import UnknownApiResponse


class ShipmentResponse:
    DELIVERED_CODE = "Entregado"
    RELABELED_CODE = "Reetiquetado"

    def __init__(self, raw_response):
        self.json_response = raw_response
        try:
            evento = self.json_response[0]["eventos"][0]
            self.status = evento["desTextoResumen"]
        except (IndexError, KeyError):
            raise UnknownApiResponse

    def _get_bried_associate_event(self):
        return self.json_response[0]["enviosAsociados"][0]

    def is_delivered(self):
        return self.status == self.DELIVERED_CODE

    def is_relabeled(self):
        return self.status == self.RELABELED_CODE

    def get_relabeled_shipment_code(self):
        try:
            return self._get_bried_associate_event()["codEnvio"]
        except (IndexError, KeyError):
            raise UnknownApiResponse
