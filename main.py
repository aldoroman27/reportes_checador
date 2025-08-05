#Importamos tkinter para poder crear la interfáz gráfica
import tkinter as tk
#Importamos los módulos que nos ayudarán para la gestión de archivos, mensajes emergentes, etc
from tkinter import ttk
#Importamos la librería de os para trabajar con operaciones relacionadas al sistema operativo
from importar import ModuloImportar
from resumen import ModuloResumen
from buscar import ModuloBuscar
from todoslosRegistros import ModuloAllRegistros

class AsistenciaApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Sistema de control de Asistencias DEMO")
        self.root.geometry("1000x600")
        self.root.configure(bg="#e8f6f9")

        self.mejorar_interfaz()

        titulo = ttk.Label(
            root,text="Sistema de Asistencia",
            font=("Segoe",18,"bold"), foreground="#2a4d69",background="#e8f6f9"
        )

        titulo.pack(pady=15)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.def_original = None

        self.importar = ModuloImportar(self.notebook, self.set_dataframe)
        self.resumen = ModuloResumen(self.notebook, self.get_dataframe)
        self.buscar = ModuloBuscar(self.notebook, self.resumen.get_resumen_df)
        self.todoslosRegistros = ModuloAllRegistros(self.notebook, self.get_dataframe)

    def mejorar_interfaz(self):
         
        #Definimos los estilos de la página para que se vea un entorno más limpio
        style = ttk.Style()
        style.theme_use("clam")

        # Colores base
        azul = "#2a9d8f"
        celeste = "#e0fbfc"
        gris_claro = "#f0f0f0"

        # Notebook
        style.configure("TNotebook", background=celeste, borderwidth=0)
        style.configure("TNotebook.Tab", background=gris_claro, padding=[12, 6],
                    font=("Segoe UI", 10, "bold"), foreground="#264653")
        style.map("TNotebook.Tab", background=[("selected", azul)],
            foreground=[("selected", "white")])

        # Botones
        style.configure("TButton", font=('Segoe UI', 10), padding=6,
                        background=azul, foreground="white")
        style.map("TButton",
            background=[("active", "#21867a"), ("pressed", "#1e6f63")],
            foreground=[("disabled", "#cccccc")])

        # Labels
        style.configure("TLabel", font=("Segoe UI", 10), background=celeste)

        # Treeview
        style.configure("Treeview",
                    font=('Segoe UI', 10),
                        background="white",
                        fieldbackground="white",
                        rowheight=26)
        style.configure("Treeview.Heading",
                        font=('Segoe UI', 10, 'bold'),
                        background=azul,
                        foreground="white")
        style.map("Treeview.Heading",
                    background=[("active", "#21867a")])

    def set_dataframe(self, df):
        self.df_original = df

    def get_dataframe(self):
        return self.df_original

if __name__ == "__main__":
    root = tk.Tk()
    app = AsistenciaApp(root)
    root.mainloop()