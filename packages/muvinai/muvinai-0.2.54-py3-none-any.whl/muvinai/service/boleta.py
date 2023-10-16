from datetime import datetime, timedelta
from typing import Optional

from muvinai.utilities.dates import today_argentina, get_periodo, DIAS_ANTICIPO_DE_PAGO
from muvinai.utilities.payments import datetime_parser, get_client_price, get_access_amount
from muvinai.utilities.init_creds import init_mongo, test

from muvisdk import SDK

from .muviBase import MuviBase
from .merchant import Merchant
from .plan import Plan
from .card import Card


class Boleta(MuviBase):
    @classmethod
    def get(cls, boleta_id):
        db = init_mongo()
        boleta_db = db.boletas.find_one(boleta_id)
        return Boleta(boleta_db) if boleta_db else None

    def __init__(self, boleta_db: dict = None, cliente=None, merchant: Merchant = None, plan: Plan = None):
        super().__init__(boleta_db)
        if not boleta_db:
            boleta_db = {}
        self.id = boleta_db.get('_id')
        self.member_id = boleta_db.get('member_id')
        self.date_created = boleta_db.get('date_created')
        self.original_payment_date = boleta_db.get('original_payment_date')
        self.source = boleta_db.get('source')
        self.tries = boleta_db.get('tries')
        self.status = boleta_db.get('status')
        self.merchant_id = boleta_db.get('merchant_id')
        self.charges_detail = boleta_db.get('charges_detail')
        self.transaction_details = boleta_db.get('transaction_details')
        self.period = boleta_db.get('period')
        self.plan_id = boleta_db.get('plan_id')
        self.seller_merchant_id = boleta_db.get('seller_merchant_id')
        self.application_fee = boleta_db.get('application_fee')
        self.mail_dates = boleta_db.get('mail_dates')

        self.cliente = cliente
        self.plan = plan
        self.merchant = merchant if merchant and merchant.id == self.seller_merchant_id else None
        self.seller_merchant = merchant if merchant and merchant.id == self.seller_merchant_id else None

    def create(self, source: str, cliente, merchant: Merchant = None, plan: Plan = None):
        self.id = None
        self.cliente = cliente
        self.plan = plan
        self.source = source
        self.merchant = merchant if merchant and merchant.id == self.seller_merchant_id else None
        self.seller_merchant = merchant if merchant and merchant.id == self.seller_merchant_id else None
        self.status = "error_not_processed"
        charges_detail = self.calculate_price()

        if "checkout" in source or "cobro_aon" in source or "pending_accesos" == source:
            opd = today_argentina()
            self.period = get_periodo(opd)
        else:
            opd = cliente.next_payment_date
            self.period = get_periodo(opd + timedelta(days=DIAS_ANTICIPO_DE_PAGO))

        plan = self.get_plan()
        self.member_id = cliente.id
        self.date_created = today_argentina()
        self.original_payment_date = opd
        self.tries = []
        self.status = self.status
        self.charges_detail = charges_detail
        self.merchant_id = plan.merchant_id
        self.seller_merchant_id = None
        self.application_fee = None
        self.period = self.period
        self.plan_id = plan.id
        self.mail_dates = None
        self.update(
            member_id=self.member_id,
            date_created=self.date_created,
            original_payment_date=self.original_payment_date,
            source=self.source,
            tries=self.tries,
            status=self.status,
            merchant_id=self.merchant_id,
            charges_detail=self.charges_detail,
            period=self.period,
            plan_id=self.plan_id
        )

        self.seller_merchant = cliente.get_seller_merchant()
        if self.seller_merchant:
            if plan.es_sportclub_cadena:
                application_fee = self.seller_merchant.get_application_fee(plan.id)
                if application_fee is None:
                    self.update(status='error_application_fee')
                    return
            else:
                application_fee = plan.get_application_fee()
                if application_fee is None:
                    application_fee = self.seller_merchant.get_application_fee_by_cobro(plan.cobro)

            if application_fee > self.final_price:
                application_fee = self.final_price

            self.update(
                application_fee=application_fee,
                seller_merchant_id=self.seller_merchant.id
            )

    @property
    def final_price(self) -> Optional[float]:
        return self.charges_detail.get('final_price') if self.charges_detail else None

    @property
    def last_payment_id(self):
        return self.tries[-1]['payment_id'] if self.tries else None

    def set_status(self, status: str) -> None:
        if self.data["status"] != 'restored' or status == 'approved':
            self.update(status=status)

    def get_cliente(self):
        if not self.cliente:
            from .cliente import Cliente
            db = init_mongo()
            self.cliente = Cliente(db.clientes.find_one(self.member_id))
        return self.cliente

    def get_plan(self) -> Plan:
        if not self.plan:
            db = init_mongo()
            plan_db = db.planes.find_one(self.plan_id)
            self.plan = Plan(plan_db) if plan_db else None
        return self.plan

    def get_merchant(self) -> Merchant:
        if not self.merchant:
            db = init_mongo()
            merchant_db = db.merchants.find_one(self.merchant_id)
            self.merchant = Merchant(db.merchants.find_one(self.merchant_id)) if merchant_db else None
        return self.merchant

    def get_seller_merchant(self) -> Optional[Merchant]:
        if not self.seller_merchant_id:
            return None

        if not self.seller_merchant:
            db = init_mongo()
            seller_merchant_db = db.merchants.find_one(self.seller_merchant_id)
            self.seller_merchant = Merchant(seller_merchant_db) if seller_merchant_db else None
        return self.seller_merchant

    def get_date_last_mail(self) -> Optional[datetime]:
        if self.mail_dates:
            return self.mail_dates[-1]

    def register_mail_date(self) -> None:
        mail_dates = self.mail_dates if self.mail_dates else []
        mail_dates.append(today_argentina())
        self.update(mail_dates=mail_dates)

    def is_restored(self) -> bool:
        return self.status == 'restored'

    def get_last_status(self) -> str:
        return self.tries[-1]['status'] if self.tries else self.status

    def get_last_status_detail(self) -> Optional[str]:
        return self.tries[-1]['status_detail'] if self.tries else None

    def is_marketplace(self) -> bool:
        return self.application_fee is not None and 0 < self.application_fee < self.charges_detail['final_price']

    def calculate_price(self) -> dict:
        plan = self.get_plan()
        plan_price = plan.price
        cliente = self.get_cliente()
        corporativo = cliente.get_corporativo()
        corpo_discount = corporativo.porcentaje_descuento_empleado if corporativo else 0
        sum_access = plan.nivel_de_acceso == "Flex"
        access_count_limit = 6

        if self.source == 'pending_accesos':
            accesos = get_access_amount(cliente.id, max_count=access_count_limit)
            charges_detail = {'final_price': accesos, 'access': accesos}
        else:
            charges_detail = get_client_price(cliente.data, plan_price, corpo_discount,
                                              sum_access=sum_access, access_count_limit=access_count_limit)
            cliente.apply_discounts(plan_price)
        return charges_detail

    def agregar_transaction_details(self, payment: dict) -> None:
        if payment.get('transaction_details'):
            self.update(transaction_details=payment['transaction_details'])

    def agregar_intento(self, payment_result: dict, card: Card) -> None:
        print('     Agregando intento en el array de tries')
        processor = payment_result.get('processor')

        intento = {
            'try_number': len(self.data['tries']) + 1,
            'payment_day': today_argentina(),
            'payment_type': card.card_type,
            'card_brand': card.card_brand,
            'card_id': card.get_id(processor),
            'status': payment_result['status'],
            'status_detail': payment_result['status_detail'],
            'payment_id': payment_result.get('id', 400),
            'processor': processor
        }

        self.tries.append(intento)
        self.update(tries=self.tries)
        self.set_status(intento['status'])

    def agregar_intento_error(self, status_detail: str, processor: str = None, card: Card = Card.empty_card()) -> None:
        print(f"    ERROR: {status_detail}")
        r = {
            "status": "error",
            "status_detail": status_detail
        }
        if processor:
            r['processor'] = processor
        self.agregar_intento(r, card)

    def agregar_intento_precio_cero(self) -> None:
        status_detail = "Pago no realizado por ser precio 0."
        print(f"    {status_detail}")
        r = {
            "status": "approved",
            "status_detail": status_detail,
            "id": 11
        }
        self.agregar_intento(r, Card.empty_card())

    def agregar_intento_pending_efectivo(self) -> None:
        status_detail = "Pago pendiente a pagar efectivo"
        print(f"    {status_detail}")
        r = {
            "status": "pending_efectivo",
            "status_detail": status_detail,
            "id": 11
        }
        self.agregar_intento(r, Card.empty_card())

    def create_payment_data(self, card: Card, card_token: str) -> dict:
        plan = self.get_plan()
        cliente = self.get_cliente()

        n_try = len(self.data['tries']) + 1
        numero_intento = "Primer intento" if n_try == 1 else f"Reintento {n_try}"
        merchant = self.get_merchant()
        seller_merchant = self.get_seller_merchant() if self.seller_merchant_id else merchant
        brand = merchant.get_brand()

        description = f"{brand.name} - {plan.name} - {self.period}"
        if seller_merchant.activate_facturacion:
            description = "Suscripción SportClub"

        payment_data = {
            "additional_info": {
                "items": [{
                    "id": str(plan.id),
                    "title": f'{plan.name} - {cliente.nombre} {cliente.apellido} - {cliente.email} - {self.period}',
                    "category_id": plan.nivel_de_acceso,
                    "description": f'{numero_intento} - id: {cliente.id}'
                }],
                "shipments": {
                    "receiver_address": {
                        "state_name": cliente.domicilio.provincia,
                        "city_name": cliente.domicilio.localidad,
                        "street_name": cliente.domicilio.calle,
                        "street_number": cliente.domicilio.altura,
                    }
                },
                "payer": {
                    "first_name": cliente.nombre,
                    "last_name": cliente.apellido,
                    "address": None
                }
            },
            "notification_url": None if test else f"https://notificaciones.buen.club/notifications"
                                                  f"?source_news=webhooks&merchant={str(seller_merchant.id)}",
            "transaction_amount": round(self.data["charges_detail"]["final_price"], 2),
            "token": card_token,
            "description": description,
            "bin": card.first_six_digits,
            "installments": 1,  # ??
            "payer": cliente.data,
            "external_reference": f'{brand.name} - {self.source} - {cliente.documento}'
        }

        if card.payment_method_id:
            payment_data['payment_method_id'] = card.payment_method_id

        if 'application_fee' in self.data and 0 < self.data['application_fee'] < payment_data['transaction_amount']:
            payment_data['application_fee'] = round(self.data['application_fee'], 2)

        if self.status != 'restored':
            payment_data['point_of_interaction'] = self.calculate_poi()

        return payment_data

    def procesar_pago(self, sdk: SDK, sdk_cadena: SDK, card: Card) -> None:
        card_token = card.tokenize(sdk_cadena) if self.is_marketplace() else card.tokenize(sdk)
        if not card_token:
            self.agregar_intento_error(status_detail='Falló la creación de token de la tarjeta.',
                                       processor=sdk.processor,
                                       card=card)
            return

        print(f'        Token generado OK')

        payment_data = self.create_payment_data(card, card_token)

        if self.application_fee is not None and self.application_fee == self.final_price:
            payment_attempt = sdk_cadena.payment().create(payment_data)
        else:
            payment_attempt = sdk.payment().create(payment_data)

        payment_response = datetime_parser(payment_attempt['response'])
        processor = payment_attempt['response']['processor']

        print("         El estado del pago es: {}".format(payment_response["status"]))
        if "id" in payment_response:
            print("         El id del pago: {}".format(payment_response["id"]))

        # si hay algun error en el pago
        if payment_attempt["status"] >= 299:
            print(payment_response)
            status_detail = payment_response.get('message', 'Falló el intento de pago.')
            self.agregar_intento_error(status_detail=status_detail, processor=processor, card=card)
            return

        # si el pago es 200
        self.agregar_intento(payment_response, card)
        if self.status == 'approved':
            self.agregar_transaction_details(payment_response)

    def pagar(self) -> None:
        if not self.charges_detail:
            self.agregar_intento_error(status_detail='Error al calcular el precio del cliente.')
            return

        if self.charges_detail["final_price"] == 0:
            self.agregar_intento_precio_cero()
            return

        cliente = self.get_cliente()
        if cliente.get_preferred_payment_method() == "efectivo":
            print("    Boleta generada con status pending_efectivo")
            if len(self.tries) == 0 or self.tries[-1]['status'] != 'pending_efectivo':
                self.agregar_intento_pending_efectivo()
            return

        cadena = Merchant.get_cadena()
        marketplace = self.seller_merchant_id is not None
        merchant = self.get_seller_merchant() if marketplace else self.get_merchant()
        if not merchant.processors(marketplace):
            print("    El merchant no tiene ningun prcesador habilitado")
            self.agregar_intento_error(status_detail="no_payment_processor")
            return

        card = cliente.get_card()
        card_processors = cliente.get_card().processors()
        if not card_processors:
            self.agregar_intento_error(status_detail='Card not found', card=card)
            return

        print(f"    Se procede a realizar un pago de ${self.data['charges_detail']['final_price']}")
        print(f'    La tarjeta {card.id} tiene los procesadores: {card_processors}')
        for processor in card_processors:
            print(f'    processor: {processor} | marketplace: {marketplace}')
            sdk = merchant.get_sdk(processor=processor, marketplace=marketplace)
            sdk_cadena = cadena.get_sdk(processor=processor)
            if not sdk.ok():
                print(f'    No se pudo instanciar el SDK {processor} {marketplace}')
                continue

            if not card.get_id(processor):
                self.agregar_intento_error(status_detail='Card not found', card=card)
                continue

            print(f"    Se procede a realizar el pago con {processor}")
            self.procesar_pago(sdk, sdk_cadena, card)
            if self.get_last_status_detail() and ('Payment not found' in self.get_last_status_detail() or
                                                  'Invalid client' in self.get_last_status_detail()):
                print(f"    Hubo un error de tipo Payment not found. "
                      f"    Se borra el poi del cliente y se vuelve a procesar el pago")
                cliente.update(poi=None)
                self.procesar_pago(sdk, sdk_cadena, card)

            if self.get_last_status() in ["approved", "in_process"]:
                break

    def calculate_poi(self) -> dict:
        point_of_interaction = {
            "transaction_data": {}
        }

        cliente = self.get_cliente()
        poi = cliente.poi
        if poi:
            first_time_use = False
            number = poi["installments"] + 1
            subscription_sequence = str(poi["payment_reference"])
            point_of_interaction["transaction_data"]["payment_reference"] = {"id": subscription_sequence}
        else:
            first_time_use = True
            number = 1

        merchant = self.get_seller_merchant() if self.seller_merchant_id else self.get_merchant()

        point_of_interaction["transaction_data"].update({
            "first_time_use": first_time_use,
            "subscription_sequence": {
                "number": number,
                "total": 32
            },
            "invoice_period": {
                "period": number,
                "type": "monthly"
            },
            "billing_date": today_argentina().strftime("%Y-%m-%d"),
            "subscription_id": f"{merchant.application_id}-{cliente.documento}"
        })
        point_of_interaction["type"] = "SUBSCRIPTIONS"

        return point_of_interaction

    def push_to_db(self) -> None:
        db = init_mongo()
        if not self.id:
            r = db.boletas.insert_one(self._to_update)
            self.update(id=r.inserted_id)
            print("Boleta insertada en db", r.inserted_id)
        else:
            r = db.boletas.update_one({"_id": self.id}, {"$set": self._to_update})
            print("Boleta actualizada en db", r.matched_count, r.modified_count)
