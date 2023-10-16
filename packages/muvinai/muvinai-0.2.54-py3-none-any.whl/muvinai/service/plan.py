from muvinai.utilities.init_creds import init_mongo
from .merchant import Merchant


class Plan:
    def __init__(self, plan_db, merchant=None):
        self.plan_db = plan_db
        self.id = plan_db['_id']
        self.name = plan_db['name']
        self.plan_herencia = plan_db.get('plan_herencia')
        self.plan_herencia_db = None
        self.cobro = plan_db['cobro']
        self.nivel_de_acceso = plan_db['nivel_de_acceso']
        self.price = plan_db['price']
        self.merchant_id = plan_db['merchant_id']
        self.payment_methods = plan_db['payment_methods']
        self.merchant = merchant
        self.application_fee = plan_db.get('application_fee')
        self.es_sportclub_cadena = plan_db.get('es-sportclub-cadena', False)

    def get_merchant(self) -> Merchant:
        if not self.merchant:
            db = init_mongo()
            self.merchant = Merchant(db.merchants.find_one(self.merchant_id))
        return self.merchant

    def get_plan_herencia(self):
        if not self.plan_herencia:
            return None
        if not self.plan_herencia_db:
            db = init_mongo()
            self.plan_herencia_db = Plan(db.planes.find_one(self.plan_herencia))
        return self.plan_herencia_db

    def get_application_fee(self) -> float:
        return self.application_fee
