import pandas as pd
from pathlib import Path
from datetime import datetime
import os
import sys

def _get_base_dir():
    if getattr(sys, 'frozen', False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).resolve().parent
    return base

BASE_DIR = _get_base_dir()
INVENTORY_FILE = BASE_DIR / "inventario.xlsx"
BACKUP_DIR = BASE_DIR / "backup"

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

ARCHIVOS_VENTAS_DIR = BASE_DIR / "ventas_mensuales"

COLUMNAS_INVENTARIO = ["codigo", "producto", "precio_compra", "precio_venta", "stock"]
COLUMNAS_VENTAS = ["fecha", "codigo", "producto", "cantidad", "precio_unitario", "total"]
COLUMNAS_SIN_STOCK = ["codigo", "producto", "fecha"]


def _verificar_nuevo_mes():
    """Verifica si es el primer día del mes y archiva las ventas del mes anterior"""
    global _df_ventas, _df_inventario, _df_sin_stock, _cache_mtime
    
    today = datetime.now()
    
    if today.day != 1:
        return
    
    if _df_ventas is None or _df_ventas.empty:
        return
    
    ARCHIVOS_VENTAS_DIR.mkdir(parents=True, exist_ok=True)
    
    mes_anterior = today.month - 1
    anio_anterior = today.year
    if mes_anterior == 0:
        mes_anterior = 12
        anio_anterior -= 1
    
    nombre_mes = MESES.get(mes_anterior, "desconocido")
    nombre_archivo = f"{nombre_mes}_{anio_anterior}.xlsx"
    archivo_ventas = ARCHIVOS_VENTAS_DIR / nombre_archivo
    
    try:
        with pd.ExcelWriter(archivo_ventas, engine='openpyxl') as writer:
            _df_ventas.to_excel(writer, sheet_name='ventas', index=False)
        
        _df_ventas = pd.DataFrame(columns=COLUMNAS_VENTAS)
        
        with pd.ExcelWriter(INVENTORY_FILE, engine='openpyxl', mode='w') as writer:
            _df_inventario.to_excel(writer, sheet_name='inventario', index=True)
            _df_ventas.to_excel(writer, sheet_name='ventas', index=False)
            _df_sin_stock.to_excel(writer, sheet_name='sin_stock', index=False)
        
        _cache_mtime = INVENTORY_FILE.stat().st_mtime
    except Exception:
        pass

_df_inventario = None
_df_ventas = None
_df_sin_stock = None
_cache_mtime = None


def _init_excel_multisheet():
    global _df_inventario, _df_ventas, _df_sin_stock, _cache_mtime
    
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    if not INVENTORY_FILE.exists():
        _df_inventario = pd.DataFrame(columns=COLUMNAS_INVENTARIO)
        _df_inventario.set_index("codigo", inplace=True)
        
        _df_ventas = pd.DataFrame(columns=COLUMNAS_VENTAS)
        
        _df_sin_stock = pd.DataFrame(columns=COLUMNAS_SIN_STOCK)
        
        with pd.ExcelWriter(INVENTORY_FILE, engine='openpyxl') as writer:
            _df_inventario.to_excel(writer, sheet_name='inventario', index=True)
            _df_ventas.to_excel(writer, sheet_name='ventas', index=False)
            _df_sin_stock.to_excel(writer, sheet_name='sin_stock', index=False)
        
        _cache_mtime = INVENTORY_FILE.stat().st_mtime
        return
    
    try:
        _df_inventario = pd.read_excel(INVENTORY_FILE, sheet_name='inventario', index_col=0)
        if _df_inventario.empty:
            _df_inventario = pd.DataFrame(columns=COLUMNAS_INVENTARIO)
            _df_inventario.set_index("codigo", inplace=True)
        else:
            _df_inventario.index = _df_inventario.index.astype(str)
    except Exception:
        _df_inventario = pd.DataFrame(columns=COLUMNAS_INVENTARIO)
        _df_inventario.set_index("codigo", inplace=True)
    
    try:
        _df_ventas = pd.read_excel(INVENTORY_FILE, sheet_name='ventas')
        if _df_ventas.empty:
            _df_ventas = pd.DataFrame(columns=COLUMNAS_VENTAS)
    except Exception:
        _df_ventas = pd.DataFrame(columns=COLUMNAS_VENTAS)
    
    try:
        _df_sin_stock = pd.read_excel(INVENTORY_FILE, sheet_name='sin_stock')
        if _df_sin_stock.empty:
            _df_sin_stock = pd.DataFrame(columns=COLUMNAS_SIN_STOCK)
    except Exception:
        _df_sin_stock = pd.DataFrame(columns=COLUMNAS_SIN_STOCK)
    
    _cache_mtime = INVENTORY_FILE.stat().st_mtime
    
    _verificar_nuevo_mes()


