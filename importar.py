import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

#Creamos nuestra clase para importar nuestro df
class ModuloImportar:
    def __init__(self, notebook, set_dataframe_func):
        self.set_dataframe = set_dataframe_func
        self.df = None

        #Ponemos el texto que indica que nuestro modulo es de importar el archivo
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="Importar archivo")
        #Generamos un botón para cargar los archivos.
        btn_cargar = ttk.Button(self.tab, text="Cargar Archivo CSV/XLSX", command=self.cargar_archivo)
        btn_cargar.pack(pady=10)
        #Definimos nuestro mensaje en caso de no tener un archivo cargado.
        self.label_archivo = ttk.Label(self.tab, text="Ningún archivo cargado")
        self.label_archivo.pack(pady=5)
        #Definimos nuestros headings y les damos estilo.
        self.tree = ttk.Treeview(self.tab, show="headings")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def cargar_archivo(self):
        #Definimos que ruta es la que se va a abrir
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=(("CSV", "*.csv"), ("Excel", "*.xlsx"), ("Todos", "*.*"))
        )
        #Si no se abre ninguna ruta entonces retornamos automaticamente.
        if not ruta:
            return
        #Hacemos un bloque try en caso de recibir error no romper el programa.
        try:
            #Si la ruta seleccionada fue .csv entonces
            if ruta.endswith(".csv"):
                #Indicamos que nuestro header no será nada
                df = pd.read_csv(ruta, header=None)
                #Definimos los nombres de nuestras columnas
                df.columns = ["Vacia1", "idEmpleado", "Empleado", "Fecha", "Vacia2", "Vacia3", "Normal"]
                #Este bloque es para separar la fecha y hora
                df["Fecha"] = df["Fecha"].astype(str).str.strip()
                df["FechaHora"] = pd.to_datetime(df["Fecha"], errors="coerce")
                df["Fecha"] = df["FechaHora"].dt.date.astype(str)
                df["Hora"] = df["FechaHora"].dt.time.astype(str)
                #Eliminamos estas columnas que son información vacía que no nos sirve para hacer los reportes
                df = df.drop(columns=["Vacia1", "Vacia2", "Vacia3", "Normal", "FechaHora"])
                #Definimos nuestro df completo ahora si.
                df = df[["idEmpleado", "Empleado", "Fecha", "Hora"]]
            #En caso que la ruta termine con .xlsx entonces hacemos el siguiente bloque de instrucciones
            elif ruta.endswith(".xlsx"):
                #Definimos la ruta y además que no tendrá Header, esta parte la tenemos que validar todavía
                df = pd.read_excel(ruta, header=None)
            else:
                #En caso de abrir un formato no compatible, mostramos el mensaje correspondiente
                messagebox.showerror("Error", "Formato no compatible.")
                return

            #Hacemos la asignación a nuestro df
            self.df = df
            self.set_dataframe(df)
            #Mostramos un mensaje que el archivo cargado y además la ruta/nombre del archivo que cargamos
            self.label_archivo.config(text=f"Archivo cargado: {os.path.basename(ruta)}")
            #Mostramos el df.
            self.mostrar_dataframe_en_treeview(df)
        #En caso de tener error durante la lectura de nuestro archivo entonces
        except Exception as e:#Obtenemos el error
            messagebox.showerror("Error", str(e))#Mostramos en un mensaje el error al abrir el archivo que queríamos usar
    
    #Esta es nuestra función para mostrar el dataframe dentro de nuestro tree
    def mostrar_dataframe_en_treeview(self, df):
        self.tree.delete(*self.tree.get_children())
        #Definimos nuestras columas, además de asignarle tamaños y el texto
        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=str(col))
            self.tree.column(col, width=100)
        
        #Definimos nestras filas y mostramos la información correspondiente.
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

        