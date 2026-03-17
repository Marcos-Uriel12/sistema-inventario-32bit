# Documentación del Agente - Sistema de Inventario

## 1. Visión General del Proyecto

**Nombre:** Sistema de Gestión de Inventario  
**Tipo:** Aplicación de consola en Python  
**Objetivo:** Crear un sistema de inventario básico que permita gestionar productos con operaciones CRUD, persistiendo datos en Excel.  
**Propósito educativo:** Aprender arquitectura de software y desarrollo asistido con IA.

---

## 2. Arquitectura del Proyecto

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                    (Punto de entrada)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        menu.py                               │
│              (Interfaz de usuario - CLI)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  inventory_manager.py                       │
│                   (Lógica del negocio)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     excel_manager.py                         │
│               (Capa de acceso a datos)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      inventario.xlsx                        │
│                   (Persistencia de datos)                    │
└─────────────────────────────────────────────────────────────┘
```

### Patrón de diseño: MVC simplificado

- **Model:** excel_manager.py (manejo de datos)
- **View:** menu.py (presentación en consola)
- **Controller:** inventory_manager.py (lógica de negocio)

---

## 3. Estructura de Datos

### Producto (fila en Excel)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| codigo | string | Identificador único del producto |
| producto | string | Nombre del producto |
| precio_compra | float | Costo de adquisición |
| precio_venta | float | Precio de venta al público |
| stock | int | Cantidad disponible |

---

## 4. Responsabilidades de Cada Archivo

### 4.1 main.py
- **Responsabilidad:** Punto de entrada del programa
- **Funciones:**
  - Inicializar la aplicación
  - Lanzar el menú principal
  - Manejar excepciones globales
- **No debe hacer:** Lógica de negocio ni acceso a datos

### 4.2 menu.py
- **Responsabilidad:** Interactuar con el usuario
- **Funciones:**
  - Mostrar menú principal con opciones
  - Recibir y validar input del usuario
  - Llamar a las funciones correspondientes del inventory_manager
  - Mostrar resultados de operaciones
  - **Confirmar eliminación (S/N)** antes de llamar a eliminar
- **No debe hacer:** Manipular datos directamente ni contener lógica de negocio

### 4.3 inventory_manager.py
- **Responsabilidad:** Lógica del negocio
- **Funciones:**
  - `agregar_producto(codigo, producto, precio_compra, precio_venta, stock)`
  - `eliminar_producto(codigo)`
  - `buscar_producto(codigo)` → dict o None
  - `actualizar_precio(codigo, nuevo_precio)`
  - `actualizar_stock(codigo, nueva_cantidad)`
  - `ver_productos()` → list
  - Validar datos de entrada
  - Validar reglas de negocio (ej: stock no negativo, precios positivos)
- **No debe hacer:** Lectura/escritura directa a Excel

### 4.4 excel_manager.py
- **Responsabilidad:** Acceso y persistencia de datos
- **Funciones:**
  - `cargar_datos()` → DataFrame
  - `guardar_datos(df)` → None
  - `existe_producto(codigo)` → bool
  - `leer_producto(codigo)` → dict o None
  - `escribir_producto(producto)` → None
  - `actualizar_producto(codigo, datos)` → None
  - `eliminar_producto(codigo)` → None
- **No debe hacer:** Validación de reglas de negocio

---

## 5. Flujo del Sistema

```
┌──────────────┐     ┌──────────────┐     ┌────────────────────┐     ┌───────────────┐
│   Usuario    │────▶│    menu.py   │────▶│ inventory_manager  │────▶│excel_manager  │
│  (Console)   │◀────│  (presenta)  │◀────│    (lógica)        │◀────│   (datos)     │
└──────────────┘     └──────────────┘     └────────────────────┘     └───────────────┘
                                                                    │
                                                                    ▼
                                                             ┌───────────────┐
                                                             │inventario.xlsx │
                                                             │  (archivo)     │
                                                             └───────────────┘
