from .merchandise import TransactionalMerchandise, TransactionalMerchandiseDelta

class Service(TransactionalMerchandise):
    pass

class ServiceDelta(TransactionalMerchandiseDelta):
    pass
