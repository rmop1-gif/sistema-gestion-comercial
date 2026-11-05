"""Sistema de Gestión Comercial - punto de entrada."""
import archivos
import inventario
import productos
import reportes
import ventas


def submenu(titulo, opciones):
    """opciones: lista de (texto, función)."""
    while True:
        print(f"\n--- {titulo} ---")
        for i, (texto, _) in enumerate(opciones, start=1):
            print(f"{i}. {texto}")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            return
        if op.isdigit() and 1 <= int(op) <= len(opciones):
            opciones[int(op) - 1][1]()
        else:
            print("  Opción no válida.")


def main():
    archivos.cargar_todo()
    while True:
        print("\n===== SISTEMA DE GESTIÓN COMERCIAL =====")
        print("1. Productos")
        print("2. Ventas")
        print("3. Inventario")
        print("4. Reportes")
        print("0. Salir")
        op = input("Opción: ").strip()
        if op == "1":
            submenu("PRODUCTOS", [("Registrar", productos.menu_registrar),
                                  ("Consultar", productos.menu_consultar),
                                  ("Modificar", productos.menu_modificar)])
        elif op == "2":
            ventas.menu_venta()
        elif op == "3":
            submenu("INVENTARIO", [
                ("Consultar existencias", inventario.menu_existencias),
                ("Registrar entrada", inventario.menu_entrada),
                ("Ajustar cantidad", inventario.menu_ajuste),
                ("Productos bajo stock mínimo", inventario.menu_bajo_stock),
                ("Historial de movimientos", inventario.menu_historial)])
        elif op == "4":
            reportes.menu_reportes()
        elif op == "0":
            archivos.guardar_todo()
            print("Datos guardados. ¡Hasta pronto!")
            return
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    main()
