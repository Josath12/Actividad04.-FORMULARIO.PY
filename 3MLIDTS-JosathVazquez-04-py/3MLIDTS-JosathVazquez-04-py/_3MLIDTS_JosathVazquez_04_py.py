"""
Formulario de Registro de Usuario
----------------------------------
Versión mejorada del formulario original.

Mejoras aplicadas (criterio de ingeniería):
1. Programación orientada a objetos: toda la app vive en una clase,
   evitando variables globales sueltas (tbNombre, var_genero, etc.).
2. Uso de ttk en lugar de tk clásico -> widgets con estilo moderno,
   consistentes con el sistema operativo.
3. Separación de responsabilidades: construcción de UI, validación
   y lógica de negocio están en métodos distintos.
4. Validación de datos antes de "guardar" (edad y estatura numéricas,
   teléfono con formato razonable, campos obligatorios).
5. Layout con grid() en vez de pack() -> alineación exacta tipo
   formulario, en lugar de widgets apilados uno debajo de otro.
6. Type hints y docstrings para legibilidad y mantenimiento.
7. Estilo visual: paleta de colores, tipografía, padding uniforme,
   tarjeta central ("card") en vez de widgets pegados al borde.
8. Atajo de teclado (Enter) y foco automático en el primer campo.
"""

from __future__ import annotations

import re
import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------------------------------------------------
# Configuración visual centralizada (fácil de tocar sin buscar en el código)
# ---------------------------------------------------------------------
class Estilo:
    COLOR_FONDO = "#f3f4f6"
    COLOR_TARJETA = "#ffffff"
    COLOR_PRIMARIO = "#2563eb"
    COLOR_PRIMARIO_HOVER = "#1d4ed8"
    COLOR_PELIGRO = "#ef4444"
    COLOR_PELIGRO_HOVER = "#dc2626"
    COLOR_TEXTO = "#1f2937"
    COLOR_TEXTO_SUAVE = "#6b7280"
    FUENTE_TITULO = ("Segoe UI", 16, "bold")
    FUENTE_LABEL = ("Segoe UI", 10)
    FUENTE_ENTRY = ("Segoe UI", 10)
    FUENTE_BOTON = ("Segoe UI", 10, "bold")


