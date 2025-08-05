import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class ModuloAllRegistros:
    def __init__(self, notebook, get_dataframe):
        self.get_dataframe = get_dataframe
        self.tab_all_registros = ttk.Frame(notebook)
        notebook.add(self.tab_all_registros, text="Ver todos los registros")

        # Campo de entrada
        self.label = ttk.Label(self.tab_all_registros, text="Ingresa el ID del empleado para mostrar todos sus registros")
        self.label.pack(pady=5)

        self.entry_id = ttk.Entry(self.tab_all_registros)
        self.entry_id.pack(pady=5)

        # Botón de búsqueda
        self.buscar_button = ttk.Button(self.tab_all_registros, text="Buscar", command=self.buscar)
        self.buscar_button.pack(pady=5)

        # Área de resultados
        self.tree = ttk.Treeview(self.tab_all_registros, show="headings")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(self.tab_all_registros, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def buscar(self):
        df = self.get_dataframe()
        print(df.columns)
        if df is None or df.empty:
            messagebox.showerror("Error", "No hay datos disponibles. Primero importa un archivo.")
            return

        id_empleado = self.entry_id.get().strip()
        if not id_empleado.isdigit():
            messagebox.showwarning("ID inválido", "El ID debe ser un número.")
            return

        id_empleado = int(id_empleado)
        df_filtrado = df[df["idEmpleado"] == id_empleado]

        if df_filtrado.empty:
            messagebox.showinfo("Sin registros", "No se encontraron registros para ese ID.")
            return

        # Agrupar registros por idEmpleado, nombreEmpleado, fecha
        registros_agrupados = (
            df_filtrado
            .sort_values(by=["Fecha", "Hora"])
            .groupby(["idEmpleado", "Empleado", "Fecha"])["Hora"]
            .apply(list)
            .reset_index()
        )

        # Expandir los registros como columnas: registro1, registro2, ...
        max_registros = registros_agrupados["Hora"].apply(len).max()
        for i in range(max_registros):
            registros_agrupados[f"registro{i+1}"] = registros_agrupados["Hora"].apply(
                lambda x: x[i] if i < len(x) else ""
            )

        # Eliminar la columna original "hora"
        registros_agrupados.drop(columns=["Hora"], inplace=True)

        # Mostrar en Treeview
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(registros_agrupados.columns)

        for col in registros_agrupados.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for _, row in registros_agrupados.iterrows():
            self.tree.insert("", "end", values=list(row))
