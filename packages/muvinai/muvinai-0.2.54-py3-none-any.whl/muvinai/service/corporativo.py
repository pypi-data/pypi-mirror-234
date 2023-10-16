class Corporativo:
    def __init__(self, corporativo_db):
        self.corporativo_db = corporativo_db
        self.id = corporativo_db['_id']
        self.porcentaje_descuento_empleado = corporativo_db['porcentaje-descuento-empleado']
