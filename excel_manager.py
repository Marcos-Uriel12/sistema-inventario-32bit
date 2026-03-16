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

COLUMNAS = ["codigo", "producto", "precio_compra", "precio_venta", "stock"]

_df_cache = None
_cache_mtime = None


def _inicializar_cache():
    global _df_cache, _cache_mtime
    
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    if not INVENTORY_FILE.exists():
        _df_cache = pd.DataFrame(columns=COLUMNAS)
        _df_cache.set_index("codigo", inplace=True)
        _df_cache.to_excel(INVENTORY_FILE, index=True)
        _cache_mtime = INVENTORY_FILE.stat().st_mtime
        return
    
    try:
        df = pd.read_excel(INVENTORY_FILE, index_col=0)
        if df.empty:
            _df_cache = pd.DataFrame(columns=COLUMNAS)
            _df_cache.set_index("codigo", inplace=True)
        else:
            _df_cache = df
            _df_cache.index = _df_cache.index.astype(str)
        _cache_mtime = INVENTORY_FILE.stat().st_mtime
    except Exception:
        _df_cache = pd.DataFrame(columns=COLUMNAS)
        _df_cache.set_index("codigo", inplace=True)
        _df_cache.to_excel(INVENTORY_FILE, index=True)
        _cache_mtime = INVENTORY_FILE.stat().st_mtime


def _verificar_cache():
    global _df_cache, _cache_mtime
    
    if _df_cache is None:
        _inicializar_cache()
        return
    
    if not INVENTORY_FILE.exists():
        _df_cache = pd.DataFrame(columns=COLUMNAS)
        _df_cache.set_index("codigo", inplace=True)
        _df_cache.to_excel(INVENTORY_FILE, index=True)
        _cache_mtime = INVENTORY_FILE.stat().st_mtime
        return
    
    try:
        current_mtime = INVENTORY_FILE.stat().st_mtime
        if current_mtime != _cache_mtime:
            _inicializar_cache()
    except Exception:
        _inicializar_cache()


def cargar_datos():
    _verificar_cache()
    return _df_cache.copy()


def guardar_datos(df, crear_backup=True):
    global _df_cache, _cache_mtime
    
    if crear_backup:
        _crear_backup()
    
    try:
        df_to_save = df.copy()
        df_to_save.to_excel(INVENTORY_FILE, index=True)
        _df_cache = df.copy()
        _cache_mtime = INVENTORY_FILE.stat().st_mtime
    except PermissionError:
        raise Exception("El archivo está abierto en Excel. Ciérrelo e intente de nuevo.")
    except FileNotFoundError:
        raise Exception("No se encontró el archivo de inventario.")
    except Exception as e:
        raise Exception(f"Error al guardar: {e}")


def _crear_backup():
    if not INVENTORY_FILE.exists():
        return
    
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"inventario_backup_{timestamp}.xlsx"
    
    try:
        df = pd.read_excel(INVENTORY_FILE, index_col=0)
        df.to_excel(backup_file, index=True)
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
    return codigo in _df_cache.index


def leer_producto(codigo):
    _verificar_cache()
    codigo = str(codigo).strip()
    
    if codigo not in _df_cache.index:
        return None
    
    producto = _df_cache.loc[codigo]
    data = producto.to_dict()
    data["codigo"] = codigo
    return data


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
    
    df = _df_cache.copy()
    df = pd.concat([df, nuevo])
    
    guardar_datos(df)


def actualizar_producto(codigo, datos):
    _verificar_cache()
    
    codigo = str(codigo).strip()
    
    if codigo not in _df_cache.index:
        raise Exception("El producto no existe")
    
    df = _df_cache.copy()
    for clave, valor in datos.items():
        df.at[codigo, clave] = valor
    
    guardar_datos(df)


def eliminar_producto(codigo):
    _verificar_cache()
    
    codigo = str(codigo).strip()
    
    if codigo not in _df_cache.index:
        raise Exception("El producto no existe")
    
    df = _df_cache.copy()
    df = df.drop(codigo)
    
    guardar_datos(df)


def aumentar_precios_porcentaje(porcentaje):
    _verificar_cache()
    
    if _df_cache.empty:
        return 0
    
    df = _df_cache.copy()
    df["precio_venta"] = df["precio_venta"] * (1 + porcentaje / 100)
    
    guardar_datos(df)
    return len(df)
