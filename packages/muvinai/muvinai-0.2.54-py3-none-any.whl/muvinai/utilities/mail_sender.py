import base64
from typing import Optional
from datetime import datetime

import iso8601
import mailchimp_transactional as MailchimpTransactional
from bson import ObjectId
from mailchimp_transactional.api_client import ApiClientError

from .dates import today_argentina
from .format import muvi_print
from .init_creds import init_mongo, mailchimp_key, test

mailchimp = MailchimpTransactional.Client(mailchimp_key)


def send_mail_with_attachment(
        files_attachments: list,
        receiver_mail,
        test_mail="matias@muvinai.com",
        global_vars: list = None,
        template: str = 'facturacion',
        brand: dict = None
):
    print("Enviando mail facturacion...")
    if not brand:
        brand = {}
    attachment = []
    try:
        for file in files_attachments:
            with open(file['path'], 'rb') as f:
                file_str = f.read()
                file_str = base64.b64encode(file_str)
                file_str = file_str.decode('utf-8')
            muvi_print('info', 'Archivo adjunto procesado con exito')
            attachment.append({
                'content': file_str,
                'name': file['name'].split('/')[-1],
                'type': file['type'] if 'type' in file else 'application/pdf'
            })
    except:
        return 'error: el archivo no pudo ser encontrado o procesado'

    if test:
        to_mail = [{"email": test_mail}]
    else:
        to_mail = [{"email": receiver_mail}]

    msg = {
        'from_email': brand.get('mail_sender_address'),
        'from_name': brand.get('name'),
        'to': to_mail,
        'global_merge_vars': global_vars if global_vars else [],
        'attachments': attachment
    }
    try:
        response = mailchimp.messages.send_template({
            'template_name': template,
            'template_content': [],
            'message': msg
        })
        print(response)
        return response[0]
    except ApiClientError as error:
        print('An exception occurred: {}'.format(error.text))
        return 'error'


def send_mail_to_template(receiver: dict, template: str, brand: dict, plan_name: str = "None") -> dict:
    """ Enviar mail con un template determinado

    :param receiver: objeto de cliente del destinatario
    :type receiver: dict
    :param template: nombre del template
    :type template: str
    :param brand: brand
    :type brand: dict
    :param plan_name: nombre del plan, defaults to "None"
    :type plan_name: str, optional
    :return: informacion del mail
    :rtype: dict
    """
    try:
        sdate = receiver["last_subscription_date"].strftime("%d/%m/%Y")

    except AttributeError:
        sdate = iso8601.parse_date(receiver["last_subscription_date"]).strftime("%d/%m/%Y")
    except:
        return {}

    global_vars = [{"name": "nombre", "content": receiver["nombre"]},
                   {"name": "apellido", "content": receiver["apellido"]},
                   {"name": "documento", "content": receiver["documento"]},
                   {"name": "plan", "content": plan_name},
                   {"name": "fecha_subscripcion", "content": sdate}
                   ]
    if brand["name"].lower() != "sportclub":
        global_vars.extend([
            {"name": "logo", "content": brand['images']['mail_logo']},
            {"name": "brand_name", "content": brand["name"]}
        ])
    return send_mail(receiver["email"], global_vars, template, brand=brand)


def send_alert(reciever_mail: str, proceso: str, mensaje: str,
               referencia: str, test_mail="matias@muvinai.com") -> Optional[dict]:
    """ Enviar mensaje de alerta a ignacio@muvinai.com
    :param reciever_mail: email de quien recibe la alerta
    :type reciever_mail: str
    :param proceso: nombre del proceso
    :type proceso: str
    :param mensaje: mensaje
    :type mensaje: str
    :param referencia: referencia
    :type referencia: str
    :param test_mail: test_mail
    :type test_mail: str
    :return: Respuesta de mailchimp o None en caso de error
    :rtype: dict | None
    """

    global_vars = [
        {"name": "proceso", "content": proceso},
        {"name": "mensaje", "content": mensaje},
        {"name": "referencia", "content": referencia}
    ]

    brand = {
        "mail_sender_address": "no-responder@sportclub.com.ar",
        "name": "SportClub"
    }
    return send_mail(reciever_mail, global_vars, template="alertas", brand=brand, test_mail=test_mail)


