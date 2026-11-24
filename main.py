from modelo.productos import Plato, Bebida, Combo
from modelo.pagos import Efectivo, QR, Tarjeta
from restaurante import Restaurante


def cargar_datos_iniciales(restaurante):
    silpancho = Plato("Silpancho", 35.0)
    pique = Plato("Pique Macho", 45.0)
    chicharron = Plato("Chicharron", 45.0, ["domingo"])
    sopa = Plato("Sopa de Mani", 15.0)

    moco_vaso = Bebida("Mocochinchi Vaso", 6.0, "vaso")
    moco_jarra = Bebida("Mocochinchi Jarra", 6.0, "jarra")
    soda = Bebida("Gaseosa", 8.0, "vaso")

    combo1 = Combo("Combo Valluno", [silpancho, moco_vaso])
    combo2 = Combo("Combo Familiar", [combo1, pique, moco_jarra])

    for prod in [silpancho, pique, chicharron, sopa, moco_vaso, moco_jarra, soda, combo1, combo2]:
        restaurante.registrar_producto(prod)


def mostrar_detalle_pedido(pedido):
    print("\n" + "=" * 45)
    print(f"DETALLE DEL {pedido}")
    print(f"Cliente: {pedido.cliente}")
    print("-" * 45)
    for item in pedido.items:
        print(f" - {item.cantidad}x {item.producto.nombre}: Bs {item.subtotal_item():.2f}")
    print("-" * 45)
    print(f"Subtotal:         Bs {pedido.calcula_subtotal():.2f}")
    print(f"Cargos extra:     Bs {pedido.calcular_cargos():.2f}")
    print(f"TOTAL A PAGAR:    Bs {pedido.calcular_total():.2f}")
    print("=" * 45)