```

### Flujo detallado para cada operación:

**Ver productos:**
1. Usuario selecciona opción en menu.py
2. menu.py llama a `inventory_manager.ver_productos()`
3. inventory_manager llama a `excel_manager.cargar_datos()`
4. excel_manager retorna DataFrame
5. inventory_manager retorna lista de productos
6. menu.py formatea y muestra al usuario

**Agregar producto:**
1. Usuario ingresa datos en menu.py
2. menu.py valida formato básico y llama a `inventory_manager.agregar_producto()`
3. inventory_manager valida reglas de negocio
4. inventory_manager llama a `excel_manager.escribir_producto()`
5. excel_manager guarda en Excel
6. Retorna éxito/fracaso

**Eliminar producto:**
1. Usuario ingresa código en menu.py
2. menu.py verifica que existe el producto
3. **menu.py muestra confirmación "¿Está seguro de eliminar? (S/N)"**
4. Si usuario confirma con "S", menu.py llama a `inventory_manager.eliminar_producto(codigo)`
5. Retorna resultado de la operación

**Buscar/Actualizar:** Similar flujo, usando métodos específicos

---

## 6. Plan de Implementación

### Fase 1: Infraestructura base ✅

1. **Crear excel_manager.py** ✅
2. **Crear inventory_manager.py** ✅
3. **Crear menu.py** ✅
4. **Crear main.py** ✅

### Fase 2: Funcionalidades ✅

- Ver productos ✅
- Buscar producto ✅
- Agregar producto ✅
- Eliminar producto (con confirmación S/N) ✅
- Actualizar precio ✅
- Actualizar stock ✅

### Fase 3: Refinamiento

- Manejo de errores adicionales
- Mejoras de UX

---

## 7. Buenas Prácticas

### 7.1 Código limpio
- **Nombres descriptivos:** Usar nombres claros para variables y funciones
- **Funciones pequeñas:** Cada función hace una cosa
- **DRY (Don't Repeat Yourself):** No duplicar código

### 7.2 Manejo de errores
- Usar `try-except` para operaciones que pueden fallar
- Validar datos de entrada en inventory_manager (no en UI)
- Mostrar mensajes de error claros al usuario

### 7.3 Estructura
- Imports organizados al inicio del archivo
- Un archivo = una responsabilidad clara

### 7.4 Nomenclatura Python
- `snake_case` para funciones y variables
- Módulos con nombres en minúsculas

---

## 8. Confirmación de Eliminación

**Requisito implementado:** Antes de eliminar un producto, mostrar confirmación simple (S/N).

**Flujo en menu.py:**
```
1. Usuario elige opción eliminar
2. Ingresa código del producto
3. Sistema verifica que existe
4. Muestra: "¿Está seguro de eliminar? (S/N)"
5. Si ingresa "S" o "s" → procede a eliminar
6. Si ingresa "N" o "n" o cualquier otra cosa → cancela operación
```

---

## 9. Dependencias

```python
pandas>=1.5.0
openpyxl>=3.0.0
```

---

## 10. Extensiones Futuras

- Interfaz gráfica (GUI)
- Base de datos real (SQL)
- Reportes y estadísticas
- Categorías de productos
- API REST

---

## 11. GUI Architecture (CustomTkinter)

### Visión General

La GUI reemplaza la CLI como la nueva interfaz principal de usuario, manteniendo la arquitectura MVC existente:

```
main.py
↓
GUI (CustomTkinter)
↓
inventory_manager.py
↓
excel_manager.py
↓
inventario.xlsx
```

### Principios

- La GUI es solo una **capa de presentación**
- NO modifica la lógica de negocio (inventory_manager.py)
- NO accede directamente a Excel (excel_manager.py)
- El patrón MVC se mantiene sin cambios

### Estructura de Carpetas GUI

```
gui/
├── __init__.py
├── app.py                    # Punto de entrada de la GUI
├── main_window.py            # Ventana principal

components/
├── __init__.py
├── product_table.py          # Tabla de productos (TTK Treeview)
├── search_bar.py            # Barra de búsqueda en vivo
└── toolbar.py               # Barra de herramientas superior

