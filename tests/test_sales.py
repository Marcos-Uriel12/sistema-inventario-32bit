import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inventory_manager
import sales_manager
import excel_manager


class TestVentas:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_codigo = "TESTV001"
        if excel_manager.existe_producto(self.test_codigo):
            excel_manager.eliminar_producto(self.test_codigo)
        
        excel_manager.escribir_producto(
            self.test_codigo,
            "Producto Venta Test",
            50,
            100,
            10
        )
        yield
        if excel_manager.existe_producto(self.test_codigo):
            excel_manager.eliminar_producto(self.test_codigo)

    def test_registrar_venta_reduce_stock(self):
        producto_antes = sales_manager.get_producto(self.test_codigo)
        stock_inicial = producto_antes["stock"]
        
        resultado = sales_manager.registrar_venta(self.test_codigo, 3)
        
        assert resultado[0] is True
        
        producto_despues = sales_manager.get_producto(self.test_codigo)
        assert producto_despues["stock"] == stock_inicial - 3

    def test_venta_stock_insuficiente(self):
        with pytest.raises(ValueError, match="Stock insuficiente"):
            sales_manager.registrar_venta(self.test_codigo, 100)

    def test_venta_cantidad_invalida(self):
        with pytest.raises(ValueError, match="La cantidad debe ser mayor a 0"):
            sales_manager.registrar_venta(self.test_codigo, 0)

        with pytest.raises(ValueError, match="La cantidad debe ser un número entero"):
            sales_manager.registrar_venta(self.test_codigo, "abc")

    def test_venta_producto_no_existe(self):
        with pytest.raises(ValueError, match="El producto no existe"):
            sales_manager.registrar_venta("NOEXISTE", 1)

    def test_total_calculo_correcto(self):
        resultado = sales_manager.registrar_venta(self.test_codigo, 2)
        
        assert resultado[0] is True
        datos = resultado[1]
        assert datos["cantidad"] == 2
        assert datos["precio_unitario"] == 100
        assert datos["total"] == 200

    def test_ventas_en_excel(self):
        sales_manager.registrar_venta(self.test_codigo, 1)
        
        ventas = sales_manager.obtener_ventas()
        
        assert len(ventas) > 0
        ultima_venta = ventas[-1]
        assert ultima_venta["codigo"] == self.test_codigo
        assert ultima_venta["cantidad"] == 1
        assert ultima_venta["total"] == 100

    def test_buscar_producto_por_nombre(self):
        resultados = sales_manager.buscar_productos("Venta Test")
        
        assert len(resultados) > 0
        assert resultados[0]["producto"] == "Producto Venta Test"

    def test_venta_multiple_productos(self):
        codigo2 = "TESTV002"
        if excel_manager.existe_producto(codigo2):
            excel_manager.eliminar_producto(codigo2)
        
        excel_manager.escribir_producto(codigo2, "Producto 2", 30, 60, 5)
        
        try:
            r1 = sales_manager.registrar_venta(self.test_codigo, 2)
            r2 = sales_manager.registrar_venta(codigo2, 3)
            
            assert r1[0] is True
            assert r2[0] is True
            
            ventas = sales_manager.obtener_ventas()
            assert len(ventas) >= 2
        finally:
            if excel_manager.existe_producto(codigo2):
                excel_manager.eliminar_producto(codigo2)

    def test_sin_stock_actualizado(self):
        codigo3 = "TESTV003"
        if excel_manager.existe_producto(codigo3):
            excel_manager.eliminar_producto(codigo3)
        
        excel_manager.escribir_producto(codigo3, "Producto Stock 1", 10, 20, 1)
        
        try:
            assert not excel_manager.esta_en_sin_stock(codigo3)
            
            sales_manager.registrar_venta(codigo3, 1)
            
            assert excel_manager.esta_en_sin_stock(codigo3)
        finally:
            if excel_manager.existe_producto(codigo3):
                excel_manager.eliminar_producto(codigo3)
