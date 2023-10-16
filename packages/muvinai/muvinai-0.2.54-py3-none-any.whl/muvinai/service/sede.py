class Sede:
    def __init__(self, sede_db):
        self.sede_db = sede_db
        self.id = sede_db['_id']
        self.email_contacto = sede_db.get('contact-email')
