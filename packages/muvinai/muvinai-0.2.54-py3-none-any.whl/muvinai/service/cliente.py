from muvinai.utilities.init_creds import init_mongo
from muvinai.utilities.dates import today_argentina, get_periodo, DIAS_ANTICIPO_DE_PAGO, DIAS_GRACIA
# from muvinai.utilities.members import member_unsubscribe
from muvinai.utilities.mail_sender import (send_mail_pago_en_efectivo, send_mail_cambio_tarjeta,
                                           send_mail_cambio_tarjeta_aon, send_mail_pago_pendiente)
from muvinai.utilities.payments import calculate_payment_date, set_next_vigency
from muvinai.utilities.sportaccess import crear_usuario_sportclub

from .muviBase import MuviBase
from .plan import Plan
from .corporativo import Corporativo
from .merchant import Merchant
from .boleta import Boleta
from .card import Card

from datetime import datetime, timedelta
from typing import Optional
from copy import deepcopy


class ClientesIterator:
    def __init__(self, clientes):
        self.clientes = clientes
        self.index = 0

    def __next__(self):
        return Cliente(self.clientes.next())


class Clientes:
    def __init__(self, query=None, lookup=None):
        db = init_mongo()

        if not query:
            query = {}

        pipeline = [
            {
                '$match': query
            }
        ]

        if lookup:
            for c in lookup:
                if c == 'planes':
                    pipeline.append({
                        '$lookup': {
                            'from': 'planes',
                            'localField': 'active_plan_id',
                            'foreignField': '_id',
                            'as': 'plan'
                        }
                    })
                if c == 'corporativo' and 'planes' in lookup:
                    pipeline.append({
                        '$lookup': {
                            'from': 'planes',
                            'localField': 'active_plan_id',
                            'foreignField': '_id',
                            'as': 'plan'
                        }
                    })

        self.clientes = db.clientes.aggregate(pipeline)

    def __iter__(self):
        return ClientesIterator(self.clientes)


