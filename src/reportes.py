"""Módulo 4 - Reportes y estadísticas (todo calculado desde los datos)."""
import estructuras as est
import inventario
import productos


def total_ingresos():
    return round(sum(v[est.V_TOT] for v in est.ventas), 2)


def producto_mas_vendido():
    """Devuelve (codigo, nombre, unidades) o None si no hay ventas."""
    unidades = {}
    for d in est.detalle:
        unidades[d[est.D_COD]] = unidades.get(d[est.D_COD], 0) + d[est.D_CANT]
    if not unidades:
        return None
    codigo = max(unidades, key=unidades.get)
    p = productos.buscar(codigo)
    return codigo, (p[est.P_NOM] if p else "(eliminado)"), unidades[codigo]


def valor_inventario():
    return round(sum(p[est.P_PRE] * p[est.P_EXI] for p in est.productos), 2)


def promedio_ventas_por_periodo():
    """Promedio de ventas por día. Devuelve (promedio, dias) o (0, 0)."""
    por_dia = {}
    for v in est.ventas:
        dia = v[est.V_FECHA][:10]
        por_dia[dia] = por_dia.get(dia, 0) + v[est.V_TOT]
    if not por_dia:
        return 0.0, 0
    return round(sum(por_dia.values()) / len(por_dia), 2), len(por_dia)


def menu_reportes():
    while True:
        print("\n--- REPORTES ---")
        print("1. Listado general de productos")
        print("2. Productos en/bajo stock mínimo")
        print("3. Historial de ventas")
        print("4. Total de ingresos por ventas")
        print("5. Producto más vendido")
        print("6. Valor total del inventario")
        print("7. Promedio de ventas por período (día)")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            if not est.productos:
                print("  No hay productos.")
            for p in est.productos:
                productos.mostrar(p)
        elif op == "2":
            lista = inventario.bajo_stock()
            if not lista:
                print("  Ningún producto está bajo el mínimo.")
            for p in lista:
                productos.mostrar(p)
        elif op == "3":
            if not est.ventas:
                print("  Aún no hay ventas.")
            for v in est.ventas:
                print(f"  No. {v[est.V_NUM]:<4} {v[est.V_FECHA]}  "
                      f"sub {v[est.V_SUB]:>9.2f}  IVA {v[est.V_IVA]:>8.2f}  "
                      f"total {v[est.V_TOT]:>9.2f}")
        elif op == "4":
            print(f"  Total de ingresos: Q{total_ingresos():.2f}")
        elif op == "5":
            r = producto_mas_vendido()
            print("  Aún no hay ventas." if r is None else
                  f"  {r[1]} ({r[0]}) con {r[2]} unidades vendidas.")
        elif op == "6":
            print(f"  Valor del inventario: Q{valor_inventario():.2f}")
        elif op == "7":
            prom, dias = promedio_ventas_por_periodo()
            print("  Aún no hay ventas." if dias == 0 else
                  f"  Promedio por día: Q{prom:.2f} ({dias} día(s) con ventas)")
        elif op == "0":
            return
        else:
            print("  Opción no válida.")