def menu():
    restaurante = Restaurante("Sabor Valluno")
    cargar_datos_iniciales(restaurante)

    while True:
        print("\n--- SISTEMA DE PEDIDOS SABOR VALLUNO (VARIANTE A) ---")
        print("1. Listar menú disponible por día")
        print("2. Registrar nuevo producto o combo")
        print("3. Registrar cliente")
        print("4. Crear pedido (Local / Para Llevar / Delivery)")
        print("5. Agregar o quitar productos a un pedido")
        print("6. Ver detalle de un pedido")
        print("7. Cambiar estado de un pedido")
        print("8. Cobrar pedido (Efectivo / QR / Tarjeta)")
        print("9. Ver reporte de ventas y Top 3 productos")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                dia = input("Ingrese el día de la semana (ej. lunes, domingo): ").strip()
                disponibles = restaurante.listar_menu_disponible(dia)
                print(f"\nMenú disponible el {dia.capitalize()}:")
                for p in disponibles:
                    print(f" - {p.nombre} ({type(p).__name__}): Bs {p.calcular_precio():.2f}")

            elif opcion == "2":
                tipo = input("Tipo (1=Plato, 2=Bebida, 3=Combo): ").strip()
                nombre = input("Nombre: ").strip()
                if tipo == "1":
                    precio = float(input("Precio (Bs): "))
                    dias_txt = input("Días disponibles separados por coma (vacío = todos): ").strip()
                    dias = [d.strip() for d in dias_txt.split(",")] if dias_txt else []
                    restaurante.registrar_producto(Plato(nombre, precio, dias))
                elif tipo == "2":
                    precio = float(input("Precio por vaso (Bs): "))
                    formato = input("Formato (vaso / jarra): ").strip()
                    restaurante.registrar_producto(Bebida(nombre, precio, formato))
                elif tipo == "3":
                    print("Productos actuales:", [p.nombre for p in restaurante.menu])
                    nombres = input("Ingrese nombres de productos separados por coma (mínimo 2): ").split(",")
                    prods = [restaurante.buscar_producto(n.strip()) for n in nombres if n.strip()]
                    restaurante.registrar_producto(Combo(nombre, prods))
                print("Producto registrado correctamente.")

            elif opcion == "3":
                nombre = input("Nombre del cliente: ").strip()
                telefono = input("Teléfono (8 dígitos, inicia en 6 o 7): ").strip()
                cliente = restaurante.registrar_cliente(nombre, telefono)
                print("Cliente registrado:", cliente)

            elif opcion == "4":
                tel = input("Teléfono del cliente registrado: ").strip()
                cliente = restaurante.buscar_cliente_por_telefono(tel)
                dia = input("Día del pedido (ej. domingo): ").strip() or "domingo"
                tipo = input("Tipo de pedido (1=Local, 2=Para Llevar, 3=Delivery): ").strip()
                if tipo == "1":
                    mesa = int(input("Número de mesa (1-15): "))
                    pedido = restaurante.crear_pedido_local(cliente, mesa, dia)
                elif tipo == "2":
                    pedido = restaurante.crear_pedido_para_llevar(cliente, dia)
                elif tipo == "3":
                    zona = input("Zona (Cercado, Quillacollo, Sacaba, Vinto): ").strip()
                    pedido = restaurante.crear_pedido_delivery(cliente, zona, dia)
                else:
                    print("Tipo no válido.")
                    continue
                print(f"Pedido creado con éxito. Número de pedido: #{pedido.n_pedido}")

            elif opcion == "5":
                n_ped = int(input("Número de pedido: "))
                pedido = restaurante.buscar_pedido(n_ped)
                accion = input("¿Desea (1) Agregar o (2) Quitar producto?: ").strip()
                if accion == "1":
                    print("Menú:", [p.nombre for p in restaurante.menu])
                    prod_nombre = input("Nombre exacto del producto: ").strip()
                    cant = int(input("Cantidad (1-20): "))
                    prod = restaurante.buscar_producto(prod_nombre)
                    pedido.agregar_producto(prod, cant)
                    print("Producto agregado.")
                elif accion == "2":
                    prod_nombre = input("Nombre del producto a quitar: ").strip()
                    pedido.quitar_producto(prod_nombre)
                    print("Producto quitado.")

            elif opcion == "6":
                n_ped = int(input("Número de pedido: "))
                pedido = restaurante.buscar_pedido(n_ped)
                mostrar_detalle_pedido(pedido)

            elif opcion == "7":
                n_ped = int(input("Número de pedido: "))
                pedido = restaurante.buscar_pedido(n_ped)
                print(f"Estado actual: {pedido.estado}")
                nuevo = input("Nuevo estado (EN_PREPARACION, LISTO, ENTREGADO, CANCELADO): ").strip()
                pedido.cambiar_estado(nuevo)
                print(f"Estado actualizado a {pedido.estado}.")

            elif opcion == "8":
                n_ped = int(input("Número de pedido a cobrar: "))
                pedido = restaurante.buscar_pedido(n_ped)
                mostrar_detalle_pedido(pedido)
                metodo = input("Método de pago (1=Efectivo, 2=QR, 3=Tarjeta): ").strip()
                if metodo == "1":
                    recibido = float(input("Monto recibido en Bs: "))
                    pago_obj = Efectivo(recibido)
                elif metodo == "2":
                    cod = input("Código de transacción (10 dígitos): ").strip()
                    pago_obj = QR(cod)
                elif metodo == "3":
                    pago_obj = Tarjeta()
                else:
                    print("Método inválido.")
                    continue
                pago = pedido.registrar_pago(pago_obj)
                print("\n--- COMPROBANTE DE PAGO ---")
                print(f"Pedido #{pedido.n_pedido} | Cliente: {pedido.cliente.nombre}")
                print(f"Detalle pago: {pago_obj}")
                print(f"Total cobrado: Bs {pago.monto:.2f}")

            elif opcion == "9":
                ventas = restaurante.reporte_ventas_por_tipo()
                print("\n--- VENTAS DEL DÍA POR TIPO ---")
                for k, v in ventas.items():
                    print(f" - {k}: Bs {v:.2f}")
                print("\n--- TOP 3 PRODUCTOS MÁS VENDIDOS ---")
                for nombre, cant in restaurante.top_3_productos_mas_vendidos():
                    print(f" - {nombre}: {cant} unidades")

            elif opcion == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida.")

        except Exception as e:
            print(f"[ERROR]: {e}")


if __name__ == "__main__":
    menu()
