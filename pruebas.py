from modelo.productos import Producto, Plato, Bebida, Combo
from modelo.clientes import Cliente
from modelo.pedidos import Pedido, Local, ParaLlevar, Delivery
from modelo.pagos import Pago, Efectivo, QR, Tarjeta
from restaurante import Restaurante


def ejecutar_pruebas():
    print("Iniciando pruebas unitarias de la Variante A...")

    for clase_abs in (Producto, Pedido, Pago):

        try:
            clase_abs("Prueba")
            assert False, f"{clase_abs.__name__} no debería instanciarse"
        except TypeError:
            pass

    try:
        Cliente("Juan", "51234567")
        assert False
    except ValueError:
        pass

    cliente = Cliente("Amner", "71234567")
    assert cliente.nombre == "Amner"

    silpancho = Plato("Silpancho", 35.0)
    chicharron = Plato("Chicharrón", 45.0, ["domingo"])
    mocochinchi_vaso = Bebida("Mocochinchi", 6.0, "vaso")
    mocochinchi_jarra = Bebida("Mocochinchi Jarra", 6.0, "jarra")

    assert mocochinchi_jarra.calcular_precio() == 18.0
    assert chicharron.esta_disponible("domingo") is True
    assert chicharron.esta_disponible("lunes") is False

    combo_valluno = Combo("Combo Valluno", [silpancho, mocochinchi_vaso])
    assert combo_valluno.calcular_precio() == 36.90

    sopa_mani = Plato("Sopa de Maní", 15.0)
    super_combo = Combo("Super Combo", [combo_valluno, sopa_mani])
    assert super_combo.calcular_precio() == 46.71
    assert super_combo.contar_platos() == 2

    rest = Restaurante()
    p_llevar = rest.crear_pedido_para_llevar(cliente, "domingo")
    p_llevar.agregar_producto(super_combo, 1)
    assert p_llevar.calcular_cargos() == 4.0
    assert p_llevar.calcular_total() == 50.71

    p_delivery = rest.crear_pedido_delivery(cliente, "Quillacollo", "domingo")
    p_delivery.agregar_producto(combo_valluno, 2)
    assert p_delivery.calcular_total() == 88.80

    p_cercado_gratis = rest.crear_pedido_delivery(cliente, "Cercado", "domingo")
    p_cercado_gratis.agregar_producto(silpancho, 5)
    assert p_cercado_gratis.calcular_cargos() == 0.0

    try:
        p_delivery.registrar_pago(Tarjeta("1234"))
        assert False
    except ValueError:
        pass

    pago_ef = Efectivo(100.0)
    p_delivery.registrar_pago(pago_ef)
    assert pago_ef.cambio == 11.20

    p_delivery.cambiar_estado("EN_PREPARACION")
    try:
        p_delivery.cancelar_pedido()
        assert False
    except ValueError:
        pass

    print("¡TODAS LAS 8 PRUEBAS PASARON CON ÉXITO!")


if __name__ == "__main__":
    ejecutar_pruebas()
