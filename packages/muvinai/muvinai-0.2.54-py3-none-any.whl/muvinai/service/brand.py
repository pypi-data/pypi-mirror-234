from bson import ObjectId

from muvinai.utilities.init_creds import init_mongo


class Brand:
    db = init_mongo()
    brands = None

    @classmethod
    def _get_brands(cls) -> dict:
        if not cls.brands:
            db = init_mongo()
            cls.brands = {b['_id']: b for b in db.brands.find({})}
        return cls.brands

    @classmethod
    def get(cls, _id: ObjectId = None, name: str = None):
        if not _id and not name:
            return
        db = init_mongo()
        if _id:
            brand_db = db.brands.find_one(_id)
            return Brand(brand_db) if brand_db else None

        brand_db = db.brands.find_one({'name': name})
        return Brand(brand_db) if brand_db else None

    @classmethod
    def search(cls, names: list = None) -> list:
        brands = cls._get_brands()
        if names:
            return [Brand(brand) for brand in brands.values() if brand['name'] in names]

        return [Brand(brand) for brand in brands.values()]

    def __init__(self, brand_db):
        self.brand_db = brand_db
        self.name = brand_db['name']
        self.id = brand_db['_id']

    def get_merchants(self) -> list:
        from .merchant import Merchant
        return [Merchant(merchant_db, brand=self) for merchant_db in self.db.merchants.find({'brand_id': self.id})]
