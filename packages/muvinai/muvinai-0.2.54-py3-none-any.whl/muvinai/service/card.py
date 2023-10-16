from typing import Optional
from muvisdk.SDK import SDK


class Card:
    def __init__(self, data: dict = None):
        self.data = data
        if not data:
            data = dict()
        self.id = data.get('id')
        self.mercadopago_id = data.get('mercadopago_id')
        self.decidir_id = data.get('decidir_id')
        self.card_type = data.get('card_type')
        self.card_brand = data.get('card_brand')
        self.first_six_digits = data.get('first_six_digits')
        self.payment_method_id = data.get('payment_method_id')

    def processors(self) -> list:
        processors = []
        if not self.data:
            return processors

        if 'decidir_id' in self.data:
            processors.append('decidir')
        if 'mercadopago_id' in self.data or 'id' in self.data:
            processors.append('mercadopago')

        return processors

    @classmethod
    def empty_card(cls):
        return Card()

    def get_id(self, processor: str) -> str:
        if processor == 'decidir':
            return self.decidir_id
        return self.mercadopago_id if self.mercadopago_id else self.id

    def tokenize(self, sdk: SDK) -> Optional[str]:
        response = sdk.card_token().create(self.data)
        if response["status"] > 299:
            print("         Falló la creación de token de tarjeta.")
            print(response["response"])
            return None

        return response["response"]["id"]