def send_mail_inactivo(receiver: dict, *, brand: dict, sede: str = None, email_contacto: str = None,
                       test_mail='matias@muvinai.com'):
    """ Enviar mail indicando al cliente que está inactivo.

    :param receiver: documento de cliente del destinatario
    :type receiver: dict
    :param brand: brand
    :type brand: dict
    :param sede: sede
    :type sede: dict
    :param email_contacto: email_contacto
    :type email_contacto: str
    :param test_mail: test_mail
    :type brand: str
    :return: informacion del mail
    :rtype: dict
    """
    db = init_mongo()
    template = 'inactivo'
    global_vars = [{'name': 'nombre', 'content': receiver['nombre']}]

    if brand["name"].lower() != "sportclub":
        template = "inactivo-nosc"
        global_vars.extend([
            {"name": "logo", "content": brand["images"]["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]}
        ])
        return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede,
                         email_contacto=email_contacto, test_mail=test_mail)

    merchant_centrales = [doc['_id'] for doc in db.merchants.find({'negocio_central': True}, {'_id': 1})]
    merchant_centrales.append(ObjectId('6178652dcfb117ad58a2cd3d'))

    if receiver.get('status') == 'baja':
        if receiver.get('plan_corporativo', None):
            template = 'inactivacion-por-baja-corpo'
        elif receiver.get('merchant_id') in merchant_centrales and not receiver.get('seller_merchant_id', None):
            template = 'inactivacion-por-baja-corpo-cadena'
            global_vars.extend([{'name': 'checkout_link', 'content': 'https://www.sportclub.com.ar'}])
        else:
            template = 'inactivacion-por-baja-sede'

    if receiver.get('status') == 'activo':
        if receiver.get('merchant_id') in merchant_centrales and not receiver.get('seller_merchant_id', None):
            template = 'inactivaci-n-autom-tica-cadena-corpo'
            global_vars.extend([
                {'name': 'checkout_link', 'content': f"https://www.sportclub.pagar.club/paso2/{receiver.get('slug')}"}
            ])
        else:
            template = 'inactivacion-automatica-sede'

    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede,
                     email_contacto=email_contacto, test_mail=test_mail)


def send_mail(receiver_mail: str, params: list, template: str, *, brand: dict, sede: dict = None,
              email_contacto: str = None, test_mail="matias@muvinai.com", send_at=None):
    """ Estructura y envía mail

    :param receiver_mail: mail del receptor
    :type receiver_mail: str
    :param params: lista de objetos que son parámetros a pasar al template
    :type params: list
    :param template: nombre del template
    :type template: str
    :param brand: brand
    :type brand: dict
    :param sede: sede
    :type sede: dict
    :param email_contacto: email contacto
    :type email_contacto: str
    :param test_mail: mail del receptor en caso de test
    :type receiver_mail: str
    :param send_at: fecha en la cual se debe enviar el mail
    :type send_at: datetime
    :return: informacion del mail
    :rtype: dict
    """
    print("Enviando mail" + template)

    if not 'email_contacto' in [v['name'] for v in params]:
        if not email_contacto:
            email_contacto_sede = sede.get('contact-email') if sede else None
            email_contacto = email_contacto_sede if email_contacto_sede else brand.get('email_contacto')
        if not email_contacto:
            email_contacto = 'info.socios@sportclub.com.ar'
        params.append({'name': 'email_contacto', 'content': email_contacto})

    msg = {
        "from_email": brand["mail_sender_address"],
        "from_name": brand["name"],
        "to": [{"email": test_mail}] if test else [{"email": receiver_mail}],
        "global_merge_vars": params
    }

    try:
        body = {"template_name": template, "template_content": [], "message": msg}
        if send_at:
            body['send_at'] = send_at.strftime('%Y-%m-%d %H:%M:%S')
        response = mailchimp.messages.send_template(body)
        print(response)
        return response[0]
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return {}


