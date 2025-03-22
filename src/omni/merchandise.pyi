from .named import Named

class Merchandise(Named):
    pass

class TransactionalMerchandise(Merchandise):
    company_product_code: str
