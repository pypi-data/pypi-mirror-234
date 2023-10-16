from muvinai.utilities.init_creds import init_mongo
from muvisdk.SDK import SDK
from .brand import Brand
from .sede import Sede

from bson import ObjectId
from typing import Optional


class MerchantsIterator:
    def __init__(self, merchants, cadena):
        self.merchants = merchants
        self.index = 0
        self.cadena = cadena

    def __next__(self):
        index = self.index
        if index == len(self.merchants):
            raise StopIteration

        self.index += 1
        return Merchant(self.merchants[index])


class Merchants:
    def __init__(self, brand_id=None):
        db = init_mongo()
        query = {}
        if brand_id:
            query['brand_id'] = brand_id
        self.merchants = list(db.merchants.find(query))
        self.cadena = db.merchants.find_one(ObjectId('6178652dcfb117ad58a2cd3d'))

    def __iter__(self):
        return MerchantsIterator(self.merchants, self.cadena)


class Merchant:
    _cadena_db = None

    @classmethod
    def _get_cadena_db(cls):
        if not cls._cadena_db:
            db = init_mongo()
            cls._cadena_db = db.merchants.find_one(ObjectId('6178652dcfb117ad58a2cd3d'))
        return cls._cadena_db

    @classmethod
    def get_cadena(cls):
        cadena_db = cls._get_cadena_db()
        return Merchant(cadena_db)

    @classmethod
    def search(cls, brand_id=None):
        return Merchants(brand_id=brand_id)

    def __init__(self, merchant_db, brand: Brand = None, sede: Sede = None):
        self.merchant_db = merchant_db
        self.id = merchant_db['_id']
        self.name = merchant_db['name']
        self.brand_id = merchant_db['brand_id']
        self.sede_principal = merchant_db.get('sede_principal')
        self.credentials = merchant_db['credentials']
        self.application_fee: dict = {k.lower(): v for k, v in merchant_db.get('application_fee', {}).items()}
        self.planes_multinegocio = merchant_db.get('planes_multinegocio', [])
        self.afip = merchant_db.get('afip')
        self.brand = brand
        self.sede = sede
        cadena_db = self._get_cadena_db()
        self.sdk_decidir = SDK(self.merchant_db, cadena_db, 'decidir', marketplace=False)
        self.sdk_decidir_marketplace = SDK(self.merchant_db, cadena_db, 'decidir', marketplace=True)
        self.sdk_mercadopago = SDK(self.merchant_db, cadena_db, 'mercadopago', marketplace=False)
        self.sdk_mercadopago_marketplace = SDK(self.merchant_db, cadena_db, 'mercadopago', marketplace=True)
        self.application_id = self.credentials['mercadopago'].get('application_id')
        self.plans_ids = None

    @property
    def activate_facturacion(self) -> bool:
        return self.afip is not None and self.afip.get('activate_facturacion', False)

    def get_brand(self) -> Brand:
        if not self.brand:
            db = init_mongo()
            self.brand = Brand(db.brands.find_one(self.brand_id))
        return self.brand

    def get_sede(self) -> Sede:
        if not self.sede:
            db = init_mongo()
            self.sede = Sede(db.club.find_one(self.sede_principal))
        return self.sede

    def get_plans_ids(self) -> list:
        if not self.plans_ids:
            db = init_mongo()
            self.plans_ids = [p['_id'] for p in db.planes.find({'merchant_id': self.id}, {'_id': 1})]
        return self.plans_ids

    def get_planes_multinegocio(self) -> list:
        if not self.plans_ids:
            db = init_mongo()
            self.plans_ids = [p['_id'] for p in db.planes.find({'merchant_id': self.id}, {'_id': 1})]
        return self.plans_ids

    def get_application_fee(self, plan_id: ObjectId) -> Optional[float]:
        for p in self.planes_multinegocio:
            if p['plan_id'] == plan_id:
                return p['application_fee']

    def get_application_fee_by_cobro(self, cobro: str) -> float:
        default_application_fee = 0
        return self.application_fee.get(cobro.lower(), default_application_fee)

    def processors(self, marketplace: bool) -> list:
        processors = []
        if marketplace:
            if self.sdk_decidir_marketplace.ok():
                processors.append('decidir')
            if self.sdk_mercadopago_marketplace.ok():
                processors.append('mercadopago')
        else:
            if self.sdk_decidir.ok():
                processors.append('decidir')
            if self.sdk_mercadopago.ok():
                processors.append('mercadopago')
        return processors

    def get_sdk(self, processor: str, marketplace: bool = False) -> SDK:
        if processor == 'decidir':
            return self.sdk_decidir_marketplace if marketplace else self.sdk_decidir
        return self.sdk_mercadopago_marketplace if marketplace else self.sdk_mercadopago