def _verificar_cache():
    global _df_inventario, _df_ventas, _df_sin_stock, _cache_mtime
    
    if _df_inventario is None:
        _init_excel_multisheet()
        return
    
    if not INVENTORY_FILE.exists():
        _init_excel_multisheet()
        return
    
    try:
        current_mtime = INVENTORY_FILE.stat().st_mtime
        if current_mtime != _cache_mtime:
            _init_excel_multisheet()
    except Exception:
        _init_excel_multisheet()


def cargar_datos():
    _verificar_cache()
    return _df_inventario.copy()


def cargar_ventas():
    _verificar_cache()
    return _df_ventas.copy()


def cargar_sin_stock():
    _verificar_cache()
    return _df_sin_stock.copy()


def guardar_inventario(df, crear_backup=True):
    global _df_inventario, _cache_mtime
    
    if crear_backup:
        _crear_backup()
    
    try:
        df_to_save = df.copy()
        with pd.ExcelWriter(INVENTORY_FILE, engine='openpyxl', mode='w') as writer:
            df_to_save.to_excel(writer, sheet_name='inventario', index=True)
            _df_ventas.to_excel(writer, sheet_name='ventas', index=False)
            _df_sin_stock.to_excel(writer, sheet_name='sin_stock', index=False)
        _df_inventario = df.copy()
        _cache_mtime = INVENTORY_FILE.stat().st_mtime
    except PermissionError:
        raise Exception("El archivo está abierto en Excel. Ciérrelo e intente de nuevo.")
    except FileNotFoundError:
        raise Exception("No se encontró el archivo de inventario.")
    except Exception as e:
        raise Exception(f"Error al guardar: {e}")


def guardar_ventas(df):
    global _df_ventas, _cache_mtime
    
    try:
        df_to_save = df.copy()
        with pd.ExcelWriter(INVENTORY_FILE, engine='openpyxl', mode='w') as writer:
            _df_inventario.to_excel(writer, sheet_name='inventario', index=True)
            df_to_save.to_excel(writer, sheet_name='ventas', index=False)
            _df_sin_stock.to_excel(writer, sheet_name='sin_stock', index=False)
        _df_ventas = df.copy()
        _cache_mtime = INVENTORY_FILE.stat().st_mtime
    except Exception as e:
        raise Exception(f"Error al guardar ventas: {e}")


def guardar_sin_stock(df):
    global _df_sin_stock, _cache_mtime
    
    try:
        df_to_save = df.copy()
        with pd.ExcelWriter(INVENTORY_FILE, engine='openpyxl', mode='w') as writer:
            _df_inventario.to_excel(writer, sheet_name='inventario', index=True)
            _df_ventas.to_excel(writer, sheet_name='ventas', index=False)
            df_to_save.to_excel(writer, sheet_name='sin_stock', index=False)
        _df_sin_stock = df.copy()
        _cache_mtime = INVENTORY_FILE.stat().st_mtime
    except Exception as e:
        raise Exception(f"Error al guardar sin_stock: {e}")


def _crear_backup():
    if not INVENTORY_FILE.exists():
        return
    
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"inventario_backup_{timestamp}.xlsx"
    
    try:
        with pd.ExcelWriter(backup_file, engine='openpyxl') as writer:
            df_inv = pd.read_excel(INVENTORY_FILE, sheet_name='inventario', index_col=0)
            df_ven = pd.read_excel(INVENTORY_FILE, sheet_name='ventas')
            df_sin = pd.read_excel(INVENTORY_FILE, sheet_name='sin_stock')
            df_inv.to_excel(writer, sheet_name='inventario', index=True)
            df_ven.to_excel(writer, sheet_name='ventas', index=False)
            df_sin.to_excel(writer, sheet_name='sin_stock', index=False)
    except Exception:
        pass
    
    _limpiar_backups()