def send_mail_carrito_abandonado(receiver_mail: str, client_name: str, plan: dict,
                                 corporativo: dict, cupon_code: str, price: int, *,
                                 brand: dict, sede: dict = None, send_at: datetime = None,
                                 seller_merchant_id: ObjectId = None,
                                 email_contacto: str = None,
                                 test_mail: str = "matias@muvinai.com"):
    """ Enviar mail de carrito abandonado

    :param receiver_mail: email del destinatario
    :type receiver_mail: str
    :param client_name: nombre de cliente del destinatario
    :type client_name: str
    :param plan: plan
    :type plan: dict
    :param corporativo:  corporativo
    :type corporativo: dict
    :param cupon_code: cupon de descuento
    :type cupon_code: str
    :param price: precio del plan
    :type price: int
    :param brand: brand del socio
    :type brand: dict
    :param sede: sede del socio
    :type sede: dict
    :param send_at: fecha en la cual se debe enviar el mail
    :type send_at: datetime
    :param seller_merchant_id: seller_merchant_id
    :type seller_merchant_id: ObjectId
    :param email_contacto: email_contacto
    :type email_contacto: str
    :param test_mail: test_mail
    :type test_mail: str
    :return: informacion del mail
    :rtype: dict
    """
    url_slug = corporativo['slug'] if corporativo else plan['slug']

    base_url = f"https://www.sportclub.pagar.club/paso2/{url_slug}"
    campaign = "utm_source=checkout&utm_medium=email&utm_campaign=carrito_abandonado"

    if cupon_code:
        url = f"{base_url}?code={cupon_code}&{campaign}"
    elif seller_merchant_id:
        url = f"{base_url}?seller_merchant_id={seller_merchant_id}&{campaign}"
    else:
        url = f"{base_url}?{campaign}"

    global_vars = [
        {"name": "corpo", "content": corporativo.get('slug') if corporativo else None},
        {"name": "name", "content": client_name},
        {"name": "plan", "content": plan['name']},
        {"name": "price", "content": price},
        {"name": "the_url", "content": url}
    ]
    if brand["name"] != "SportClub":
        return

    template = "carrito-abandonado"
    return send_mail(receiver_mail, global_vars, template, brand=brand, sede=sede, send_at=send_at,
                     email_contacto=email_contacto, test_mail=test_mail)


def cancel_scheduled_email(email_id: str):
    """ Enviar mail de carrito abandonado

    :param email_id: id del email a cancelar
    :type email_id: str
    :return: informacion del email cancelado
    :rtype: dict
    """
    try:
        response = mailchimp.messages.cancel_scheduled({'id': email_id})
        print(response)
        return response
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return {}


def cancel_all_scheduled_email_from(email: str):
    """ Enviar mail de carrito abandonado

    :param email: email del destinatario
    :type email: str
    :return: lista de emails cancelados
    :rtype: list
    """
    canceled = []
    emails = mailchimp.messages.list_scheduled({'to': email})
    if isinstance(emails, list):
        for e in emails:
            canceled.append(cancel_scheduled_email(e['_id']))
    return canceled


def send_mail_cambio_tarjeta(receiver: dict, *, brand: dict, sede: dict = None, email_contacto: str = None):
    """ Enviar mail indicando al cliente que debe cambiar la tarjeta.

            :param receiver: documento de cliente del destinatario
            :type receiver: dict
            :param brand: brand
            :type brand: dict
            :param sede: sede
            :type sede: dict
            :param email_contacto: email_contacto
            :type email_contacto: str
            :return: informacion del mail
            :rtype: dict
            """
    fecha_vigencia = receiver["fecha_vigencia"].strftime("%d/%m/%Y")
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "fecha_vigencia", "content": fecha_vigencia}
    ]

    if brand["name"].lower() == "sportclub":
        template = "pago-rechazado"
    elif brand["name"].lower() == "aranceles":
        return
    elif brand["name"].upper() == "AON":
        template = "cambio_de_tarjeta_aon"
        global_vars = [
            {'name': 'nombre', 'content': receiver['name']},
        ]
    else:
        template = "pago-rechazado-nosc"
        global_vars.extend([
            {"name": "horizontal_white", "content": brand['images']["horizontal_white"]},
            {"name": "image_dark", "content": brand['images']["image_dark"]},
            {"name": "image_light", "content": brand['images']["image_light"]},
            {"name": "brand_name", "content": brand["name"]}
        ])

    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede, email_contacto=email_contacto)