dialogs/
├── __init__.py
├── add_product_dialog.py    # Diálogo para agregar producto
├── update_product_dialog.py # Diálogo para actualizar producto
└── delete_product_dialog.py # Diálogo para confirmar eliminación
```

### Responsabilidades de Cada Archivo GUI

#### app.py
- Inicializa CustomTkinter
- Lanza la ventana principal
- Configura el tema "dark-blue"

#### main_window.py
- Ventana principal de la aplicación
- Layout: TOP (toolbar + search) + CENTER (tabla)
- Maneja eventos de la aplicación
- Coordina comunicación entre componentes

#### components/product_table.py
- Muestra todos los productos en formato tabular
- Columnas: codigo, producto, precio_compra, precio_venta, stock
- Permite selección de filas
- Scroll vertical
- Bind para menú contextual (click derecho)

#### components/search_bar.py
- Campo de entrada para búsqueda en vivo
- Filtra productos por código o nombre
- Actualiza la tabla dinámicamente

#### components/toolbar.py
- Título de la aplicación
- Botón "Agregar producto"
- Dropdown "Ordenar" (precio venta mayor/menor, stock mayor/menor)
- Botón "Actualizar" (recargar desde Excel)

#### dialogs/add_product_dialog.py
- Modal CTkToplevel
- Campos: codigo, nombre, precio_compra, precio_venta, stock
- Botón "AGREGAR PRODUCTO"
- Llama a inventory_manager.agregar_producto()

#### dialogs/update_product_dialog.py
- Modal CTkToplevel
- Campos pre-rellenados con datos del producto seleccionado
- Botón "ACTUALIZAR PRODUCTO"
- Llama a inventory_manager.actualizar_precio() y actualizar_stock()

#### dialogs/delete_product_dialog.py
- Diálogo de confirmación
- Muestra código y nombre del producto
- Botones SI/NO
- Llama a inventory_manager.eliminar_producto()

### Funciones de inventory_manager usadas por la GUI

```python
# Leer todos los productos
inventory_manager.ver_productos() -> list[dict]

# Buscar un producto específico
inventory_manager.buscar_producto(codigo) -> dict | None

# Agregar nuevo producto
inventory_manager.agregar_producto(codigo, producto, precio_compra, precio_venta, stock) -> (bool, str)

# Actualizar precio
inventory_manager.actualizar_precio(codigo, nuevo_precio) -> (bool, str)

# Actualizar stock
inventory_manager.actualizar_stock(codigo, nueva_cantidad) -> (bool, str)

# Eliminar producto
inventory_manager.eliminar_producto(codigo) -> (bool, str)
```

### Configuración de Ventana

- Título: "Sistema de Inventario"
- Tamaño: 1200x700
- Tema: dark-blue

### Validación

Por ahora, la GUI no valida errores de entrada. Los errores son manejados por inventory_manager. La validación de diálogos se implementará en una fase posterior.

---

## 12. Validaciones de Entrada

### Propósito
Validar datos de entrada en inventory_manager.py y mostrar errores en la GUI usando popups.

### Validaciones Implementadas

#### CODIGO
- No puede estar vacío
- No puede duplicarse al agregar

#### PRODUCTO (nombre)
- No puede estar vacío

#### PRECIO_COMPRA
- Debe ser numérico
- Debe ser >= 0
- No puede ser mayor que precio_venta

#### PRECIO_VENTA
- Debe ser numérico
- Debe ser >= 0

#### STOCK
- Debe ser numérico
- Debe ser entero
- Debe ser >= 0

### Manejo de Errores
- inventory_manager lanza `ValueError("mensaje claro")`
- GUI captura excepciones y muestra popup con CTkToplevel

### Popup de Error (error_dialog.py)

```python
def show_error_popup(parent, message):
    # Título: "ERROR"
    # Mensaje: texto de validación
    # Botón: "OK"
