from bson import ObjectId
from dateutil.relativedelta import relativedelta

from ..utilities.dates import (
    calculate_payment_date,
    get_periodo,
    set_next_vigency,
    today_argentina,
)
from ..utilities.members import create_history_event


class Client:
    def __init__(self):
        pass

    def create(
        self,
        active_plan_id,
        payment_id,
        card=None,
        discount=None,
        plan_corporativo=None,
        **kwargs
    ):
        self.active_plan_id = ObjectId(active_plan_id)
        self.payment_ids = [payment_id]
        self.last_payment_id = payment_id
        self.plan_corporativo = plan_corporativo
        self.nacimiento = "22/02/2022"
        self.preferred_payment_method = "tarjeta"
        self.status = "pago en proceso"
        self.cobros_recurrentes = 0

        self.__dict__.update(kwargs)
        self.discounts = [] if not discount else [discount]
        self.cards = [] if not card else [card]

        if card:
            self.active_card = card["id"]

        today = today_argentina()
        f_vigencia_apto = today + relativedelta(days=30)
        self.apto_medico = {
            "url": "",
            "status": "validado",
            "fecha_vigencia": f_vigencia_apto.replace(
                day=f_vigencia_apto.day, hour=23, minute=59, second=59
            ),
        }

        self.history = [
            create_history_event(
                member=self.__dict__, event_type="alta", source="checkout"
            )
        ]

    def set_dates(self, cobro, date=None):
        if not date:
            date = today_argentina()

        npd = calculate_payment_date(date.day, cobro, get_periodo(date))
        self.next_payment_date = npd
        self.fecha_vigencia = (
            None
            if self.status == "pago en proceso"
            else set_next_vigency(npd, cobro=cobro)
        )
        self.last_subscription_date = None if self.status == "pago en proceso" else date
        self.period_init_day = date.day

    def import_from_db(self, client: dict):
        for key in client.keys():
            setattr(self, key, client[key])

    def push_to_db(self, db):
        client = db.clientes.find_one(
            {"documento": self.documento, "brand_name": self.brand_name}
        )
        if not client:
            inserted = db.clientes.insert_one(self.__dict__)
            self._id = inserted.inserted_id
        else:
            db.clientes.update_one(
                {"documento": self.documento, "brand_name": self.brand_name},
                {"$set": self.__dict__},
            )

    def to_dict(self):
        return self.__dict__
