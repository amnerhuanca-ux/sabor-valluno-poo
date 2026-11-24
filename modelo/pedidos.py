from abc import ABC, abstractmethod
from modelo.productos import Producto
from modelo.clientes import Cliente
from modelo.pagos import Pago


class ProductoPedido:
    """Clase intermedia: relaciona un Producto con un Pedido y su cantidad."""

    def __init__(self, pedido, producto, cantidad=1):
        if not isinstance(producto, Producto):
            raise ValueError("El ítem debe ser un Producto válido")
        self._pedido = pedido
        self._producto = producto
        self._cantidad = 0
        self.cantidad = cantidad

    @property
    def pedido(self):
        return self._pedido

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        try:
            cant = int(valor)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número entero")
        if cant < 1 or cant > 20:
            raise ValueError("La cantidad de un producto en el pedido debe estar entre 1 y 20")
        self._cantidad = cant

    def subtotal_item(self):
        return round(self._producto.calcular_precio() * self._cantidad, 2)

    def total_platos_item(self):
        return self._producto.contar_platos() * self._cantidad


class Pedido(ABC):
    """Clase abstracta base para todos los tipos de pedido."""

    ESTADOS_VALIDOS = ["REGISTRADO", "EN_PREPARACION", "LISTO", "ENTREGADO", "CANCELADO"]
    TRANSICIONES = {
        "REGISTRADO": ["EN_PREPARACION", "CANCELADO"],
        "EN_PREPARACION": ["LISTO"],
        "LISTO": ["ENTREGADO"],
        "ENTREGADO": [],
        "CANCELADO": []
    }

    def __init__(self, n_pedido, cliente, dia_semana="domingo"):
        if not isinstance(cliente, Cliente):
            raise ValueError("Debe asignar un Cliente válido al pedido")
        self._n_pedido = int(n_pedido)
        self._cliente = cliente
        self._dia_semana = dia_semana
        self._estado = "REGISTRADO"
        self._items = []
        self._pagos = []

    @property
    def n_pedido(self):
        return self._n_pedido

    @property
    def cliente(self):
        return self._cliente

    @property
    def estado(self):
        return self._estado

    @property
    def items(self):
        return list(self._items)

    @property
    def pagos(self):
        return list(self._pagos)

    def _verificar_editable(self):
        if self._estado != "REGISTRADO":
            raise ValueError("Solo se pueden agregar o quitar productos cuando el pedido está en REGISTRADO")

    def agregar_producto(self, producto, cantidad=1):
        self._verificar_editable()
        if not producto.esta_disponible(self._dia_semana):
            raise ValueError(f"El producto '{producto.nombre}' no está disponible el día {self._dia_semana}")

        for item in self._items:
            if item.producto is producto:
                item.cantidad = item.cantidad + cantidad
                return

        nuevo_item = ProductoPedido(self, producto, cantidad)
        self._items.append(nuevo_item)

    def quitar_producto(self, nombre_producto):
        self._verificar_editable()
        for item in self._items:
            if item.producto.nombre.lower() == nombre_producto.strip().lower():
                self._items.remove(item)
                return
        raise ValueError(f"El producto '{nombre_producto}' no está en el pedido")

    def cambiar_estado(self, nuevo_estado):
        nuevo = str(nuevo_estado).strip().upper()
        if nuevo not in Pedido.TRANSICIONES.get(self._estado, []):
            raise ValueError(f"Transición inválida: no se puede pasar de {self._estado} a {nuevo}")
        self._estado = nuevo

    def cancelar_pedido(self):
        self.cambiar_estado("CANCELADO")

    def registrar_pedido(self):
        if len(self._items) == 0:
            raise ValueError("No se puede confirmar un pedido vacío")
        self._validar_reglas_especificas()

    def _validar_reglas_especificas(self):
        pass

    def calcula_subtotal(self):
        total = 0.0
        for item in self._items:
            total += item.subtotal_item()
        return round(total, 2)

    def contar_total_platos(self):
        platos = 0
        for item in self._items:
            platos += item.total_platos_item()
        return platos

    @abstractmethod
    def calcular_cargos(self):
        pass

    def permite_metodo_pago(self, tipo_pago):
        return True

    def calcular_total(self):
        return round(self.calcula_subtotal() + self.calcular_cargos(), 2)

    def registrar_pago(self, pago):
        if self._estado == "CANCELADO":
            raise ValueError("No se puede cobrar un pedido cancelado")
        if len(self._items) == 0:
            raise ValueError("El pedido no tiene productos")
        self._validar_reglas_especificas()
        if not self.permite_metodo_pago(pago.tipo):
            raise ValueError(f"El pedido {type(self).__name__} no acepta pago con {pago.tipo}")
        pago.procesar_pago(self.calcular_total())
        self._pagos.append(pago)
        return pago


