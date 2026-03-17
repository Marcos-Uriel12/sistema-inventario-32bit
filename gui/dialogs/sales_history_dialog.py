import customtkinter as ctk
import sales_manager


class SalesHistoryDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historial de Ventas")
        self.geometry("800x500")
        self.configure(fg_color="#000000")
        self.transient(parent)
        self.grab_set()

        self._setup_ui()
        self._cargar_ventas()

    def _setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="#000000")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            main_frame,
            text="HISTORIAL DE VENTAS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=(0, 20))

        headers_frame = ctk.CTkFrame(main_frame, fg_color="#333333", height=35)
        headers_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(headers_frame, text="Fecha", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=150).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(headers_frame, text="Código", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=80).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(headers_frame, text="Producto", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=150).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(headers_frame, text="Cantidad", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=70).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(headers_frame, text="P. Unit", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=80).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(headers_frame, text="Total", font=ctk.CTkFont(size=12, weight="bold"), text_color="white", width=100).pack(side="left", padx=5, pady=5)

        self.ventas_scroll = ctk.CTkScrollableFrame(main_frame, fg_color="#1a1a1a")
        self.ventas_scroll.pack(fill="both", expand=True, pady=(0, 15))

        total_ventas = sales_manager.obtener_ventas()
        total = sum(v.get("total", 0) for v in total_ventas)

        self.total_label = ctk.CTkLabel(
            main_frame,
            text=f"Total de ventas: ${total:.2f}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2fa572"
        )
        self.total_label.pack(pady=(0, 15))

        cerrar_btn = ctk.CTkButton(
            main_frame,
            text="CERRAR",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#c93535",
            hover_color="#a12828",
            text_color="white",
            command=self.destroy
        )
        cerrar_btn.pack(fill="x")

    def _cargar_ventas(self):
        ventas = sales_manager.obtener_ventas()
        
        for widget in self.ventas_scroll.winfo_children():
            widget.destroy()
        
        if not ventas:
            ctk.CTkLabel(
                self.ventas_scroll,
                text="No hay ventas registradas",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            ).pack(pady=20)
            return
        
        for venta in ventas:
            item_frame = ctk.CTkFrame(self.ventas_scroll, fg_color="#1a1a1a", height=30)
            item_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(item_frame, text=str(venta.get("fecha", "-"))[:19], font=ctk.CTkFont(size=11), text_color="white", width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(item_frame, text=str(venta.get("codigo", "-")), font=ctk.CTkFont(size=11), text_color="white", width=80).pack(side="left", padx=5)
            ctk.CTkLabel(item_frame, text=str(venta.get("producto", "-"))[:20], font=ctk.CTkFont(size=11), text_color="white", width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(item_frame, text=str(venta.get("cantidad", "-")), font=ctk.CTkFont(size=11), text_color="white", width=70).pack(side="left", padx=5)
            ctk.CTkLabel(item_frame, text=f"${venta.get('precio_unitario', 0):.2f}", font=ctk.CTkFont(size=11), text_color="white", width=80).pack(side="left", padx=5)
            ctk.CTkLabel(item_frame, text=f"${venta.get('total', 0):.2f}", font=ctk.CTkFont(size=11, weight="bold"), text_color="#2fa572", width=100).pack(side="left", padx=5)
