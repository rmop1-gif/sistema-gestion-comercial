"""Módulo 2 - Registro de ventas."""
from datetime import datetime

import archivos
import estructuras as est
import inventario
import productos


def siguiente_numero():
    if not est.ventas:
        return 1
    return max(v[est.V_NUM] for v in est.ventas) + 1


def registrar_venta(items):
    """items: lista de (codigo, cantidad). Devuelve (ok, mensaje, resumen)."""
    if not items:
        return False, "La venta no tiene productos.", None

    pedidos = {}  # codigo -> cantidad acumulada (valida stock antes de vender)
    for codigo, cantidad in items:
        p = productos.buscar(codigo)
        if p is None:
            return False, f"El producto {codigo} no existe.", None
        if not isinstance(cantidad, int) or cantidad <= 0:
            return False, "La cantidad debe ser un entero mayor que cero.", None
        acumulado = pedidos.get(p[est.P_COD], 0) + cantidad
        if acumulado > p[est.P_EXI]:
            return (False, f"Existencias insuficientes de {p[est.P_NOM]} "
                    f"(disponibles: {p[est.P_EXI]}).", None)
        pedidos[p[est.P_COD]] = acumulado

    numero = siguiente_numero()
    lineas = []
    for codigo, cantidad in pedidos.items():
        p = productos.buscar(codigo)
        lineas.append([numero, codigo, cantidad, p[est.P_PRE],
                       round(p[est.P_PRE] * cantidad, 2)])

    subtotal = round(sum(l[est.D_SUB] for l in lineas), 2)
    iva = round(subtotal * est.IVA, 2)
    total = round(subtotal + iva, 2)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for l in lineas:  # actualizar existencias
        p = productos.buscar(l[est.D_COD])
        p[est.P_EXI] -= l[est.D_CANT]
        inventario.registrar_movimiento(
            l[est.D_COD], "SALIDA", l[est.D_CANT], f"Venta #{numero}")

    est.ventas.append([numero, fecha, subtotal, iva, total])
    est.detalle.extend(lineas)
    archivos.guardar_todo()
    resumen = {"numero": numero, "fecha": fecha, "lineas": lineas,
               "subtotal": subtotal, "iva": iva, "total": total}
    return True, "Venta registrada correctamente.", resumen


def imprimir_factura(r):
    print(f"\n===== VENTA No. {r['numero']} - {r['fecha']} =====")
    for l in r["lineas"]:
        p = productos.buscar(l[est.D_COD])
        print(f"  {p[est.P_NOM]:<22} {l[est.D_CANT]:>4} x "
              f"{l[est.D_PRE]:>8.2f} = {l[est.D_SUB]:>9.2f}")
    print(f"  Subtotal: {r['subtotal']:>10.2f}")
    print(f"  IVA 12%:  {r['iva']:>10.2f}")
    print(f"  TOTAL:    {r['total']:>10.2f}")


def menu_venta():
    print("\n-- Nueva venta (código vacío para terminar) --")
    items = []
    while True:
        codigo = input("Código del producto: ").strip()
        if not codigo:
            break
        p = productos.buscar(codigo)
        if p is None:
            print("  Error: el producto no existe.")
            continue
        print(f"  {p[est.P_NOM]} - Q{p[est.P_PRE]:.2f} "
              f"(disponibles: {p[est.P_EXI]})")
        cantidad = est.leer_entero("Cantidad: ", 1)
        ya = sum(c for cod, c in items if cod.upper() == p[est.P_COD])
        if ya + cantidad > p[est.P_EXI]:
            print("  Error: no hay existencias suficientes.")
            continue
        items.append((p[est.P_COD], cantidad))
    ok, msg, resumen = registrar_venta(items)
    if ok:
        imprimir_factura(resumen)
    else:
        print("  Error: " + msg)
