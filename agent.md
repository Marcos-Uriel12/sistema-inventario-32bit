# Documentación del Agente - Sistema de Inventario

## 1. Visión General

**Nombre:** Sistema de Gestión de Inventario con Ventas
**Tipo:** Aplicación de escritorio Python con GUI (CustomTkinter)
**Objetivo:** Gestión de inventario y ventas con persistencia en Excel

---

## 2. Arquitectura

```
main.py → GUI → inventory_manager.py → excel_manager.py → inventario.xlsx
```

### Patrón MVC
- **Model:** excel_manager.py
- **View:** GUI (CustomTkinter)
- **Controller:** inventory_manager.py, sales_manager.py

---

## 3. Estructura de Datos

### Excel (3 hojas)
| Hoja | Columnas |
|------|----------|
| inventario | codigo, producto, precio_compra, precio_venta, stock |
| ventas | fecha, codigo, producto, cantidad, precio_unitario, total |
| sin_stock | codigo, producto, fecha |

---

## 4. Archivos del Proyecto

### Principales
- `main.py` - Punto de entrada
- `inventory_manager.py` - Lógica de inventario
- `sales_manager.py` - Lógica de ventas
- `excel_manager.py` - Acceso a datos (3 hojas Excel)

### GUI
```
gui/
├── main_window.py
├── components/
│   ├── toolbar.py (botones: Agregar, Ordenar, Actualizar precios, Vender, Historial)
│   ├── search_bar.py
│   └── product_table.py
└── dialogs/
    ├── add_product_dialog.py
    ├── update_product_dialog.py
    ├── delete_product_dialog.py
    ├── update_prices_dialog.py
    ├── error_dialog.py
    ├── sales_dialog.py
    └── sales_history_dialog.py
```

---

## 5. Funcionalidades

### Inventario
- Agregar/Eliminar/Actualizar productos
- Buscar por código o nombre
- Búsqueda en vivo
- Ordenar por precio/stock
- Actualizar precios por porcentaje
- Validaciones de entrada

### Ventas
- Sistema de ventas con carrito
- Búsqueda por código o nombre
- Múltiples productos por venta
- Registro automático en Excel
- Reducción automática de stock
- Seguimiento de productos sin stock

### Sistema
- Backups automáticos (20 máximo)
- Archivado mensual de ventas (cada 1 del mes)
- Cache en memoria (carga Excel solo una vez)
- Auto-creación de Excel si no existe

---

## 6. Funciones Principales

### inventory_manager.py
```python
ver_productos() -> list
buscar_producto(codigo) -> dict
agregar_producto(codigo, producto, precio_compra, precio_venta, stock) -> (bool, str)
actualizar_producto(codigo, producto, precio_compra, precio_venta, stock) -> (bool, str)
eliminar_producto(codigo) -> (bool, str)
aumentar_precios(porcentaje) -> (bool, str)
```

### sales_manager.py
```python
registrar_venta(codigo, cantidad) -> (bool, dict)
obtener_ventas() -> list
obtener_sin_stock() -> list
buscar_productos(nombre) -> list
get_producto(codigo) -> dict
```

### excel_manager.py
```python
cargar_datos() -> DataFrame      # inventario
cargar_ventas() -> DataFrame
cargar_sin_stock() -> DataFrame
guardar_inventario(df)
guardar_ventas(df)
guardar_sin_stock(df)
```

---

## 7. Validaciones

### entrada
- Código: no vacío, no duplicado
- Producto: no vacío
- Precios: numéricos, >= 0, precio_compra <= precio_venta
- Stock: numérico, entero, >= 0

### ventas
- Stock insuficiente → ValueError

---

## 8. Tests

| Archivo | Tests |
|---------|-------|
| test_validations.py | 18 |
| test_sales.py | 9 |
| stress_test_inventory.py | 8 |
| test_gui_basic.py | 8 |

**Total: 43 tests**

---

## 9. Compilación

### Python 32-bit (3.11.9)
```bash
pyinstaller --onefile --windowed --icon=icono.ico --name sistema_inventario main.py
```

### Dependencias
```
pandas==2.0.3
numpy==1.26.4
openpyxl
customtkinter
pyinstaller
pytest
```

---

## 10. Repositorios GitHub

| Repo | URL |
|------|-----|
| inventario-python | github.com/Marcos-Uriel12/inventario-python |
| sistema-inventario-32bit | github.com/Marcos-Uriel12/sistema-inventario-32bit |

---

## 11. Notas

- El 1 de cada mes se archivan las ventas en `ventas_mensuales/mes_año.xlsx`
- Máximo 20 backups en carpeta `backup/`
- Cache en memoria mejora rendimiento
- Compatible Windows 32-bit y 64-bit