class FormularioUsuario(tk.Tk):
    """Ventana principal del formulario de registro de usuario."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Formulario de Registro de Usuario · v2.0")
        self.geometry("480x560")
        self.minsize(480, 560)
        self.configure(bg=Estilo.COLOR_FONDO)

        self.var_genero = tk.IntVar(value=0)

        self._configurar_estilos_ttk()
        self._construir_interfaz()
        self.tbNombre.focus_set()

    # -----------------------------------------------------------------
    # Configuración de estilos ttk
    # -----------------------------------------------------------------
    def _configurar_estilos_ttk(self) -> None:
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Card.TFrame", background=Estilo.COLOR_TARJETA
        )
        estilo.configure(
            "Titulo.TLabel",
            background=Estilo.COLOR_TARJETA,
            foreground=Estilo.COLOR_TEXTO,
            font=Estilo.FUENTE_TITULO,
        )
        estilo.configure(
            "Campo.TLabel",
            background=Estilo.COLOR_TARJETA,
            foreground=Estilo.COLOR_TEXTO_SUAVE,
            font=Estilo.FUENTE_LABEL,
        )
        estilo.configure(
            "TEntry",
            padding=6,
            fieldbackground="#f9fafb",
            font=Estilo.FUENTE_ENTRY,
        )
        estilo.configure(
            "TRadiobutton",
            background=Estilo.COLOR_TARJETA,
            foreground=Estilo.COLOR_TEXTO,
            font=Estilo.FUENTE_LABEL,
        )
        estilo.configure(
            "Primario.TButton",
            background=Estilo.COLOR_PRIMARIO,
            foreground="white",
            font=Estilo.FUENTE_BOTON,
            padding=10,
            borderwidth=0,
        )
        estilo.map(
            "Primario.TButton",
            background=[("active", Estilo.COLOR_PRIMARIO_HOVER)],
        )
        estilo.configure(
            "Peligro.TButton",
            background=Estilo.COLOR_PELIGRO,
            foreground="white",
            font=Estilo.FUENTE_BOTON,
            padding=10,
            borderwidth=0,
        )
        estilo.map(
            "Peligro.TButton",
            background=[("active", Estilo.COLOR_PELIGRO_HOVER)],
        )

    # -----------------------------------------------------------------
    # Construcción de la interfaz
    # -----------------------------------------------------------------
    def _construir_interfaz(self) -> None:
        contenedor = tk.Frame(self, bg=Estilo.COLOR_FONDO)
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        tarjeta = ttk.Frame(contenedor, style="Card.TFrame", padding=25)
        tarjeta.pack(expand=True, fill="both")

        ttk.Label(
            tarjeta, text="Registro de Usuario", style="Titulo.TLabel"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Diccionario campo -> widget Entry, para simplificar limpiar/leer
        self.tbNombre = self._crear_campo(tarjeta, "Nombres:", 1)
        self.tbApellidos = self._crear_campo(tarjeta, "Apellidos:", 2)
        self.tbTelefono = self._crear_campo(tarjeta, "Teléfono:", 3)
        self.tbEdad = self._crear_campo(tarjeta, "Edad:", 4)
        self.tbEstatura = self._crear_campo(tarjeta, "Estatura (m):", 5)

        # Género
        ttk.Label(tarjeta, text="Género:", style="Campo.TLabel").grid(
            row=6, column=0, sticky="w", pady=(12, 4)
        )
        frame_genero = ttk.Frame(tarjeta, style="Card.TFrame")
        frame_genero.grid(row=7, column=0, columnspan=2, sticky="w")

        ttk.Radiobutton(
            frame_genero, text="Hombre", variable=self.var_genero, value=1
        ).pack(side="left", padx=(0, 15))
        ttk.Radiobutton(
            frame_genero, text="Mujer", variable=self.var_genero, value=2
        ).pack(side="left")

        # Botones de acción
        frame_botones = ttk.Frame(tarjeta, style="Card.TFrame")
        frame_botones.grid(row=8, column=0, columnspan=2, pady=(30, 0), sticky="ew")
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)

        ttk.Button(
            frame_botones,
            text="Borrar valores",
            style="Peligro.TButton",
            command=self.limpiar_campos,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ttk.Button(
            frame_botones,
            text="Guardar",
            style="Primario.TButton",
            command=self.guardar_valores,
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        tarjeta.columnconfigure(1, weight=1)
        self.bind("<Return>", lambda _evento: self.guardar_valores())

    def _crear_campo(self, padre: ttk.Frame, etiqueta: str, fila: int) -> ttk.Entry:
        """Crea una fila con Label + Entry y devuelve el Entry."""
        ttk.Label(padre, text=etiqueta, style="Campo.TLabel").grid(
            row=fila, column=0, sticky="w", pady=(10, 2), columnspan=2
        )
        entry = ttk.Entry(padre)
        entry.grid(row=fila + 1, column=0, columnspan=2, sticky="ew", ipady=3)
        padre.rowconfigure(fila + 1, weight=0)
        return entry
    def limpiar_campos(self) -> None:
        for campo in (
            self.tbNombre,
            self.tbApellidos,
            self.tbTelefono,
            self.tbEdad,
            self.tbEstatura,
        ):
            campo.delete(0, tk.END)
        self.var_genero.set(0)
        self.tbNombre.focus_set()

    def _validar_datos(
        self, nombres: str, apellidos: str, telefono: str, edad: str, estatura: str
    ) -> str | None:
        """Devuelve un mensaje de error si algo es inválido, o None si todo bien."""
        if not nombres.strip() or not apellidos.strip():
            return "El nombre y el apellido son obligatorios."

        if not edad.isdigit() or not (0 < int(edad) < 120):
            return "La edad debe ser un número entero válido (1-119)."

        try:
            valor_estatura = float(estatura.replace(",", "."))
            if not (0.3 < valor_estatura < 2.5):
                return "La estatura debe estar en metros, ej. 1.75."
        except ValueError:
            return "La estatura debe ser un número, ej. 1.75."

        if telefono and not re.fullmatch(r"[\d\s\-\+\(\)]{7,15}", telefono):
            return "El teléfono contiene caracteres no válidos."

        if self.var_genero.get() not in (1, 2):
            return "Selecciona un género."

        return None

    def guardar_valores(self) -> None:
        nombres = self.tbNombre.get()
        apellidos = self.tbApellidos.get()
        telefono = self.tbTelefono.get()
        edad = self.tbEdad.get()
        estatura = self.tbEstatura.get()

        error = self._validar_datos(nombres, apellidos, telefono, edad, estatura)
        if error:
            messagebox.showwarning("Datos incompletos", error)
            return

        genero = "Hombre" if self.var_genero.get() == 1 else "Mujer"

        mensaje = (
            f"Nombre:\n{nombres}\n\n"
            f"Apellido:\n{apellidos}\n\n"
            f"Teléfono:\n{telefono or '—'}\n\n"
            f"Edad:\n{edad}\n\n"
            f"Estatura:\n{estatura} m\n\n"
            f"Género:\n{genero}"
        )
        messagebox.showinfo("Registro de Usuario", mensaje)


if __name__ == "__main__":
    app = FormularioUsuario()
    app.mainloop()