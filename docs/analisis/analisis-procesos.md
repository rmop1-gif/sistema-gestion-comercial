# Análisis de procesos - Sistema de Gestión Comercial

Este documento describe los procesos funcionales principales del sistema.
Los diagramas de flujo están en la carpeta `docs/diagramas/`.

Datos generales:
- IVA aplicado en las ventas: 12 %.
- Los datos se guardan en archivos CSV dentro de `data/`.
- En memoria se manejan matrices (listas de listas) definidas en `src/estructuras.py`.

---

## 1. Registro de productos

- **Módulo:** Productos (`src/productos.py`)
- **Objetivo:** Agregar un producto nuevo al catálogo con sus datos básicos.
- **Descripción del funcionamiento:** El usuario ingresa los datos del producto. El sistema valida cada dato, agrega una fila a la matriz de productos y guarda el archivo `productos.csv`.
- **Datos de entrada:** código, nombre, precio, existencia inicial y stock mínimo.
- **Procesamiento realizado:** se convierte el código a mayúsculas y se quitan espacios; se verifica que no exista; se agrega la fila `[código, nombre, precio, existencia, stock mínimo]`; se guarda en CSV.
- **Datos de salida:** mensaje "Producto registrado correctamente" o el mensaje de error correspondiente.
- **Reglas de negocio:**
  - El código es único.
  - El código y el nombre son obligatorios.
  - El precio debe ser mayor que cero.
  - La existencia y el stock mínimo no pueden ser negativos.
- **Validaciones y posibles errores:**
  - Datos numéricos con tipo incorrecto: se vuelve a pedir el dato.
  - Código o nombre vacío: "El código y el nombre son obligatorios."
  - Código duplicado: "El código ya existe."
  - Precio menor o igual a cero, o cantidades negativas: se rechaza el registro.
- **Diagrama:** `docs/diagramas/01_registro_productos.png`

---

## 2. Consulta y modificación de productos

- **Módulo:** Productos (`src/productos.py`)
- **Objetivo:** Ver la información de los productos y corregir su nombre, precio o stock mínimo.
- **Descripción del funcionamiento:** En la consulta, el usuario ingresa un código y se muestra el producto; si deja el código vacío, se listan todos. En la modificación, se muestran los datos actuales y el usuario escribe solo los que desea cambiar (Enter deja el valor igual).
- **Datos de entrada:** código del producto y, para modificar, nuevo nombre, nuevo precio y nuevo stock mínimo.
- **Procesamiento realizado:** búsqueda del código en la matriz; validación de los nuevos datos; actualización de la fila; guardado en CSV.
- **Datos de salida:** datos del producto, listado completo, o mensaje de confirmación o error.
- **Reglas de negocio:**
  - La existencia no se modifica aquí; se cambia desde Inventario.
  - El precio nuevo debe ser mayor que cero.
  - El stock mínimo nuevo no puede ser negativo.
- **Validaciones y posibles errores:**
  - Consultar o modificar un producto inexistente: "El producto no existe."
  - Datos de tipo incorrecto al modificar: se cancela el cambio.
  - Precio o mínimo fuera de rango: se rechaza la modificación.
- **Diagrama:** `docs/diagramas/02_consulta_modificacion_productos.png`

---

## 3. Registro de ventas

- **Módulo:** Ventas (`src/ventas.py`)
- **Objetivo:** Registrar una venta con uno o varios productos, calcular los montos y actualizar el inventario.
- **Descripción del funcionamiento:** El usuario agrega productos y cantidades en un ciclo hasta dejar el código vacío. Luego el sistema genera el número de venta, calcula subtotal, IVA y total, descuenta las existencias, registra los movimientos y guarda todo en archivos.
- **Datos de entrada:** código y cantidad de cada producto vendido.
- **Procesamiento realizado:**
  - Subtotal = suma de precio × cantidad de cada línea.
  - IVA = subtotal × 12 %.
  - Total = subtotal + IVA.
  - Número de venta = último número + 1 (o 1 si es la primera).
  - Existencia = existencia − cantidad vendida.
  - Se registra un movimiento de tipo SALIDA por cada producto.
- **Datos de salida:** factura en pantalla, y registros en `ventas.csv`, `detalle_ventas.csv`, `movimientos.csv` y `productos.csv`.
- **Reglas de negocio:**
  - No se puede vender más de lo que hay en existencia.
  - Si un producto se agrega varias veces, las cantidades se acumulan para validar el stock.
  - Una venta debe tener al menos un producto.
