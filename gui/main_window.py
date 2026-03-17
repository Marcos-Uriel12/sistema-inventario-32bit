import tkinter as tk
from tkinter import ttk
import inventory_manager
from .components.toolbar import Toolbar
from .components.search_bar import SearchBar
from .components.product_table import ProductTable
from .dialogs.add_product_dialog import AddProductDialog
from .dialogs.update_product_dialog import UpdateProductDialog
from .dialogs.delete_product_dialog import DeleteProductDialog
from .dialogs.update_prices_dialog import UpdatePricesDialog
from .dialogs.sales_dialog import SalesDialog
from .dialogs.sales_history_dialog import SalesHistoryDialog


class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.productos = []
        self.productos_filtrados = []
        self.sort_option = None

        self._setup_ui()
        self._load_products()

    def _setup_ui(self):
        self.configure(bg="#000000")
        
        top_frame = tk.Frame(self, height=120, bg="#000000")
        top_frame.pack(fill="x", padx=15, pady=(15, 10))
        top_frame.pack_propagate(False)

        self.toolbar = Toolbar(
            top_frame,
            on_add_product=self._on_add_product,
            on_refresh=self._load_products,
            on_sort=self._on_sort,
            on_update_prices=self._on_update_prices,
            on_sell=self._on_sell,
            on_view_sales=self._on_view_sales
        )
        self.toolbar.pack(fill="x", pady=(10, 15))

        self.search_bar = SearchBar(
            top_frame,
            on_search=self._on_search
        )
        self.search_bar.pack(fill="x")

        self.table = ProductTable(
            self,
            on_update=self._on_update_product,
            on_delete=self._on_delete_product
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _load_products(self):
        self.productos = inventory_manager.ver_productos()
        self.productos_filtrados = self.productos.copy()
        if self.sort_option:
            self._apply_sort()
        self._refresh_table()

    def _refresh_table(self):
        self.table.clear()
        for producto in self.productos_filtrados:
            self.table.insert_producto(producto)

    def _on_search(self, query):
        if not query:
            self.productos_filtrados = self.productos.copy()
        else:
            query_lower = query.lower()
            self.productos_filtrados = [
                p for p in self.productos
                if query_lower in str(p.get("codigo", "")).lower()
                or query_lower in str(p.get("producto", "")).lower()
            ]
        if self.sort_option:
            self._apply_sort()
        self._refresh_table()

    def _on_sort(self, option):
        self.sort_option = option
        self._apply_sort()
        self._refresh_table()

    def _apply_sort(self):
        if not self.sort_option:
            return

        reverse = False
        key = "precio_venta"

        if self.sort_option == "precio_venta_mayor":
            reverse = True
        elif self.sort_option == "precio_venta_menor":
            reverse = False
        elif self.sort_option == "stock_mayor":
            key = "stock"
            reverse = True
        elif self.sort_option == "stock_menor":
            key = "stock"
            reverse = False

        self.productos_filtrados = sorted(
            self.productos_filtrados,
            key=lambda x: float(x.get(key, 0)),
            reverse=reverse
        )

    def _on_add_product(self):
        dialog = AddProductDialog(self.parent, on_success=self._load_products)

    def _on_update_prices(self):
        dialog = UpdatePricesDialog(self.parent, on_success=self._load_products)

    def _on_update_product(self, producto):
        dialog = UpdateProductDialog(
            self.parent,
            producto,
            on_success=self._load_products
        )

    def _on_delete_product(self, producto):
        dialog = DeleteProductDialog(
            self.parent,
            producto,
            on_success=self._load_products
        )

    def _on_sell(self):
        dialog = SalesDialog(self.parent, on_success=self._load_products)

    def _on_view_sales(self):
        dialog = SalesHistoryDialog(self.parent)
