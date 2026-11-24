from abc import ABC, abstractmethod

DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def normalizar_dia(dia):
    """Convierte 'Sábado' o 'MIÉRCOLES' en 'sabado' o 'miercoles'."""
    texto = str(dia).strip().lower()
    texto = texto.replace("á", "a").replace("é", "e")
    return texto


class Producto(ABC):
    """Clase abstracta: todo lo que se puede vender."""

    def __init__(self, nombre):
        self._nombre = ""
        self.nombre = nombre

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()
        if valor == "":
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor

    @property
    def precio_pedido(self):
        """Precio con el que el producto entra a un pedido."""
        return self.calcular_precio()

    def _validar_precio(self, precio):
        try:
            valor = float(precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número")
        if valor <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return valor

    def contiene(self, otro):
        """Un producto simple solo 'contiene' a sí mismo (Combo lo redefine)."""
        return self is otro

    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def esta_disponible(self, dia):
        pass

    @abstractmethod
    def contar_platos(self):
        pass


class Plato(Producto):
    def __init__(self, nombre, precio, dias_disponible=None):
        super().__init__(nombre)
        self._precio = 0
        self._dias_disponible = []
        self.precio = precio
        self.dias_disponible = dias_disponible

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = self._validar_precio(valor)

    @property
    def dias_disponible(self):
        return list(self._dias_disponible)

    @dias_disponible.setter
    def dias_disponible(self, dias):
        if dias is None:
            dias = []
        lista = []
        for dia in dias:
            dia = normalizar_dia(dia)
            if dia not in DIAS_SEMANA:
                raise ValueError("Día no válido: " + dia)
            lista.append(dia)
        self._dias_disponible = lista

    def calcular_precio(self):
        return self._precio

    def esta_disponible(self, dia):
        if len(self._dias_disponible) == 0:
            return True
        return normalizar_dia(dia) in self._dias_disponible

    def contar_platos(self):
        return 1

    def __str__(self):
        return self._nombre


class Bebida(Producto):
    FACTORES = {"vaso": 1, "jarra": 3}

    def __init__(self, nombre, precio_vaso, tipo="vaso"):
        super().__init__(nombre)
        self._precio_vaso = 0
        self._tipo = "vaso"
        self.precio_vaso = precio_vaso
        self.tipo = tipo

    @property
    def precio_vaso(self):
        return self._precio_vaso

    @precio_vaso.setter
    def precio_vaso(self, valor):
        self._precio_vaso = self._validar_precio(valor)

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        texto = str(valor).strip().lower()
        if texto not in Bebida.FACTORES:
            raise ValueError("El tipo de bebida debe ser 'vaso' o 'jarra'")
        self._tipo = texto

    def calcular_precio(self):
        return round(self._precio_vaso * Bebida.FACTORES[self._tipo], 2)

    def esta_disponible(self, dia):
        return True

    def contar_platos(self):
        return 0

    def __str__(self):
        return self._nombre


class ComboProductos:
    """Clase intermedia: une un Combo con uno de sus Productos."""

    def __init__(self, combo, producto):
        self._combo = combo
        self._producto = producto

    @property
    def combo(self):
        return self._combo

    @property
    def producto(self):
        return self._producto


class Combo(Producto):
    # Constante fácil de cambiar en la defensa (Variante A = 10%)
    DESCUENTO = 0.10

    def __init__(self, nombre, productos):
        super().__init__(nombre)
        self._items = []
        for producto in productos:
            self.agregar_producto(producto)
        if len(self._items) < 2:
            raise ValueError("Un combo debe tener al menos 2 productos")

    @property
    def productos(self):
        return [item.producto for item in self._items]

    def agregar_producto(self, producto):
        if producto.contiene(self):
            raise ValueError("Un combo no puede contenerse a sí mismo")
        self._items.append(ComboProductos(self, producto))

    def contiene(self, otro):
        if self is otro:
            return True
        for item in self._items:
            if item.producto.contiene(otro):
                return True
        return False

    def calcular_precio(self):
        suma = 0
        for item in self._items:
            suma += item.producto.calcular_precio()
        return round(suma * (1 - Combo.DESCUENTO), 2)

    def esta_disponible(self, dia):
        for item in self._items:
            if not item.producto.esta_disponible(dia):
                return False
        return True

    def contar_platos(self):
        total = 0
        for item in self._items:
            total += item.producto.contar_platos()
        return total

    def __str__(self):
        return self._nombre
