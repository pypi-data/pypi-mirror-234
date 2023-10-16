from datetime import datetime, timedelta
from pprint import pprint
from bson import ObjectId
from ..utilities.dates import today_argentina, DIAS_ANTICIPO_DE_PAGO


class Boleta:
    def __init__(self):
        self.member_id = None
        self.date_created = None
        self.original_payment_date = None
        self.source = None
        self.tries = []
        self.status = None
        self.merchant_id = None
        self.charges_detail = None
        self.period = None
        self.plan_id = None

    def create(
        self,
        cliente_id,
        merchant_id,
        plan_id,
        source: str,
        status: str = "error_not_proccesed",
        charges_detail: dict = None,
        opd: datetime = today_argentina(),
        date_created: datetime = today_argentina(),
        **kwargs,
    ):
        for field_id in [cliente_id, merchant_id, plan_id]:
            field_id = ObjectId(field_id) if ObjectId.is_valid(field_id) else None

        self.member_id = cliente_id
        self.date_created = date_created
        self.original_payment_date = opd
        self.source = source
        self.tries = []
        self.status = status
        self.merchant_id = merchant_id
        self.charges_detail = charges_detail if charges_detail else {}
        self.period = None
        self.plan_id = plan_id
        self.__dict__.update(kwargs)

    def push_to_db(self, db):
        if hasattr(self, "_id"):
            result = db.boletas.update_one({"_id": self._id}, {"$set": self.__dict__})
            return self._id

        result = db.boletas.insert_one(self.__dict__)
        self._id = result.inserted_id
        return result.inserted_id

    def import_from_db(self, boleta: dict):
        for key in boleta.keys():
            setattr(self, key, boleta[key])

    def add_try(self, payment_data: dict, card_data: dict = None):
        # Complete with card data
        if card_data:
            for e in ["card_brand", "card_id", "payment_type"]:
                if e in card_data:
                    payment_data[e] = card_data[e]
                    continue
                payment_data[e] = None

        if not payment_data.get("payment_type"):
            payment_data["payment_type"] = payment_data.get("card", {}).get(
                "card_type", None
            )

        # Genera el nuevo try
        new_try = {
            "try_number": len(self.tries) + 1,
            "payment_day": payment_data["payment_day"],
            "payment_type": payment_data["payment_type"],
            "status": payment_data["status"],
            "status_detail": payment_data["status_detail"],
            "card_id": payment_data["card_id"],
            "card_brand": payment_data["card_brand"],
            "payment_id": payment_data["id"],
            "processor": payment_data.get("processor"),
            "date_approved": payment_data.get("date_approved"),
        }
        self.tries.append(new_try)
        self.status = new_try["status"]

    def make_period(self, fecha_de_cobro: datetime, DIAS_DE_ANTICIPO: int = 0):
        if "recurring" in self.source:
            DIAS_DE_ANTICIPO = DIAS_ANTICIPO_DE_PAGO
        fecha_de_cobro += timedelta(days=DIAS_DE_ANTICIPO)
        period = f"{fecha_de_cobro.month}/{fecha_de_cobro.year}"
        self.period = period

    def print(self):
        pprint(self.__dict__)

    def to_dict(self):
        return self.__dict__
