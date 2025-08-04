import tk as Tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import time, datetime, timedelta

#Definimos los horarios de los becarios para que se ajuste a los horarios correctamente el analisis.
becarios = {
    17:{"entrada":time(9,0), "salidaComida":time(12,0), "regresoComida":time(12,50),"salida":time(15,0) }, #Aldo
    36:{"entrada":time(8,0), "salidaComida":time(14,15), "regresoComida":time(15,10),"salida":time(16,0) },# Ivan
    7:{"entrada":time(8,0), "salidaComida":time(14,15), "regresoComida":time(15,10),"salida":time(16,0)}, #Luis Barragán
}

#Definimos nuestra función para poder clasificar los registros de nuestros usuarios
def clasificarRegistro(grupo):
    grupo["FechaHora"] = pd.to_datetime(grupo["Fecha"]+ " "+ grupo["Hora"], errors='coerce') #Hacemos la concatenación de la información
    grupo_ordenado = grupo.sort_values("FechaHora").reset_index(drop=True) #Ordenamos los valores.
    #Creamos un diccionario con los posibles eventos que pueden surgir.
    eventosRegistro = {
        "Entrada" : None, #Asignamos los valores a nuestras varibales del diccionario como None
        "SalidaComida" : None,
        "RegresoComida" : None,
        "Salida" : None
    }

    #Definimos los horarios de entrada y salida de los trabajadores en común
    hora_entrada = time(8,0)
    hora_salida = time(18,0)
    
    #Ubicamos el id de cada usuario
    id_empleado = grupo_ordenado["idEmpleado"].iloc[0]
    #Si el id del empleado coincide con el de los establecidos de los becarios entonces
    if id_empleado in becarios:
        #Definimos su hora de entrada indicada en nuestro diccionario
        hora_entrada = becarios[id_empleado]["entrada"]
        #Definimos su hora de salida indicada en nuestro diccionario
        hora_salida = becarios[id_empleado]["salida"]
    #Definimos la salida mínima
    salida_minima = (datetime.combine(datetime.today(),hora_salida) - pd.Timedelta(minutes=30)).time()
    #Antes _ donde dice idx
    for idx, row in grupo_ordenado.iterrows(): #Interactuamos hasta encontrar una ,
        fecha_hora = row["FechaHora"]
        is_last = idx == len(grupo_ordenado)-1
        if not isinstance(fecha_hora, datetime): #Si no es una fecha entonces pasamos a ejecutar el siguiente bloque de instrucciones
            continue
        hora = fecha_hora.time() #Definimos nuestra hora.
        
        #Definimos los rangos de entrada en este caso es de 7:20 - 9:30 am
        if time(6,10) <= hora <= time(9,30) and eventosRegistro["Entrada"] is None:
            eventosRegistro["Entrada"] = hora #Si entra dentro de este rango entonces lo clasificamos como Entrada
        #Definimos los rangos de comida, que empiezan desde las 12:00 - 15:10
        elif time(12,00) <= hora <= time(16,15) and eventosRegistro["SalidaComida"] is None:
            eventosRegistro["SalidaComida"] = hora
        #Definimos nestros rangos de salida de la comida, que puede ser desde las 13:45 - 15:55
        elif time(13,00) <= hora <= time(16,45) and eventosRegistro["RegresoComida"] is None:
            eventosRegistro["RegresoComida"] = hora
        elif eventosRegistro["Salida"] is None:
            if is_last and hora >= salida_minima:
                eventosRegistro["Salida"] = hora
    
    #Hacemos un conteo de los registros por día
    total_registros = len(grupo_ordenado)
    #Si se tiene más de 4 registros es considerado como completo, en caso de tener menos de 4 se considera como FALTANTE de registro
    estatus = "COMPLETO" if all(eventosRegistro.values()) else "FALTANTE"

    #Hacemos el cálculo de las horas trabajadas
    horas_trabajadas = "-"
    if eventosRegistro["Entrada"] and eventosRegistro["Salida"]:
        entrada_dt = datetime.combine(datetime.today(), eventosRegistro["Entrada"])
        salida_dt = datetime.combine(datetime.today(), eventosRegistro["Salida"])
        if salida_dt > entrada_dt:
            delta = salida_dt - entrada_dt
            horas_trabajadas = str(delta)

    #Hacemos el cáulculo del retardo.
    tolerancia = (datetime.combine(datetime.today(), hora_entrada)+timedelta(minutes=1)).time()
    retraso = "-"
    if eventosRegistro["Entrada"] and eventosRegistro["Entrada"] > tolerancia:
        entrada_real = datetime.combine(datetime.today(), eventosRegistro["Entrada"])
        tarde_dt = datetime.combine(datetime.today(), tolerancia)
        retraso = str(entrada_real - tarde_dt)

    return pd.Series({
        "Entrada" : eventosRegistro["Entrada"],
        "SalidaComida" : eventosRegistro["SalidaComida"],
        "RegresoComida" : eventosRegistro["RegresoComida"],
        "Salida" : eventosRegistro["Salida"],
        "Registros" : total_registros,
        "Estatus" : estatus,
        "HorariosEntradaEsperados": hora_entrada,
        "HorarioSalidaEsperado":hora_salida,
        "HorasTrabajadas": horas_trabajadas,
        "Retraso" : retraso

    })

