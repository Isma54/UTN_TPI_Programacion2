class FoodStoreError(Exception):
    pass

class EntidadNoEncontradaError(FoodStoreError):
    pass

class DatoInvalidoError(FoodStoreError):
    pass

class PrecioInvalidoError(DatoInvalidoError):
    pass

class StockInvalidoError(DatoInvalidoError):
    pass

class StockInsuficienteError(FoodStoreError):
    pass

class DuplicadoError(FoodStoreError):
    pass

class OperacionNoPermitidaError(FoodStoreError):
    pass

class CredencialesInvalidasError(FoodStoreError):
    pass