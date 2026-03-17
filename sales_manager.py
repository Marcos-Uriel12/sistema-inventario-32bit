import excel_manager
from datetime import datetime


def registrar_venta(codigo, cantidad):
    codigo = str(codigo).strip()
    
    if not codigo:
        raise ValueError("El código no puede estar vacío")
    
    try:
        cantidad = int(cantidad)
    except ValueError:
        raise ValueError("La cantidad debe ser un número entero")
    
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0")
    
    if not excel_manager.existe_producto(codigo):
        raise ValueError("El producto no existe")
    
    producto = excel_manager.leer_producto(codigo)
    
    stock_actual = producto["stock"]
    
    if stock_actual < cantidad:
        raise ValueError(f"Stock insuficiente. Stock actual: {stock_actual}")
    
    nuevo_stock = stock_actual - cantidad
    
    excel_manager.actualizar_stock(codigo, nuevo_stock)
    
    precio_unitario = producto["precio_venta"]
    total = precio_unitario * cantidad
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    excel_manager.agregar_venta(
        fecha=fecha,
        codigo=codigo,
        producto=producto["producto"],
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        total=total
    )
    
    if nuevo_stock == 0:
        excel_manager.agregar_a_sin_stock(codigo, producto["producto"])
    
    return True, {
        "codigo": codigo,
        "producto": producto["producto"],
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "total": total
    }


def obtener_ventas():
    df = excel_manager.cargar_ventas()
    if df.empty:
        return []
    return df.to_dict("records")


def obtener_sin_stock():
    df = excel_manager.cargar_sin_stock()
    if df.empty:
        return []
    return df.to_dict("records")


def buscar_productos(nombre):
    return excel_manager.buscar_producto_por_nombre(nombre)


def get_producto(codigo):
    return excel_manager.leer_producto(codigo)
