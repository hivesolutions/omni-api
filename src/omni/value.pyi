from .named import Named, NamedDelta

class Value(Named):
    value: float

class ValueDelta(NamedDelta):
    value: float
