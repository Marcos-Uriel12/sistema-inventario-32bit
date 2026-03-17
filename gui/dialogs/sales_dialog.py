import customtkinter as ctk
import sales_manager
from .error_dialog import show_error_popup


class SalesDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_success=None):
        super().__init__(parent)
        self.on_success = on_success
        self.carrito = []
        self.producto_actual = None
        self.title("Nueva Venta")
        self.geometry("900x600")
        self.configure(fg_color="#000000")
        self.transient(parent)
        self.grab_set()

        self._setup_ui()

    def _setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="#000000")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            main_frame,
            text="NUEVA VENTA",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=(0, 20))

        content_frame = ctk.CTkFrame(main_frame, fg_color="#000000")
        content_frame.pack(fill="both", expand=True)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=2)

        left_frame = ctk.CTkFrame(content_frame, fg_color="#000000")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        right_frame = ctk.CTkFrame(content_frame, fg_color="#000000")
        right_frame.grid(row=0, column=1, sticky="nsew")

        search_label = ctk.CTkLabel(
            left_frame,
            text="Buscar producto:",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        search_label.pack(pady=(0, 5))

        self.search_entry = ctk.CTkEntry(
            left_frame,
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color="#1a1a1a",
            text_color="white",
            border_color="#333333",
            placeholder_text="Código o nombre del producto",
            placeholder_text_color="#888888"
        )
        self.search_entry.pack(fill="x", pady=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self._buscar_producto())

        buscar_btn = ctk.CTkButton(
            left_frame,
            text="Buscar",
            height=40,
            fg_color="#1f538d",
            hover_color="#143b6f",
            text_color="white",
            command=self._buscar_producto
        )
        buscar_btn.pack(fill="x", pady=(0, 20))

        self.producto_info_frame = ctk.CTkFrame(left_frame, fg_color="#1a1a1a")
        self.producto_info_frame.pack(fill="x", pady=(0, 20))

        self.info_nombre_label = ctk.CTkLabel(
            self.producto_info_frame,
            text="Producto: -",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.info_nombre_label.pack(pady=5, padx=10, anchor="w")

        self.info_precio_label = ctk.CTkLabel(
            self.producto_info_frame,
            text="Precio: -",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.info_precio_label.pack(pady=5, padx=10, anchor="w")

        self.info_stock_label = ctk.CTkLabel(
            self.producto_info_frame,
            text="Stock: -",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.info_stock_label.pack(pady=5, padx=10, anchor="w")

        cantidad_label = ctk.CTkLabel(
            left_frame,
            text="Cantidad:",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        cantidad_label.pack(pady=(0, 5))

        self.cantidad_entry = ctk.CTkEntry(
            left_frame,
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color="#1a1a1a",
            text_color="white",
            border_color="#333333",
            placeholder_text="1",
            placeholder_text_color="#888888"
        )
        self.cantidad_entry.pack(fill="x", pady=(0, 15))

        agregar_btn = ctk.CTkButton(
            left_frame,
            text="Agregar al carrito",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            text_color="white",
            command=self._agregar_al_carrito
        )
        agregar_btn.pack(fill="x")

        self.cart_label = ctk.CTkLabel(
            right_frame,
            text="Carrito",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        self.cart_label.pack(pady=(0, 10))

        cart_headers = ctk.CTkFrame(right_frame, fg_color="#333333", height=35)
        cart_headers.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(cart_headers, text="Producto", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=150).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(cart_headers, text="Precio", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=80).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(cart_headers, text="Cant", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=60).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(cart_headers, text="Subtotal", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=80).pack(side="left", padx=5, pady=5)

        self.cart_scroll = ctk.CTkScrollableFrame(right_frame, fg_color="#1a1a1a")
        self.cart_scroll.pack(fill="both", expand=True, pady=(0, 15))

        self.total_label = ctk.CTkLabel(
            right_frame,
            text="Total: $0.00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2fa572"
        )
        self.total_label.pack(pady=(0, 15))

        buttons_frame = ctk.CTkFrame(right_frame, fg_color="#000000")
        buttons_frame.pack(fill="x")

        vender_btn = ctk.CTkButton(
            buttons_frame,
            text="VENDER",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2fa572",
            hover_color="#238551",
            text_color="white",
            command=self._vender
        )
        vender_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))

        cancelar_btn = ctk.CTkButton(
            buttons_frame,
            text="CANCELAR",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#c93535",
            hover_color="#a12828",
            text_color="white",
            command=self.destroy
        )
        cancelar_btn.pack(side="left", expand=True, fill="x")

    def _buscar_producto(self):
        busqueda = self.search_entry.get().strip()
        
        if not busqueda:
            return
        
        producto = None
        
        producto = sales_manager.get_producto(busqueda)
        
        if not producto:
            resultados = sales_manager.buscar_productos(busqueda)
            if resultados:
                producto = resultados[0]
        
        if producto:
            self.producto_actual = producto
            self.info_nombre_label.configure(text=f"Producto: {producto['producto']}")
            self.info_precio_label.configure(text=f"Precio: ${producto['precio_venta']:.2f}")
            self.info_stock_label.configure(text=f"Stock: {producto['stock']}")
        else:
            self.producto_actual = None
            self.info_nombre_label.configure(text="Producto: No encontrado")
            self.info_precio_label.configure(text="Precio: -")
            self.info_stock_label.configure(text="Stock: -")
            show_error_popup(self, "Producto no encontrado")

    def _agregar_al_carrito(self):
        if not self.producto_actual:
            show_error_popup(self, "Debe buscar un producto primero")
            return
        
        cantidad_texto = self.cantidad_entry.get().strip()
        if not cantidad_texto:
            show_error_popup(self, "Ingrese la cantidad")
            return
        
        try:
            cantidad = int(cantidad_texto)
        except ValueError:
            show_error_popup(self, "La cantidad debe ser un número")
            return
        
        if cantidad <= 0:
            show_error_popup(self, "La cantidad debe ser mayor a 0")
            return
        
        if cantidad > self.producto_actual["stock"]:
            show_error_popup(self, f"Stock insuficiente. Stock actual: {self.producto_actual['stock']}")
            return
        
        subtotal = self.producto_actual["precio_venta"] * cantidad
        
        self.carrito.append({
            "codigo": self.producto_actual["codigo"],
            "producto": self.producto_actual["producto"],
            "precio": self.producto_actual["precio_venta"],
            "cantidad": cantidad,
            "subtotal": subtotal
        })
        
        self._actualizar_carrito()

    def _actualizar_carrito(self):
        for widget in self.cart_scroll.winfo_children():
            widget.destroy()
        
        total = 0
        for item in self.carrito:
            item_frame = ctk.CTkFrame(self.cart_scroll, fg_color="#1a1a1a", height=30)
            item_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(item_frame, text=item["producto"][:20], font=ctk.CTkFont(size=12), text_color="white", width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(item_frame, text=f"${item['precio']:.2f}", font=ctk.CTkFont(size=12), text_color="white", width=80).pack(side="left", padx=5)
            ctk.CTkLabel(item_frame, text=str(item["cantidad"]), font=ctk.CTkFont(size=12), text_color="white", width=60).pack(side="left", padx=5)
            ctk.CTkLabel(item_frame, text=f"${item['subtotal']:.2f}", font=ctk.CTkFont(size=12), text_color="white", width=80).pack(side="left", padx=5)
            
            total += item["subtotal"]
        
        self.total_label.configure(text=f"Total: ${total:.2f}")
        self.cantidad_entry.delete(0, "end")

    def _vender(self):
        if not self.carrito:
            show_error_popup(self, "El carrito está vacío")
            return
        
        try:
            for item in self.carrito:
                sales_manager.registrar_venta(item["codigo"], item["cantidad"])
            
            self.carrito = []
            self.destroy()
            if self.on_success:
                self.on_success()
        except ValueError as e:
            show_error_popup(self, str(e))
        except Exception as e:
            show_error_popup(self, f"Error al registrar venta: {str(e)}")
