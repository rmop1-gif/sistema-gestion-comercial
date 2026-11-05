"""Lectura y escritura de archivos CSV (carpeta data/ del repositorio)."""
import csv
import os

import estructuras as est

CARPETA = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))

# clave: (archivo, encabezado, tipos de cada columna, matriz)
ARCHIVOS = {
    "productos": ("productos.csv",
                  ["codigo", "nombre", "precio", "existencia", "stock_minimo"],
                  (str, str, float, int, int), est.productos),
    "ventas": ("ventas.csv",
               ["numero", "fecha", "subtotal", "iva", "total"],
               (int, str, float, float, float), est.ventas),
    "detalle": ("detalle_ventas.csv",
                ["numero", "codigo", "cantidad", "precio", "subtotal"],
                (int, str, int, float, float), est.detalle),
    "movimientos": ("movimientos.csv",
                    ["fecha", "codigo", "tipo", "cantidad", "descripcion"],
                    (str, str, str, int, str), est.movimientos),
}


def guardar(clave):
    nombre, encabezado, _, matriz = ARCHIVOS[clave]
    os.makedirs(CARPETA, exist_ok=True)
    with open(os.path.join(CARPETA, nombre), "w", newline="",
              encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(encabezado)
        escritor.writerows(matriz)


def cargar(clave):
    """Carga un CSV en su matriz. Omite líneas dañadas. Devuelve filas leídas."""
    nombre, _, tipos, matriz = ARCHIVOS[clave]
    del matriz[:]
    ruta = os.path.join(CARPETA, nombre)
    if not os.path.exists(ruta):
        return 0
    try:
        with open(ruta, newline="", encoding="utf-8") as f:
            lector = csv.reader(f)
            next(lector, None)  # encabezado
            for n, fila in enumerate(lector, start=2):
                if not fila:
                    continue
                try:
                    if len(fila) != len(tipos):
                        raise ValueError
                    matriz.append([t(v) for t, v in zip(tipos, fila)])
                except ValueError:
                    print(f"  Aviso: línea {n} de {nombre} inválida; se omitió.")
    except OSError as error:
        print(f"  Error al leer {nombre}: {error}")
    return len(matriz)


def guardar_todo():
    for clave in ARCHIVOS:
        guardar(clave)


def cargar_todo():
    for clave in ARCHIVOS:
        cargar(clave)