```

---

## 13. Sistema de Backup Automático

### Descripción
Cada vez que se guarda el inventario, se crea un backup automático.

### Configuración
- **Carpeta:** `backup/`
- **Nombre:** `inventario_backup_YYYYMMDD_HHMMSS.xlsx`
- **Límite:** Máximo 20 backups (se eliminan los más antiguos)

### Implementación
- En `excel_manager.py`
- Se crea automáticamente la carpeta si no existe
- Se ejecuta antes de cada guardado

---

## 14. Optimizaciones de Rendimiento

### Cache en Memoria
- El Excel se carga solo una vez al iniciar la aplicación
- Los datos se almacenan en un DataFrame global en memoria
- Solo se escribe en Excel cuando hay modificaciones
- Detecta cambios externos y recarga automáticamente

### Búsqueda con DataFrame Index
- El código del producto se usa como índice del DataFrame
- Búsquedas más rápidas con `df.loc[codigo]`

### Operaciones Vectorizadas
- Actualización masiva de precios usa pandas:
```python
df["precio_venta"] = df["precio_venta"] * (1 + porcentaje / 100)
```

---

## 15. Excel con Múltiples Hojas

### Estructura del Archivo Excel

| Hoja | Columnas |
|------|----------|
| inventario | codigo, producto, precio_compra, precio_venta, stock |
| ventas | fecha, codigo, producto, cantidad, precio_unitario, total |
| sin_stock | codigo, producto, fecha |

### Funciones en excel_manager.py

```python
# Cargar datos
cargar_datos()           # Hoja inventario
cargar_ventas()          # Hoja ventas
cargar_sin_stock()       # Hoja sin_stock

# Guardar datos
guardar_inventario(df)   # Guarda inventario
guardar_ventas(df)      # Guarda ventas
guardar_sin_stock(df)    # Guarda sin_stock
```

---

## 16. Sistema de Ventas (Sales)

### Propósito
Permitir vender productos con carrito de compras y registrar ventas.

### Módulo: sales_manager.py

```python
# Registrar una venta
registrar_venta(codigo, cantidad) -> (bool, dict)

# Obtener todas las ventas
obtener_ventas() -> list[dict]

# Obtener productos sin stock
obtener_sin_stock() -> list[dict]

# Buscar productos por nombre
buscar_productos(nombre) -> list[dict]

