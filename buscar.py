#Importamos tkinter para poder seguir con lo visual
import tkinter as tk
#Importamos ttk y messagebox para mostrar información al usuairo
from tkinter import ttk, messagebox
#Importamos pandas para poder trabajar con tablas
import pandas as pd

#Definimos nuestra clase para nuestro módulo buscar
class ModuloBuscar:
    def __init__(self, notebook, get_resumen_func):

        #Obtenemos nuestro df generado en el resumen para ver el reporte individual de las personas.
        self.get_dataframe = get_resumen_func
        self.tab_buscar = ttk.Frame(notebook)
        notebook.add(self.tab_buscar, text="Buscar Registro por ID")

        #Campo de entrada
        self.label = ttk.Label(self.tab_buscar, text="Ingresa el ID del empleado: ")
        self.label.pack(pady=5)
        #Este el bloque para definir la entrada para la busquéda
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

    #Creamos una nueva función para hacer la búsqueda.
    def buscar(self):
        #Creamos una variable resumen para almacenar el dataframe generado en nuestro resumen
        resumen = self.get_dataframe()
        #Si el dataframe está vació o es None entonces mostramos un mensaje de error porque no se ha generado un resumen.
        if resumen is None or resumen.empty:
            messagebox.showerror("Resumen no disponible", "Primero debes generar el resumen desde su pestaña.")
            return
        #Definimos que el id a buscar será el que se introduzca desde nuestro entry
        id_empleado = self.entry_id.get().strip()
        #Si el id que se introduzca no es un dígito mostramos entonces el error correspondiente
        if not id_empleado.isdigit():
            #Mostramos un mensaje de Warning en caso de que el ID no sea válido
            messagebox.showwarning("ID inválido", "El ID debe ser un número.")
            return
        #En caso contrario reasignamos la varibale id_empleado pero ahora como un entero
        id_empleado = int(id_empleado)
        #Hacemos el filtrado dentro de nuestro df de resumen y buscamos por el id_empleado
        filtrado = resumen[resumen["idEmpleado"] == id_empleado]
        #Si nuestro filtrado es vació o no encontró ese id dentro de nuestro df entonces mostramos un mensaje de que no hay resultados.
        if filtrado.empty:
            messagebox.showinfo("Sin resultados", "No se encontraron registros con ese ID.")
            return
        #Si encontramos entonces el id dentro de nuestro df comenzamos a llenar nuestro árbol para mostrar la información.
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(filtrado.columns)

        #Llenamos las columnas
        for col in filtrado.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        #Llenamos las filas
        for _, row in filtrado.iterrows():
            self.tree.insert("", "end", values=list(row))



