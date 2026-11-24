from abc import ABC, abstractmethod


class Pago(ABC):
    """Clase abstracta padre de Efectivo, QR y Tarjeta (igual al diagrama)."""

    def __init__(self, tipo):
        self._monto = 0.0
        self._tipo = str(tipo).strip()

    @property
    def monto(self):
        return self._monto

    @property
    def tipo(self):
        return self._tipo

    @abstractmethod
    def validar_pago(self, monto_total):
        pass

    @abstractmethod
    def procesar_pago(self, monto_total):
        pass


class Efectivo(Pago):
    def __init__(self, monto_recibido):
        super().__init__("Efectivo")
        self._monto_recibido = 0.0
        self._cambio = 0.0
        self.monto_recibido = monto_recibido

    @property
    def monto_recibido(self):
        return self._monto_recibido

    @monto_recibido.setter
    def monto_recibido(self, valor):
        valor = float(valor)
        if valor <= 0:
            raise ValueError("El monto recibido debe ser mayor a 0")
        self._monto_recibido = valor

    @property
    def cambio(self):
        return self._cambio

    def cubrir_total(self, monto_total):
        if self._monto_recibido < monto_total:
            raise ValueError(f"Monto insuficiente. Faltan Bs {round(monto_total - self._monto_recibido, 2)}")
        self._cambio = round(self._monto_recibido - monto_total, 2)
        return self._cambio

    def validar_pago(self, monto_total):
        return self._monto_recibido >= monto_total

    def procesar_pago(self, monto_total):
        self.cubrir_total(monto_total)
        self._monto = round(monto_total, 2)
        return self._monto

    def __str__(self):
        return f"Efectivo (Recibido: Bs {self._monto_recibido:.2f}, Cambio: Bs {self._cambio:.2f})"


class QR(Pago):
    def __init__(self, codigo_10_digitos):
        super().__init__("QR")
        self._codigo_10_digitos = ""
        self.registrar_codigo(codigo_10_digitos)

    @property
    def codigo_10_digitos(self):
        return self._codigo_10_digitos

    def registrar_codigo(self, codigo):
        texto = str(codigo).strip()
        if not texto.isdigit() or len(texto) != 10:
            raise ValueError("El código QR debe tener exactamente 10 dígitos numéricos")
        self._codigo_10_digitos = texto

    def validar_pago(self, monto_total):
        return len(self._codigo_10_digitos) == 10 and self._codigo_10_digitos.isdigit()

    def procesar_pago(self, monto_total):
        if not self.validar_pago(monto_total):
            raise ValueError("Código QR inválido")
        self._monto = round(monto_total, 2)
        return self._monto

    def __str__(self):
        return f"QR (Código: {self._codigo_10_digitos})"


class Tarjeta(Pago):
    PORCENTAJE_COMISION = 0.03

    def __init__(self, numero_ultimos_4="0000"):
        super().__init__("Tarjeta")
        self._numero_ultimos_4 = str(numero_ultimos_4).strip()
        self._comision = 0.0

    @property
    def comision(self):
        return self._comision

    def validar_pago(self, monto_total):
        return monto_total > 0

    def procesar_pago(self, monto_total):
        self._comision = round(monto_total * Tarjeta.PORCENTAJE_COMISION, 2)
        self._monto = round(monto_total + self._comision, 2)
        return self._monto

    def __str__(self):
        return f"Tarjeta (Comisión 3%: Bs {self._comision:.2f})"
