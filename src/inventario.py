"""Módulo 3 - Control de inventarios."""
from datetime import datetime

import archivos
import estructuras as est
import productos


def registrar_movimiento(codigo, tipo, cantidad, descripcion):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    est.movimientos.append([fecha, codigo, tipo, cantidad, descripcion])


def registrar_entrada(codigo, cantidad, descripcion="Entrada de inventario"):
    p = productos.buscar(codigo)
    if p is None:
        return False, "El producto no existe."
    if not isinstance(cantidad, int) or cantidad <= 0:
        return False, "La cantidad debe ser un entero mayor que cero."
    p[est.P_EXI] += cantidad
    registrar_movimiento(p[est.P_COD], "ENTRADA", cantidad, descripcion)
    archivos.guardar_todo()
    return True, f"Entrada registrada. Nueva existencia: {p[est.P_EXI]}"


def ajustar(codigo, nueva_cantidad, descripcion="Ajuste de inventario"):
    p = productos.buscar(codigo)
    if p is None:
        return False, "El producto no existe."
    if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
        return False, "La cantidad debe ser un entero no negativo."
    diferencia = nueva_cantidad - p[est.P_EXI]
    p[est.P_EXI] = nueva_cantidad
    registrar_movimiento(p[est.P_COD], "AJUSTE", diferencia, descripcion)
    archivos.guardar_todo()
    return True, f"Existencia ajustada a {nueva_cantidad}."


def bajo_stock():
    """Productos con existencia <= stock mínimo."""
    return [p for p in est.productos if p[est.P_EXI] <= p[est.P_MIN]]


# ---------- Menús interactivos ----------
def menu_existencias():
    print("\n-- Existencias --")
    codigo = input("Código (Enter = todos): ").strip()
    if codigo:
        p = productos.buscar(codigo)
        if p is None:
            print("  Error: el producto no existe.")
        else:
            productos.mostrar(p)
    else:
        for p in est.productos:
            productos.mostrar(p)


def menu_entrada():
    print("\n-- Registrar entrada --")
    codigo = input("Código: ")
    if productos.buscar(codigo) is None:
        print("  Error: el producto no existe.")
        return
    cantidad = est.leer_entero("Cantidad que ingresa: ", 1)
    desc = input("Descripción: ").strip() or "Entrada de inventario"
    ok, msg = registrar_entrada(codigo, cantidad, desc)
    print(("  OK: " if ok else "  Error: ") + msg)


def menu_ajuste():
    print("\n-- Ajustar cantidad --")
    codigo = input("Código: ")
    if productos.buscar(codigo) is None:
        print("  Error: el producto no existe.")
        return
    nueva = est.leer_entero("Nueva cantidad disponible: ", 0)
    desc = input("Motivo: ").strip() or "Ajuste de inventario"
    ok, msg = ajustar(codigo, nueva, desc)
    print(("  OK: " if ok else "  Error: ") + msg)


def menu_bajo_stock():
    print("\n-- Productos en o bajo el stock mínimo --")
    lista = bajo_stock()
    if not lista:
        print("  Ningún producto está bajo el stock mínimo.")
    for p in lista:
        productos.mostrar(p)


def menu_historial():
    print("\n-- Historial de movimientos --")
    if not est.movimientos:
        print("  Aún no hay movimientos.")
    for m in est.movimientos:
        print(f"  {m[est.M_FECHA]}  {m[est.M_COD]:<8} {m[est.M_TIPO]:<8} "
              f"{m[est.M_CANT]:>5}  {m[est.M_DESC]}")
