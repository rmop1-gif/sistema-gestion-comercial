"""Módulo 1 - Gestión de productos."""
import archivos
import estructuras as est


def buscar(codigo):
    """Devuelve la fila del producto o None si no existe."""
    codigo = str(codigo).strip().upper()
    for fila in est.productos:
        if fila[est.P_COD] == codigo:
            return fila
    return None


def registrar(codigo, nombre, precio, existencia, minimo):
    """Registra un producto. Devuelve (ok, mensaje)."""
    codigo = str(codigo).strip().upper()
    nombre = str(nombre).strip()
    if not codigo or not nombre:
        return False, "El código y el nombre son obligatorios."
    if buscar(codigo):
        return False, f"El código {codigo} ya existe."
    if not isinstance(precio, (int, float)) or \
       not isinstance(existencia, int) or not isinstance(minimo, int):
        return False, "Tipo de dato incorrecto."
    if precio <= 0:
        return False, "El precio debe ser mayor que cero."
    if existencia < 0 or minimo < 0:
        return False, "Existencia y stock mínimo no pueden ser negativos."
    est.productos.append([codigo, nombre, round(float(precio), 2),
                          existencia, minimo])
    archivos.guardar_todo()
    return True, "Producto registrado correctamente."


def modificar(codigo, nombre=None, precio=None, minimo=None):
    """Modifica nombre, precio y/o stock mínimo (None = no cambiar)."""
    producto = buscar(codigo)
    if producto is None:
        return False, "El producto no existe."
    if precio is not None and precio <= 0:
        return False, "El precio debe ser mayor que cero."
    if minimo is not None and minimo < 0:
        return False, "El stock mínimo no puede ser negativo."
    if nombre:
        producto[est.P_NOM] = nombre.strip()
    if precio is not None:
        producto[est.P_PRE] = round(float(precio), 2)
    if minimo is not None:
        producto[est.P_MIN] = minimo
    archivos.guardar_todo()
    return True, "Producto modificado correctamente."


def mostrar(p):
    print(f"  {p[est.P_COD]:<8} {p[est.P_NOM]:<22} "
          f"Q{p[est.P_PRE]:>9.2f}  exist: {p[est.P_EXI]:>5}  "
          f"mín: {p[est.P_MIN]:>4}")


# ---------- Menús interactivos ----------
def menu_registrar():
    print("\n-- Registrar producto --")
    codigo = input("Código: ")
    nombre = input("Nombre: ")
    precio = est.leer_decimal("Precio: ", 0.01)
    existencia = est.leer_entero("Existencia inicial: ", 0)
    minimo = est.leer_entero("Stock mínimo: ", 0)
    ok, msg = registrar(codigo, nombre, precio, existencia, minimo)
    print(("  OK: " if ok else "  Error: ") + msg)


def menu_consultar():
    print("\n-- Consultar producto --")
    codigo = input("Código (Enter = listar todos): ").strip()
    if not codigo:
        if not est.productos:
            print("  No hay productos registrados.")
        for p in est.productos:
            mostrar(p)
        return
    p = buscar(codigo)
    if p is None:
        print("  Error: el producto no existe.")
    else:
        mostrar(p)


def menu_modificar():
    print("\n-- Modificar producto --")
    codigo = input("Código: ")
    p = buscar(codigo)
    if p is None:
        print("  Error: el producto no existe.")
        return
    mostrar(p)
    print("  (Enter = dejar igual)")
    nombre = input("Nuevo nombre: ").strip() or None
    precio = input("Nuevo precio: ").strip()
    minimo = input("Nuevo stock mínimo: ").strip()
    try:
        precio = float(precio.replace(",", ".")) if precio else None
        minimo = int(minimo) if minimo else None
    except ValueError:
        print("  Error: dato de tipo incorrecto.")
        return
    ok, msg = modificar(codigo, nombre, precio, minimo)
    print(("  OK: " if ok else "  Error: ") + msg)