def _limpiar_backups():
    try:
        backups = sorted(BACKUP_DIR.glob("inventario_backup_*.xlsx"))
        if len(backups) > 20:
            for old_backup in backups[:-20]:
                try:
                    old_backup.unlink()
                except Exception:
                    pass
    except Exception:
        pass


def existe_producto(codigo):
    _verificar_cache()
    codigo = str(codigo).strip()
    return codigo in _df_inventario.index


def leer_producto(codigo):
    _verificar_cache()
    codigo = str(codigo).strip()
    
    if codigo not in _df_inventario.index:
        return None
    
    producto = _df_inventario.loc[codigo]
    data = producto.to_dict()
    data["codigo"] = codigo
    return data


def buscar_producto_por_nombre(nombre):
    _verificar_cache()
    nombre = str(nombre).strip().lower()
    
    if nombre == "":
        return []
    
    resultados = _df_inventario[_df_inventario['producto'].str.lower().str.contains(nombre, na=False)]
    
    lista = []
    for idx, row in resultados.iterrows():
        data = row.to_dict()
        data["codigo"] = str(idx)
        lista.append(data)
    
    return lista


def escribir_producto(codigo, producto, precio_compra, precio_venta, stock):
    _verificar_cache()
    
    codigo = str(codigo).strip()
    
    nuevo = pd.DataFrame([{
        "codigo": codigo,
        "producto": str(producto),
        "precio_compra": precio_compra,
        "precio_venta": precio_venta,
        "stock": stock
    }])
    nuevo.set_index("codigo", inplace=True)
    
    df = _df_inventario.copy()
    df = pd.concat([df, nuevo])
    
    guardar_inventario(df)


def actualizar_producto(codigo, datos):
    _verificar_cache()
    
    codigo = str(codigo).strip()
    
    if codigo not in _df_inventario.index:
        raise Exception("El producto no existe")
    
    df = _df_inventario.copy()
    for clave, valor in datos.items():
        df.at[codigo, clave] = valor
    
    guardar_inventario(df)


def actualizar_stock(codigo, nuevo_stock):
    _verificar_cache()
    
    codigo = str(codigo).strip()
    
    if codigo not in _df_inventario.index:
        raise Exception("El producto no existe")
    
    df = _df_inventario.copy()
    df.at[codigo, "stock"] = nuevo_stock
    
    guardar_inventario(df)


def eliminar_producto(codigo):
    _verificar_cache()
    
    codigo = str(codigo).strip()
    
    if codigo not in _df_inventario.index:
        raise Exception("El producto no existe")
    
    df = _df_inventario.copy()
    df = df.drop(codigo)
    
    guardar_inventario(df)


def aumentar_precios_porcentaje(porcentaje):
    _verificar_cache()
    
    if _df_inventario.empty:
        return 0
    
    df = _df_inventario.copy()
    df["precio_venta"] = df["precio_venta"] * (1 + porcentaje / 100)
    
    guardar_inventario(df)
    return len(df)


def agregar_venta(fecha, codigo, producto, cantidad, precio_unitario, total):
    _verificar_cache()
    
    nueva_venta = pd.DataFrame([{
        "fecha": fecha,
        "codigo": codigo,
        "producto": producto,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "total": total
    }])
    
    df = pd.concat([_df_ventas, nueva_venta], ignore_index=True)
    guardar_ventas(df)


def esta_en_sin_stock(codigo):
    _verificar_cache()
    codigo = str(codigo).strip()
    return codigo in _df_sin_stock["codigo"].values


def agregar_a_sin_stock(codigo, producto):
    _verificar_cache()
    
    codigo = str(codigo).strip()
    
    if esta_en_sin_stock(codigo):
        return
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    nuevo = pd.DataFrame([{
        "codigo": codigo,
        "producto": producto,
        "fecha": fecha
    }])
    
    df = pd.concat([_df_sin_stock, nuevo], ignore_index=True)
    guardar_sin_stock(df)