class Local(Pedido):
    MESAS_MIN = 1
    MESAS_MAX = 15

    def __init__(self, n_pedido, cliente, n_mesa, dia_semana="domingo"):
        super().__init__(n_pedido, cliente, dia_semana)
        self._n_mesa = 0
        self.n_mesa = n_mesa

    @property
    def n_mesa(self):
        return self._n_mesa

    @n_mesa.setter
    def n_mesa(self, valor):
        mesa = int(valor)
        if mesa < Local.MESAS_MIN or mesa > Local.MESAS_MAX:
            raise ValueError("El número de mesa debe estar entre 1 y 15")
        self._n_mesa = mesa

    def calcular_cargos(self):
        return 0.0

    def __str__(self):
        return f"Pedido Local #{self._n_pedido} - Mesa {self._n_mesa} ({self._estado})"


class ParaLlevar(Pedido):
    COSTO_ENVASE_POR_PLATO = 2.0

    def __init__(self, n_pedido, cliente, dia_semana="domingo"):
        super().__init__(n_pedido, cliente, dia_semana)

    @property
    def n_envases(self):
        return self.contar_total_platos()

    def calcular_cargo(self, n_e=None):
        cantidad = self.n_envases if n_e is None else int(n_e)
        return round(cantidad * ParaLlevar.COSTO_ENVASE_POR_PLATO, 2)

    def calcular_cargos(self):
        return self.calcular_cargo()

    def __str__(self):
        return f"Pedido Para Llevar #{self._n_pedido} - Envases: {self.n_envases} ({self._estado})"


class Delivery(Pedido):
    TARIFAS_ZONA = {
        "cercado": 8.0,
        "quillacollo": 15.0,
        "sacaba": 15.0,
        "vinto": 20.0
    }
    PEDIDO_MINIMO = 40.0
    MONTO_ENVIO_GRATIS_CERCADO = 150.0

    def __init__(self, n_pedido, cliente, zona, dia_semana="domingo"):
        super().__init__(n_pedido, cliente, dia_semana)
        self._zona = ""
        self.zona = zona

    @property
    def zona(self):
        return self._zona

    @zona.setter
    def zona(self, valor):
        z = str(valor).strip().lower()
        if z not in Delivery.TARIFAS_ZONA:
            raise ValueError(f"Zona no válida. Zonas permitidas: {list(Delivery.TARIFAS_ZONA.keys())}")
        self._zona = z

    @property
    def costo_minimo(self):
        return Delivery.PEDIDO_MINIMO

    def _validar_reglas_especificas(self):
        if self.calcula_subtotal() < Delivery.PEDIDO_MINIMO:
            raise ValueError(f"El pedido mínimo para Delivery es de Bs {Delivery.PEDIDO_MINIMO:.2f}")

    def calcular_costo_envio(self, zona=None):
        z = self._zona if zona is None else str(zona).strip().lower()
        if z not in Delivery.TARIFAS_ZONA:
            raise ValueError("Zona desconocida")
        if z == "cercado" and self.calcula_subtotal() >= Delivery.MONTO_ENVIO_GRATIS_CERCADO:
            return 0.0
        return Delivery.TARIFAS_ZONA[z]

    def calcular_cargos(self):
        return self.calcular_costo_envio()

    def permite_metodo_pago(self, tipo_pago):
        return str(tipo_pago).strip().lower() in ("efectivo", "qr")

    def __str__(self):
        return f"Pedido Delivery #{self._n_pedido} - Zona: {self._zona.capitalize()} ({self._estado})"
