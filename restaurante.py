from modelo.productos import Producto, Plato, Bebida, Combo
from modelo.clientes import Cliente
from modelo.pedidos import Pedido, Local, ParaLlevar, Delivery


class Restaurante:
    """Clase gestora que administra el menú, clientes y pedidos de Sabor Valluno."""

    def __init__(self, nombre="Sabor Valluno"):
        self._nombre = nombre
        self._menu = []
        self._clientes = []
        self._pedidos = []
        self._contador_pedidos = 1

    @property
    def nombre(self):
        return self._nombre

    @property
    def menu(self):
        return list(self._menu)

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def pedidos(self):
        return list(self._pedidos)

    def registrar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise ValueError("Solo se pueden registrar objetos de tipo Producto")
        for p in self._menu:
            if p.nombre.lower() == producto.nombre.lower():
                raise ValueError(f"Ya existe un producto llamado '{producto.nombre}'")
        self._menu.append(producto)
        return producto

    def buscar_producto(self, nombre):
        for producto in self._menu:
            if producto.nombre.lower() == str(nombre).strip().lower():
                return producto
        raise ValueError(f"Producto '{nombre}' no encontrado en el menú")

    def listar_menu_disponible(self, dia):
        disponibles = []
        for producto in self._menu:
            if producto.esta_disponible(dia):
                disponibles.append(producto)
        return disponibles

    def registrar_cliente(self, nombre, telefono):
        for c in self._clientes:
            if c.telefono == str(telefono).strip():
                raise ValueError(f"Ya existe un cliente registrado con el teléfono {telefono}")
        nuevo_cliente = Cliente(nombre, telefono)
        self._clientes.append(nuevo_cliente)
        return nuevo_cliente

    def buscar_cliente_por_telefono(self, telefono):
        for cliente in self._clientes:
            if cliente.telefono == str(telefono).strip():
                return cliente
        raise ValueError(f"No se encontró ningún cliente con el teléfono {telefono}")

    def _verificar_mesa_disponible(self, n_mesa):
        estados_cerrados = ("ENTREGADO", "CANCELADO")
        for pedido in self._pedidos:
            if isinstance(pedido, Local) and pedido.n_mesa == int(n_mesa):
                if pedido.estado not in estados_cerrados:
                    raise ValueError(f"La mesa {n_mesa} ya tiene un pedido abierto (#{pedido.n_pedido})")

    def crear_pedido_local(self, cliente, n_mesa, dia="domingo"):
        self._verificar_mesa_disponible(n_mesa)
        pedido = Local(self._contador_pedidos, cliente, n_mesa, dia)
        self._pedidos.append(pedido)
        self._contador_pedidos += 1
        return pedido

    def crear_pedido_para_llevar(self, cliente, dia="domingo"):
        pedido = ParaLlevar(self._contador_pedidos, cliente, dia)
        self._pedidos.append(pedido)
        self._contador_pedidos += 1
        return pedido

    def crear_pedido_delivery(self, cliente, zona, dia="domingo"):
        pedido = Delivery(self._contador_pedidos, cliente, zona, dia)
        self._pedidos.append(pedido)
        self._contador_pedidos += 1
        return pedido

    def buscar_pedido(self, n_pedido):
        for pedido in self._pedidos:
            if pedido.n_pedido == int(n_pedido):
                return pedido
        raise ValueError(f"No existe el pedido #{n_pedido}")

    def reporte_ventas_por_tipo(self):
        resumen = {"Local": 0.0, "ParaLlevar": 0.0, "Delivery": 0.0}
        for pedido in self._pedidos:
            if pedido.estado != "CANCELADO" and len(pedido.pagos) > 0:
                tipo = type(pedido).__name__
                if tipo in resumen:
                    resumen[tipo] = round(resumen[tipo] + pedido.calcular_total(), 2)
        return resumen

    def top_3_productos_mas_vendidos(self):
        conteo = {}
        for pedido in self._pedidos:
            if pedido.estado != "CANCELADO":
                for item in pedido.items:
                    nombre = item.producto.nombre
                    conteo[nombre] = conteo.get(nombre, 0) + item.cantidad

        ordenados = sorted(conteo.items(), key=lambda x: x, reverse=True)
        return ordenados[:3]
