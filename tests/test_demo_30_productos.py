import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inventory_manager
import sales_manager
import excel_manager


def test_agregar_30_productos_y_vender_5():
    """Test: Agregar 30 productos y vender 5"""
    
    productos_creados = []
    
    print("\n=== AGREGANDO 30 PRODUCTOS ===")
    for i in range(1, 31):
        codigo = f"P{i:03d}"
        producto = f"Producto {i}"
        precio_compra = 10 + i
        precio_venta = 20 + (i * 2)
        stock = 10 + i
        
        try:
            inventory_manager.agregar_producto(codigo, producto, precio_compra, precio_venta, stock)
            productos_creados.append(codigo)
            print(f"  [OK] Agregado: {codigo} - {producto} (Stock: {stock}, Precio: ${precio_venta})")
        except Exception as e:
            print(f"  [X] Error agregando {codigo}: {e}")
    
    print(f"\nTotal productos creados: {len(productos_creados)}")
    
    inventario = inventory_manager.ver_productos()
    print(f"Productos en inventario: {len(inventario)}")
    
    print("\n=== VENDIENDO 5 PRODUCTOS ===")
    ventas_realizadas = []
    
    codigos_vender = ["P001", "P005", "P010", "P015", "P020"]
    
    for codigo in codigos_vender:
        try:
            resultado = sales_manager.registrar_venta(codigo, 1)
            if resultado[0]:
                datos = resultado[1]
                ventas_realizadas.append(codigo)
                print(f"  [OK] Vendido: {codigo} - {datos['producto']} (${datos['total']})")
        except Exception as e:
            print(f"  [X] Error vendiendo {codigo}: {e}")
    
    print(f"\nTotal ventas realizadas: {len(ventas_realizadas)}")
    
    print("\n=== VERIFICANDO STOCK DESPUES DE VENTAS ===")
    for codigo in codigos_vender:
        producto = inventory_manager.buscar_producto(codigo)
        if producto:
            print(f"  {codigo}: Stock remaining = {producto['stock']}")
    
    print("\n=== VERIFICANDO VENTAS EN EXCEL ===")
    ventas = sales_manager.obtener_ventas()
    print(f"Total ventas registradas: {len(ventas)}")
    
    print("\n=== VERIFICANDO SIN STOCK ===")
    sin_stock = sales_manager.obtener_sin_stock()
    print(f"Productos sin stock: {len(sin_stock)}")
    
    print("\n=== TEST COMPLETADO ===")
    print(f"Productos agregados: {len(productos_creados)}")
    print(f"Ventas realizadas: {len(ventas_realizadas)}")
    
    return True