#Creamos una clase para mostrar el modulo de resumen
class ModuloResumen:
    def __init__(self, notebook, get_dataframe_func):
        self.get_dataframe = get_dataframe_func
        self.tab_resumen = ttk.Frame(notebook)
        notebook.add(self.tab_resumen, text="Visualizar Resumen")

        btn_generar = ttk.Button(self.tab_resumen, text="Generar resumen", command=self.generar_resumen)
        btn_generar.pack(pady=10)

        btn_exportar_xlsx = ttk.Button(self.tab_resumen, text="Exportar como excel", command=self.exportar_excel)
        btn_exportar_xlsx.pack(pady=5)

        self.frame_tabla = ttk.Frame(self.tab_resumen)
        self.frame_tabla.pack(fill="both", expand=True)

        self.tree = ttk.Frame(self.tab_resumen)
        self.frame_tabla.pack(fil="both", expand=True)

        self.tree = ttk.Treeview(self.frame_tabla, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def generar_resumen(self):
        df = self.get_dataframe()
        if df is None:
            messagebox.showerror("Error", "Primero debes importar un archivo.")
            return
        try:

            df["FechaHora"] = pd.to_datetime(df["Fecha"]+ " "+df["Hora"],errors="coerce")
            resumen = df.groupby(["idEmpleado", "Empleado", "Fecha"]).apply(clasificarRegistro).reset_index()

            self.df_resumen = resumen

            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(resumen.columns)

            for col in resumen.columns:
                self.tree.heading(col, text=str(col))
                self.tree.column(col, width=100)
            for _, row in resumen.iterrows():
                fila = list(row)
                idx_estatus = resumen.columns.get_loc("Estatus")
                if fila[idx_estatus] == "COMPLETO":
                    fila[idx_estatus] = "✅ COMPLETO"
                else:
                    fila[idx_estatus] = "❌ FALTANTE"
                self.tree.insert("", "end", values=fila)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    

    def get_resumen_df(self):
        return getattr(self, "resumen_df", None)


    def exportar_excel(self):
        try:
            if not hasattr(self, "df_resumen"):
                messagebox.showerror("Error", "Primero genera el resumen antes de exportar.")
                return

            # Diálogo para elegir ruta y nombre
            ruta_archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Guardar archivo como"
            )
            if not ruta_archivo:
                return

            # Guardamos el archivo
            self.df_resumen.to_excel(ruta_archivo, index=False)
            messagebox.showinfo("Éxito", f"Archivo guardado correctamente:\n{ruta_archivo}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