# Obtener un producto
get_producto(codigo) -> dict | None
```

### Comportamiento de registrar_venta()
1. Valida que el producto existe
2. Valida que hay stock suficiente
3. Reduce el stock
4. Calcula: total = precio_venta * cantidad
5. Registra la venta en hoja "ventas"
6. Si stock = 0, agrega a "sin_stock"

### Validaciones
- Stock insuficiente → `ValueError("Stock insuficiente. Stock actual: X")`

---

## 17. GUI de Ventas

### Diálogo: sales_dialog.py

**Botón en toolbar:** "Vender" (color morado #9b59b6)

**Diseño:**
```
+------------------------------------------+
|           NUEVA VENTA                   |
+------------------------------------------+
| IZQUIERDA           | DERECHA           |
| [Buscar: ________]   | CARRITO           |
|                     | --------------------|
| Producto: ...       | Producto | cant    |
| Precio: ...         | Producto | cant    |
| Stock: ...         | Producto | cant    |
|                     |                    |
| Cantidad: [___]     +--------------------+
|                     | TOTAL: $XXX.XX    |
| [Agregar]           |                    |
|                     | [VENDER] [CANCELAR]|
+---------------------+--------------------+
```

### Funcionalidades
- **Búsqueda:** Por código o nombre de producto
- **Carrito:** Permite agregar múltiples productos
- **Total:** Se calcula automáticamente
- **Vender:** Procesa todas las ventas del carrito
- **Cancelar:** Cierra sin guardar

---

## 18. Historial de Ventas

### Diálogo: sales_history_dialog.py

**Botón en toolbar:** "Historial" (color azul #3498db)

**Muestra:**
- Fecha de cada venta
- Código del producto
- Nombre del producto
- Cantidad
- Precio unitario
- Total
- **Total general de todas las ventas**

---

## 19. Archivado Mensual de Ventas

### Descripción
El 1 de cada mes, las ventas del mes anterior se archivan en un archivo separado.

### Ubicación
- **Carpeta:** `ventas_mensuales/`
- **Nombre:** `mes_año.xlsx` (ej: `marzo_2026.xlsx`)

### Meses en español
```python
MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}
```

### Funcionamiento
1. Al iniciar el programa, verifica si es día 1
2. Si hay ventas del mes anterior, las guarda en archivo mensual
3. Limpia la hoja "ventas" del Excel principal

---

## 20. Compilación a Executable

### Python 32-bit
- Versión de Python: 3.11.9 (32-bit)
- Ubicación: `C:\Python311_32`

### Dependencias安装
```bash
pip install pandas==2.0.3 numpy==1.26.4 openpyxl customtkinter pyinstaller pytest
```

### Comando de compilación
```bash
pyinstaller --onefile --windowed --icon=icono.ico --name sistema_inventario main.py
```

### Repositorios GitHub

| Repositorio | Descripción |
|--------------|-------------|
| inventario-python | Versión 64-bit |
| sistema-inventario-32bit | Versión 32-bit |

---

## 21. Tests

### Suites de Tests

| Archivo | Descripción |
|---------|-------------|
| tests/test_validations.py | Tests de validaciones de entrada |
| tests/test_sales.py | Tests del sistema de ventas |
| tests/stress_test_inventory.py | Tests de estrés (100 y 500 productos) |
| tests_gui/test_gui_basic.py | Tests de importación de GUI |

### Ejecución de Tests
```bash
pytest tests/ tests_gui/ -v
```

---

## 22. Estructura Final del Proyecto

```
Inventario_app/
├── main.py                      # Punto de entrada
├── inventory_manager.py          # Lógica de negocio
├── excel_manager.py              # Acceso a datos (3 hojas Excel)
├── sales_manager.py              # Sistema de ventas
├── requirements.txt              # Dependencias
├── icono.ico                     # Icono de la aplicación
├── .gitignore                    # Archivos ignorados por Git
├── agent.md                      # Documentación del agente
├── README.md                     # README del proyecto
│
├── gui/                         # Interfaz gráfica
│   ├── __init__.py
│   ├── app.py
│   ├── main_window.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── product_table.py
│   │   ├── search_bar.py
│   │   └── toolbar.py
│   │
│   └── dialogs/
│       ├── __init__.py
│       ├── add_product_dialog.py
│       ├── update_product_dialog.py
│       ├── delete_product_dialog.py
│       ├── update_prices_dialog.py
│       ├── error_dialog.py
│       ├── sales_dialog.py
│       └── sales_history_dialog.py
│
├── tests/                       # Tests unitarios
│   ├── test_validations.py
│   ├── test_sales.py
│   ├── stress_test_inventory.py
│   └── test_demo_30_productos.py
│
├── tests_gui/                  # Tests de GUI
│   └── test_gui_basic.py
│
├── backup/                     # Backups automáticos
│   └── inventario_backup_*.xlsx
│
├── ventas_mensuales/           # Ventas archivadas por mes
│   └── mes_año.xlsx
│
└── inventario.xlsx             # Archivo principal de datos
```

---

## 23. Funcionalidades Completas

### Inventario
- ✅ Agregar producto
- ✅ Eliminar producto
- ✅ Actualizar producto
- ✅ Buscar producto
- ✅ Ver todos los productos
- ✅ Ordenar por precio/stock
- ✅ Búsqueda en vivo

### Precios
- ✅ Actualizar precios por porcentaje
- ✅ Validaciones de precios

### Ventas
- ✅ Sistema de ventas con carrito
- ✅ Búsqueda por código o nombre
- ✅ Registro de ventas en Excel
- ✅ Reducción automática de stock
- ✅ Seguimiento de productos sin stock
- ✅ Historial de ventas

### Respaldo
- ✅ Backups automáticos (20 máximo)
- ✅ Archivado mensual de ventas

### Sistema
- ✅ Validaciones de entrada
- ✅ Popup de errores
- ✅ Cache en memoria
- ✅ Auto-creación de Excel
- ✅ Compatible 32-bit y 64-bit
