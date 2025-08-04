#Importamos tkinter para poder seguir con lo visual
import tkinter as tk
#Importamos ttk y messagebox para mostrar información al usuairo
from tkinter import ttk, messagebox
#Importamos pandas para poder trabajar con tablas
import pandas as pd

class ModuloBuscar:
    def __init__(self, notebook, get_resumen_func):
        self.get_dataframe = get_resumen_func
        self.tab_buscar = ttk.Frame(notebook)
        notebook.add(self.tab_buscar, text="Buscar Registro por ID")

        #Campo de entrada
        self.label = ttk.Label(self.tab_buscar, text="Ingresa el ID del empleado: ")
        self.label.pack(pady=5)
        
        self.entry_id = ttk.Entry(self.tab_buscar)
        self.entry_id.pack(pady=5)

        #Botón de busqueda.
        self.button_buscar = ttk.Button(self.tab_buscar, text="Buscar", command=self.buscar)
        self.button_buscar.pack(pady=5)

        #Area de los resultados
        self.tree = ttk.Treeview(self.tab_buscar, show="headings")
        self.tree.pack(expand=True, fill="both",padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(self.tab_buscar, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)


    def buscar(self):
        resumen = self.get_dataframe()
        if resumen is None or resumen.empty:
            messagebox.showerror("Resumen no disponible", "Primero debes generar el resumen desde su pestaña.")
            return

        id_empleado = self.entry_id.get().strip()
        if not id_empleado.isdigit():
            messagebox.showwarning("ID inválido", "El ID debe ser un número.")
            return

        id_empleado = int(id_empleado)
        filtrado = resumen[resumen["idEmpleado"] == id_empleado]

        if filtrado.empty:
            messagebox.showinfo("Sin resultados", "No se encontraron registros con ese ID.")
            return

        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(filtrado.columns)

        for col in filtrado.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for _, row in filtrado.iterrows():
            self.tree.insert("", "end", values=list(row))