def send_mail_bienvenida(receiver: dict, *, plan: dict, brand: dict, sede: dict = None,
                         email_contacto: str = None, test_mail: str = "ignacio@muvinai.com"):
    """ Enviar mail de bienvenida a la suscripción.

    :param receiver: documento de cliente del destinatario
    :type receiver: dict
    :param plan: plan
    :type plan: dict
    :param brand: brand
    :type brand: dict
    :param sede: sede
    :type sede: dict
    :param email_contacto: email_contacto
    :type email_contacto: str
    :param test_mail: test_mail
    :type test_mail: dict
    :return: informacion del mail
    :rtype: dict
    """
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "apellido", "content": receiver["apellido"]},
        {"name": "documento", "content": receiver["documento"]},
        {"name": "plan", "content": plan["name"]},
        {"name": "fecha_subscripcion", "content": today_argentina().strftime("%d/%m/%Y")},
    ]

    if plan["sede_local"]:
        db = init_mongo()
        sede = db.club.find_one({"_id": plan["sede_local"]})
        global_vars.extend([
            {"name": "direccion", "content": sede["direccion"]},
            {"name": "telefono", "content": sede["telefono"]},
            {"name": "contact-email", "content": sede["contact-email"]}
        ])
        if "instagram" in sede.keys():
            global_vars.append({"name": "instagram", "content": sede["instagram"]})

    if brand["name"].lower() == 'sportclub':
        if plan["nivel_de_acceso"] == "Full" or plan["nivel_de_acceso"] == "Flex":
            template = "workclub-bienvenida"
        elif plan["nivel_de_acceso"] == "Local":
            template = "bienvenida-local"
        else:
            template = "bienvenida"
    else:
        template = "bienvenida-nosc"
        global_vars.extend([
            {"name": "logo_mails", "content": brand['images']['mail_logo']},
            {"name": "brand_name", "content": brand["name"]}
        ])

    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede,
                     email_contacto=email_contacto, test_mail=test_mail)