- **Validaciones y posibles errores:**
  - Producto inexistente: "El producto no existe."
  - Cantidad no entera o menor que 1: se vuelve a pedir.
  - Existencias insuficientes: se rechaza la línea y no se descuenta nada.
  - Venta sin productos: "La venta no tiene productos."
- **Diagrama:** `docs/diagramas/03_registro_ventas.png`

---

## 4. Actualización de inventario

- **Módulo:** Inventario (`src/inventario.py`)
- **Objetivo:** Mantener las existencias al día mediante entradas y ajustes, con historial de cada movimiento.
- **Descripción del funcionamiento:** El usuario elige un producto y una operación. En una entrada se suma la cantidad que ingresa; en un ajuste se indica la nueva cantidad disponible. Se registra el movimiento, se guardan los archivos y se avisa si el producto quedó en o bajo el stock mínimo.
- **Datos de entrada:** código del producto, tipo de operación y cantidad.
- **Procesamiento realizado:** entrada: existencia = existencia + cantidad; ajuste: diferencia = nueva − existencia y existencia = nueva; registro del movimiento con fecha, código, tipo, cantidad y descripción.
- **Datos de salida:** existencia actualizada, movimiento en `movimientos.csv` y alerta de stock mínimo.
- **Reglas de negocio:**
  - Una entrada debe ser un entero mayor que cero.
  - Un ajuste debe ser un entero mayor o igual a cero.
  - Un producto está en alerta si su existencia es menor o igual a su stock mínimo.
  - Cada movimiento guarda como mínimo fecha, código, tipo, cantidad y descripción.
- **Validaciones y posibles errores:**
  - Producto inexistente: "El producto no existe."
  - Cantidad inválida, negativa o de tipo incorrecto: se vuelve a pedir.
- **Diagrama:** `docs/diagramas/04_actualizacion_inventario.png`

---

## 5. Lectura de archivos

- **Módulo:** Archivos (`src/archivos.py`)
- **Objetivo:** Cargar en memoria los datos guardados al iniciar el programa.
- **Descripción del funcionamiento:** Para cada archivo (productos, ventas, detalle y movimientos) se vacía la matriz, se abre el CSV, se omite el encabezado y se lee línea por línea, convirtiendo cada valor a su tipo.
- **Datos de entrada:** archivos CSV de la carpeta `data/`.
- **Procesamiento realizado:** conversión de texto a número entero, decimal o texto según la columna; agregado de cada fila válida a su matriz.
- **Datos de salida:** matrices cargadas en memoria y cantidad de filas leídas.
- **Reglas de negocio:**
  - Si un archivo no existe, la matriz inicia vacía (primer uso del sistema).
  - La ruta de `data/` es relativa al repositorio, no a una computadora específica.
- **Validaciones y posibles errores:**
  - Archivo inexistente: no es error, se inicia sin datos.
  - Línea vacía: se ignora.
  - Línea con columnas faltantes o datos que no se pueden convertir: se muestra un aviso y se omite.
  - Error del sistema al abrir el archivo: se muestra el mensaje y se continúa.
- **Diagrama:** `docs/diagramas/05_lectura_archivos.png`

---

## 6. Generación de reportes

- **Módulo:** Reportes (`src/reportes.py`)
- **Objetivo:** Mostrar información resumida y estadísticas a partir de los datos almacenados.
- **Descripción del funcionamiento:** El usuario elige uno de los 7 reportes en un menú que se repite hasta que escribe 0. El sistema calcula el resultado recorriendo las matrices y lo muestra.
- **Datos de entrada:** opción del menú (1 a 7).
- **Procesamiento realizado:**
  1. Listado general de productos.
  2. Productos con existencia menor o igual al stock mínimo.
  3. Historial de ventas.
  4. Total de ingresos: suma de los totales de todas las ventas.
  5. Producto más vendido: se acumulan unidades por código y se toma el mayor.
  6. Valor del inventario: suma de precio × existencia.
  7. Promedio de ventas por período: ventas agrupadas por día; promedio = suma de los totales / número de días con ventas.
- **Datos de salida:** reporte en pantalla.
- **Reglas de negocio:**
  - Todos los resultados se calculan de la información almacenada, no de valores escritos en el código.
  - El período usado para el promedio es el día.
- **Validaciones y posibles errores:**
  - Opción no válida: "Opción no válida."
  - Sin datos registrados: se muestra "Aún no hay ventas" o "No hay productos".
- **Diagrama:** `docs/diagramas/06_generacion_reportes.png`
