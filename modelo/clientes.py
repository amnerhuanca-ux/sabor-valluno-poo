class Cliente:
    """Representa un cliente del restaurante con validación de teléfono."""

    def __init__(self, nombre, telefono):
        self._nombre = ""
        self._telefono = ""
        self.nombre = nombre
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        texto = str(valor).strip()
        if texto == "":
            raise ValueError("El nombre del cliente no puede estar vacío")
        self._nombre = texto

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).strip()
        if not texto.isdigit() or len(texto) != 8 or not texto.startswith(("6", "7")):
            raise ValueError("El teléfono debe tener 8 dígitos y empezar con 6 o 7")
        self._telefono = texto

    def __str__(self):
        return f"{self._nombre} (Tel: {self._telefono})"