def send_mail_exitoso(receiver: dict, *, plan: dict, brand: dict, sede: dict = None, email_contacto: str = None):
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "apellido", "content": receiver["apellido"]},
        {"name": "plan", "content": plan["name"]},
        {"name": "fecha_subscripcion", "content": today_argentina().strftime("%d/%m/%Y")}
    ]

    if brand["name"].lower() == "sportclub":
        template = "exitoso"
    else:
        template = "exitoso-nosc"
        global_vars.extend([
            {"name": "logo_mails", "content": brand['images']["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]}
        ])

    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede, email_contacto=email_contacto)


def send_mail_checkout_rechazado(receiver: dict, *, plan: dict, brand: dict, sede: dict = None,
                                 email_contacto: str = None):
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "slug", "content": plan["slug"]}
    ]

    if brand["name"].lower() == "sportlub":
        template = "checkout-rechazado"
    else:
        template = "checkout-rechazado-nosc"
        global_vars.extend([
            {"name": "logo_mails", "content": brand['images']["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]}
        ])

    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede, email_contacto=email_contacto)


def send_mail_pago_en_efectivo(receiver: dict, *, final_price: float, plan_name: str, brand: dict, sede: dict = None,
                               email_contacto: str = None):
    global_vars = [
        {
            "name": "nombre",
            "content": receiver["nombre"],
        }, {
            "name": "precio_total",
            "content": final_price
        }, {
            "name": "plan",
            "content": plan_name
        }
    ]
    if brand["name"].lower() == "sportclub":
        template = "nueva-boleta"
    else:
        template = "nueva-boleta-nosc"
        global_vars.extend([
            {"name": "logo", "content": brand['images']["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]}
        ])
    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede, email_contacto=email_contacto)


def send_mail_pago_pendiente(receiver: dict, *, brand: dict, sede: dict = None,
                             email_contacto: str = None, test_mail="ignacio@muvinai.com"):
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]}
    ]
    if brand["name"].lower() == "sportclub":
        template = "pago-pendiente"
    else:
        template = "pago-pendiente-nosc"
        global_vars.extend([
            {"name": "logo", "content": brand['images']["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]}
        ])
    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede,
                     email_contacto=email_contacto, test_mail=test_mail)


def send_mail_cambio_tarjeta_aon(receiver: dict, *, brand: dict, sede: dict = None, email_contacto: str = None):
    """ Enviar mail indicando al cliente que debe cambiar la tarjeta.

    :param receiver: documento de cliente del destinatario
    :type receiver: dict
    :param brand: brand
    :type brand: dict
    :param sede: sede
    :type sede: dict
    :param email_contacto: email_contacto
    :type email_contacto: str
    :return: informacion del mail
    :rtype: dict
    """
    template = "cambio-de-tarjeta-aon"
    global_vars = [
        {'name': 'nombre', 'content': receiver['name']},
    ]

    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede, email_contacto=email_contacto)


def send_mail_vencimiento_anual(receiver: dict, *, brand: dict, sede: dict = None, email_contacto: str = None):
    """ Enviar mail indicando al cliente que debe cambiar la tarjeta.

    :param receiver: documento de cliente del destinatario
    :type receiver: dict
    :param brand: brand
    :type brand: dict
    :param sede: sede
    :type sede: dict
    :param email_contacto: email_contacto
    :type email_contacto: str
    :return: informacion del mail
    :rtype: dict
    """
    template = "vencimiento-anual"
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "apellido", "content": receiver["apellido"]},
        {"name": "plan", "content": receiver["plan"]["name"]},
        {"name": "fecha_vigencia", "content": receiver["fecha_vigencia"].strftime("%d/%m/%Y")},
    ]
    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede, email_contacto=email_contacto)


def send_mail_cambio_plan_herenecia(receiver: dict, *, brand: dict, sede: dict = None, email_contacto: str = None):
    template = "vencimiento-anual-herencia"
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "apellido", "content": receiver["apellido"]},
        {"name": "precio_mensual", "content": receiver["plan"]['price']},
        {"name": "plan", "content": receiver["plan"]["name"]},
        {"name": "plan_herencia", "content": receiver["plan_herencia"]["name"]},
        {"name": "fecha_vigencia", "content": receiver["fecha_vigencia"].strftime("%d/%m/%Y")},
        {"name": "precio_plan_herencia", "content": receiver['plan_herencia']['price']},
        {"name": "frecuencia", "content": receiver['plan_herencia']['cobro'].lower()}
    ]
    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede, email_contacto=email_contacto)


def send_mail_baja(receiver: dict, *, template: str, brand: dict, sede: dict = None, email_contacto: str = None):
    """ Enviar mail indicando al cliente que está en estado baja.

    :param receiver: documento de cliente del destinatario
    :type receiver: dict
    :param template: nombre del template de mailchimp
    :type template: str
    :param brand: brand
    :type brand: dict
    :param sede: sede
    :type sede: dict
    :param email_contacto: email_contacto
    :type email_contacto: str
    :return: informacion del mail
    :rtype: dict
    """
    planes_url = 'https://www.sportclub.com.ar/#planes'
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "checkout_link", "content": planes_url}
    ]

    return send_mail(receiver["email"], global_vars, template, brand=brand, sede=sede, email_contacto=email_contacto)