class Cliente(MuviBase):
    @classmethod
    def search(cls, query=None):
        return Clientes(query)

    def __init__(self, cliente_db: dict, plan: Plan = None, corporativo: Corporativo = None):
        super().__init__(cliente_db)
        self.id = cliente_db['_id']
        self.documento = cliente_db['documento']
        self.nombre = cliente_db['nombre']
        self.apellido = cliente_db['apellido']
        self.status = cliente_db['status']
        self.email = cliente_db['email']
        self.domicilio = Domicilio(cliente_db['domicilio'])
        self.discounts = cliente_db['discounts'] if 'discounts' in cliente_db else None
        self.fecha_vigencia = cliente_db['fecha_vigencia']
        self.next_payment_date = cliente_db['next_payment_date']
        self.last_subscription_date = cliente_db['last_subscription_date']
        self.period_init_day = cliente_db['period_init_day']
        self.active_plan_id = cliente_db['active_plan_id']
        self.plan_corporativo = cliente_db.get('plan_corporativo')
        self.cards = cliente_db.get('cards', [])
        self.preferred_payment_method = cliente_db['preferred_payment_method']
        self.brand_name = cliente_db['brand_name']
        self.payment_ids = cliente_db.get('payment_ids', [])
        self.last_payment_id = cliente_db.get('last_payment_id')
        self.history = cliente_db.get('history', [])
        self.poi = cliente_db.get('poi')
        self.cobros_recurrentes = cliente_db.get('cobros_recurrentes', 0)
        self.seller_merchant_id = cliente_db.get('seller_merchant_id')

        self.plan = plan if plan and plan.id == cliente_db['active_plan_id'] else None
        self.corporativo = corporativo if corporativo and corporativo.id == cliente_db['plan_corporativo'] else None
        self.seller_merchant = None

    def get_plan(self) -> Plan:
        if not self.plan:
            db = init_mongo()
            self.plan = Plan(db.planes.find_one(self.active_plan_id))
        return self.plan

    def get_corporativo(self) -> Optional[Corporativo]:
        if not self.plan_corporativo:
            return None

        if self.corporativo:
            db = init_mongo()
            self.corporativo = Corporativo(db.corporativo.find_one(self.plan_corporativo))
        return self.corporativo

    def get_seller_merchant(self) -> Optional[Merchant]:
        if not self.seller_merchant_id:
            return None

        if not self.seller_merchant and self.plan and self.seller_merchant_id == self.plan.merchant_id:
            self.seller_merchant = self.plan.get_merchant()

        if not self.seller_merchant:
            db = init_mongo()
            self.seller_merchant = Merchant(db.merchants.find_one(self.seller_merchant_id))
        return self.seller_merchant

    def existe_boleta_para_periodo_corriente(self) -> bool:
        db = init_mongo()
        existing_period = db.boletas.find_one({
            "member_id": self.id,
            "period": get_periodo(self.next_payment_date + timedelta(days=DIAS_ANTICIPO_DE_PAGO)),
            "source": {
                "$regex": "recurring"
            },
            "status": {
                "$nin": ["refunded", "expired"]
            }
        })
        if not existing_period:
            return False  # crea la boleta nueva

        boleta_checkout = db.boletas.find_one({
            "source": {
                "$regex": "checkout"
            },
            "original_payment_date": {
                "$gt": existing_period["original_payment_date"]
            }
        })
        return boleta_checkout is None  # devuelve true si no existe la de checkout --> no la crea

    def crear_boleta(self, source: str) -> Boleta:
        boleta = Boleta()
        boleta.create(source, cliente=self, merchant=self.get_plan().get_merchant(), plan=self.get_plan())
        return boleta

    # def member_unsubscribe(self, reason: str, source: str):
    #     return member_unsubscribe(self.data, reason, source)

    def get_preferred_payment_method(self) -> str:
        plan = self.get_plan()
        if plan.payment_methods[self.preferred_payment_method]:
            # el plan acepta el ppm del cliente
            return self.preferred_payment_method

        if plan.payment_methods["tarjeta"] or not plan.payment_methods["efectivo"]:
            # el plan no acepta ningun metodo de pago, se usa tarjeta
            return "tarjeta"

        return "tarjeta" if plan.payment_methods["tarjeta"] else "efectivo"

    def get_card(self) -> Card:
        for card in self.cards:
            if card['valid']:
                return Card(card)
        return Card()

    def send_mail_nuevo_pago_en_efectivo(self, boleta: Boleta) -> None:
        receiver = {'nombre': self.nombre, 'email': self.email}
        plan = boleta.get_plan()
        merchant = boleta.get_merchant()
        brand = merchant.get_brand()
        send_mail_pago_en_efectivo(receiver, brand.brand_db, boleta.final_price, plan.name)

    def send_mail_pago_en_efectivo_pendiente(self, boleta: Boleta) -> None:
        receiver = {'nombre': self.nombre, 'email': self.email}
        merchant = boleta.get_merchant()
        brand = merchant.get_brand()
        send_mail_pago_pendiente(receiver, brand.brand_db)

    def send_mail_cambio_de_tarjeta(self) -> dict:
        merchant = self.get_plan().get_merchant()
        brand = merchant.get_brand()
        seller_merchant = self.get_seller_merchant()
        sede = seller_merchant.get_sede() if seller_merchant else merchant.get_sede()
        if self.brand_name.lower() == 'sportclub':
            return send_mail_cambio_tarjeta(self.data, brand.brand_db, sede.email_contacto)
        elif self.brand_name.lower() == 'aon':
            return send_mail_cambio_tarjeta_aon(self.data, brand.brand_db)

    def apply_discounts(self, plan_price: float) -> dict:
        corporativo = self.get_corporativo()
        corpo_discount = corporativo.porcentaje_descuento_empleado if corporativo else 0
        discounts = {}
        if corpo_discount > 0:
            discounts["corpo_discount"] = round(- plan_price * corpo_discount / 100, 2)

        if self.discounts:
            try:  # TODO: Agregar validations para sacar este try
                for discount in self.discounts:
                    if discount['aplicaciones_restantes'] > 0:
                        concepto = discount['concepto'] if 'concepto' in discount else 'n/a'
                        discount_price = plan_price * discount["porcentaje"] / 100 + discount["monto_absoluto"]
                        discounts[concepto] = round(- discount_price, 2)
                        discount['aplicaciones_restantes'] -= 1
            except:
                print(f"    ERROR en el cálculo de descuentos - se retorna un diccionario de precios vacío.")
                return {}

        self.update(discounts=self.discounts)

        return discounts

    def add_history_event(self, event: str, source: str = None) -> None:
        plan = self.get_plan()
        history = self.history if self.history else []
        history.append({
            'event': event,
            'date_created': today_argentina(),
            'source': source,
            'plan': plan.id
        })
        self.update(history=history)

    def crear_usuario_sportclub(self) -> None:
        plan = self.get_plan()
        try:
            crear_usuario_sportclub(self.data, self.payment_ids[-1], plan.nivel_de_acceso)
        except:
            print('Error al intentar crear_usuario_sportclub')

    def calculate_next_payment_date(self, boleta: Boleta) -> datetime:
        plan = self.get_plan()
        npd = calculate_payment_date(self.period_init_day, plan.cobro, boleta.period)
        print("         El próximo dia de cobro es el {}".format(npd.strftime("%d/%m/%y")))
        return npd

    def calculate_vigencia(self, npd: datetime, cobro: str) -> datetime:
        fecha_vigencia = set_next_vigency(npd, cobro)
        if self.status != 'activo' and cobro == 'Mensual':
            fecha_vigencia = fecha_vigencia - timedelta(DIAS_GRACIA)
        print("         Se actualiza la fecha de vigencia: {}".format(fecha_vigencia))
        return fecha_vigencia

    def update_poi(self, boleta: Boleta) -> None:
        if boleta.tries[-1]['processor'] != 'mercadopago':
            return

        poi = {
            "installments": self.poi["installments"] + 1 if self.poi else 1,
            "payment_reference": boleta.last_payment_id
        }

        self.update(poi=poi)

    def update_client(self, boleta: Boleta, update_npd: bool = False) -> None:
        self.update(lastModified=today_argentina())

        if boleta.last_payment_id:
            print("         Se inserta payment id en el cliente.")
            payment_ids = self.payment_ids
            payment_ids.insert(0, boleta.last_payment_id)
            self.update(payment_ids=payment_ids, last_payment_id=boleta.last_payment_id)

        npd = self.calculate_next_payment_date(boleta)
        if update_npd:
            self.update(next_payment_date=npd)

        plan = boleta.get_plan()
        if boleta.status == 'approved':
            self.update(
                fecha_vigencia=self.calculate_vigencia(npd, plan.cobro),
                cobros_recurrentes=self.cobros_recurrentes + 1
            )
            self.update_poi(boleta)

    def update_plan_herencia(self) -> bool:
        plan = self.get_plan()
        if plan.plan_herencia:
            self.add_history_event('plan_herencia', source='cobros_recurrentes')
            self.update(active_plan_id=plan.plan_herencia)
            self.plan = plan.get_plan_herencia()
            print("[Plan Herencia] El cliente {} con plan {} pasa a tener el plan {}".format(self.id,
                                                                                             self.active_plan_id,
                                                                                             plan.plan_herencia))
            return True
        return False

    def push_to_db(self) -> None:
        db = init_mongo()
        to_update = deepcopy(self._to_update)
        to_unset = {}
        if 'poi' in to_update and not to_update['poi']:
            to_unset['poi'] = ''
            del to_update['poi']

        r = db.clientes.update_one(
            {'_id': self.id},
            {
                '$set': to_update,
                '$unset': to_unset
            }
        )
        print('Cliente actualizado en db', r.matched_count, r.modified_count)


class Domicilio:
    def __init__(self, data):
        self.provincia = data['provincia'] if 'provincia' in data else None
        self.localidad = data['localidad'] if 'localidad' in data else None
        self.calle = data['calle'] if 'calle' in data else None
        self.altura = data['altura'] if 'altura' in data else None

        try:
            self.altura = int(self.altura)
        except ValueError:
            pass
