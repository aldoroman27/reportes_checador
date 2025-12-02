#Se debe de hacer el pip install tk
import tk as Tk
from tkinter import ttk, messagebox, filedialog
#Se debe de hacer el pip install pandas
import pandas as pd
from datetime import time, datetime, timedelta, date

#Comezamos definiendo los verdaderos horarios bases de nuestros trabajadores.
horarios_base = {
    "normal":{"entrada": time(8,0),"salida":time(18,00)}, #Horario normal de 08:00 - 18:00
    "becario_it":{"entrada":time(9,0),"salida":time(15,00)}, #Horario de becario TI 09:00 - 15:007
    "becario_calidad":{"entrada":time(8,0), "salida":time(14,00)}, #Horario del becario de calidad 08:00 - 14:00
    "becaria_compras":{"entrada":time(8,0), "salida":time(14,00)}, #Horario de la becaria de compras 08:00 - 17:00
    "becario_CONALEP":{"entrada":time(8,0),"salida":time(16,00)}, #Horario de becarios CONALEP 08:00 - 16:00
    "nocturno":{"entrada":time(23,00), "salida":time(6,00)}, #Horario de salida para el turno nocturno
    "matutino":{"entrada":time(6,00),"salida":time(15,00)}, # Horario matutino (maquinados) 06:00 - 15:00
    "horarioRicardo":{"entrada":time(7,00), "salida":time(23,00)}, #Horario de Ricardo que puede ser que llegue desde las 7 y salir hasta las 23
    "vespertino":{"entrada":time(15,00),"salida":time(23,00)}, # Horario vespertino (maquinados) 15:00 - 23:00
    "sabado":{"entrada":time(9,00), "salida":time(14,00)}#Horarios de sábado (just in case)
}

#Definimos los rangos de los turnos por horario
rangos_turno = {
    "normal":{ #Horario normal
        "entrada":(time(6,00), time(10,15)),#Definimos un rango de entrada desde las 06:10 - 10:15 (máximo)
        "salida_comida":(time(12,00), time(16,15)),#Definimos un rango de salida de comida 12:00 - 16:15 (máximo)
        "regreso_comida":(time(13,00), time(16,45)),#Definimos un rango de regreso de comida 13:00 - 16:45 (máximo)
    },
    "becario_it":{ #Definimos el horario del becario de TI
        "entrada":(time(8,00), time(9,45)),#Definimos un rango de entrada desde las 08-00 - 09:45 (máximo)
        "salida_comida":(time(12,00), time(12,45)),#Definimos un rango de salida a comer 12:00 - 12:45 (máximo)
        "regreso_comida":(time(12,30), time(13,10))#Definimos un rango de regreso de comida 12:30 - 13:10 (máximo)
    },
    "becario_CONALEP":{ #Definimos el rango de horarios de los becarios del CONALEP
        "entrada":(time(7,00), time(8,45)),#Definimos el rango de entrada desde las 07:00 - 08:45 (máximo)
        "salida_comida":(time(14,00), time(14,30)),#Definimos el rango de salida a comer 14:00 - 14:30 (máximo)
        "regreso_comida":(time(14,45), time(15,15))#Definimos el rango de regreso de comida 14:45 - 15:15 (máximo)
    },
    "becario_calidad":{
        "entrada":(time(7,00), time(9,00)),
        "salida_comida":(time(11,00), time(12,00)),
        "regreso_comida":(time(11,30), time(12,00))
    },
    "becaria_compras":{
        "entrada":(time(7,00), time(9,20)),
        "salida_comida":(time(15,00),time(16,00)),
        "regreso_comida":(time(15,30), time(16,30)),
    },
    "matutino":{ #Definimos el rango de horarios de maquinados matutino
        "entrada":(time(5,00), time(7,00)),#Definimos el rango de entrada desde las 05:00 - 07:00 (máximo)
        "salida_comida":(time(11,30), time(12,45)),#Definimos el rango de salida a comer 11:30 - 12:45 (máximo)
        "regreso_comida":(time(12,30), time(13,20))#DEfinimos el rango de regreso a comer 12:30 - 13:20 (máximo)
    },
    "vespertino":{#Definimos los rangos de horarios de maquinados vespertino
        "entrada":(time(14,00), time(16,00)),#Definimos el rango de entrada 14:00 - 16:00 (máximo)
        "salida_comida":(time(18,00), time(19,45)),#Definimos el rango de salida a comer 18:00 - 19:45 (máximo)
        "regreso_comida":(time(18,45), time(20,20))#Definimos el rango de regreso de comida 18:45 - 20:20 (máximo)
    },
    "sabado":{#Definimos los rangos de horarios para el turno sabatino
        "entrada":(time(6,00), time(9,00)), #Definimos el rango de entrada desde las 06:00 - 09:00 (máximo)
        "salida_comida":(time(11,00), time(11,45)), #Definimos el rango de salida para la comida 11:00 - 11:45 (máximo)
        "regreso_comida":(time(11,45), time(12,30)) #Definimos el rango de la salida de regreso de comida 11:45 - 12:30 (máximo)
    },
    "horarioRicardo":{ #Definimos un rango de entrada para ricardo que es algo rotativo (de momento inactivo ya que se encuentra en el turno nocturno)
        "entrada":(time(7,00), time(15,00)),
        "salida_comida":(time(17,00), time(17,50)),
        "regreso_comida":(time(17,45),time(18,48))
    },
    "nocturno":{
        "entrada":(time(22,00), time(00,00)),
        "salida_comida":(time(3,00),time(5,00)),
        "regreso_comida":(time(3,45),time(5,45))
    }
}
"""
    Esta es la parte de posibles modificaciones que se pueden hacer a las fechas o rangos, ya sabrán ustedes.
"""
fecha_inicio_nuevos_horarios = date(2025,8,6) #Es decir que en 06/08/2025 iniciamos a contar los nuevos horarios.
sabado_erick = date(2025,8,9)


#Definimos a los empleados con turnos "Especiales"
empleados_turnos = {
    "015": "becario_it", #Becario de Ti
    "01078":"vespertino",
    "01032": "horarioRicardo", #Maquinados vespertino
    "01042": "matutino", #Maquinados matutino
    "01087": "nocturno", #Royer turno nocturno
    "014": "becario_CONALEP",#Becario de Conalep IVAN
    "016": "becaria_compras", #Becaria de compras
    "013": "becario_CONALEP", #Becario de Conalep Luis Barragán
    "017": "becario_calidad" #Becario de calidad
}

#Definimos nuestra función para poder clasificar los registros de nuestros usuarios
def clasificarRegistro(grupo):
     # Combina Fecha y Hora, los errores se convierten en NaT (Not a Time)
    grupo["FechaHora"] = pd.to_datetime(grupo["Fecha"]+ " "+ grupo["Hora"], errors='coerce')
    grupo_ordenado = grupo.sort_values("FechaHora").reset_index(drop=True)

    # --- INICIA BLOQUE CORREGIDO Y MEJORADO ---
    # Verifica si el grupo no tiene registros válidos
    if grupo_ordenado["FechaHora"].isna().all():
        fecha_actual = pd.to_datetime(grupo_ordenado["Fecha"].iloc[0]).date()
        print("Entré a la comparación")
        estatus_dia = "FALTA" if fecha_actual.weekday() < 5 else "FIN DE SEMANA" # 5 es Sábado, 6 es Domingo
        print("Hago la comparación con fin de semana")
        if estatus_dia == "FIN DE SEMANA":
            # Diccionario para fines de semana
            return pd.Series({
                "Entrada": "FIN DE SEMANA",
                "Inicio Descanso": "FIN DE SEMANA", # CORREGIDO
                "Regreso Descanso": "FIN DE SEMANA",
                "Salida": "FIN DE SEMANA",
                "Registros": 0,
                "Estatus": estatus_dia, # Estatus mejorado
                "HorariosEntradaEsperados": "FIN DE SEMANA",
                "HorarioSalidaEsperado": "FIN DE SEMANA", # CORREGIDO
                "HorasTrabajadas": "-",
                "Retraso": "-"
            })
       #Si el status del día es Falta (no cuenta con registros y no es en fin de semana) 
        elif estatus_dia == "FALTA":
            #Retornamos un diccionario que tenga el status de Falta
            return pd.Series({
                "Entrada": "FALTA",
                "Inicio Descanso": "FALTA",
                "Regreso Descanso": "FALTA",
                "Salida": "FALTA",
                "Registros": 0,
                "Estatus": estatus_dia,
                "HorariosEntradaEsperados": "-",
                "HorarioSalidaEsperado": "-",
                "HorasTrabajadas": None,
                "Retraso": "-"
            })
    #Eventos de registro los manetemos como None
    eventosRegistro = {
        "Entrada" : None,
        "SalidaComida" : None,
        "RegresoComida" : None,
        "Salida" : None,
        "Turno" : None
    }

    id_empleado = str(grupo_ordenado["idEmpleado"].iloc[0]) # Convertimos a str
    turno = empleados_turnos.get(id_empleado, "normal")


    hora_entrada = horarios_base[turno]["entrada"]
    hora_salida = horarios_base[turno]["salida"]
    
    salida_minima = (datetime.combine(date.today(), hora_salida) - timedelta(minutes=30)).time()
    rango_ent = rangos_turno[turno]["entrada"]
    rango_sal_comida = rangos_turno[turno]["salida_comida"]
    rango_reg_comida = rangos_turno[turno]["regreso_comida"]
    
    for idx, row in grupo_ordenado.iterrows():
        fecha_hora = row["FechaHora"]
        if pd.isna(fecha_hora) : continue
        
        hora = fecha_hora.time()
        is_last = (grupo_ordenado["FechaHora"].notna()).sum() -1 == idx

        if rango_ent[0] <= hora <= rango_ent[1] and eventosRegistro["Entrada"] is None:
            eventosRegistro["Entrada"] = hora
        elif rango_sal_comida[0] <= hora <= rango_sal_comida[1] and eventosRegistro["SalidaComida"] is None:
            eventosRegistro["SalidaComida"] = hora
        elif rango_reg_comida[0] <= hora <= rango_reg_comida[1] and eventosRegistro["RegresoComida"] is None:
            eventosRegistro["RegresoComida"] = hora
        elif eventosRegistro["Salida"] is None and hora >= salida_minima:
             # Se asigna como salida al último registro que cumpla la condición
             eventosRegistro["Salida"] = hora

    total_registros = (grupo_ordenado["FechaHora"].notna()).sum()
    estatus = "✅ COMPLETO" if total_registros >= 4 else "❌ FALTANTE"
    
    horas_trabajadas = "-"
    if eventosRegistro["Entrada"] and eventosRegistro["Salida"]:
        entrada_dt = datetime.combine(date.today(), eventosRegistro["Entrada"])
        salida_dt = datetime.combine(date.today(), eventosRegistro["Salida"])
        if salida_dt > entrada_dt:
            delta = salida_dt - entrada_dt
            horas_trabajadas = str(delta)
    
    retraso = "-"
    if eventosRegistro["Entrada"]:
        tolerancia = (datetime.combine(date.today(), hora_entrada)).time()
        if eventosRegistro["Entrada"] > tolerancia:
            entrada_real = datetime.combine(date.today(), eventosRegistro["Entrada"])
            tarde_dt = datetime.combine(date.today(), tolerancia)
            retraso = str(entrada_real - tarde_dt)

    # Diccionario para días normales
    return pd.Series({
        "Entrada" : eventosRegistro["Entrada"],
        "Inicio Descanso" : eventosRegistro["SalidaComida"],
        "Regreso Descanso" : eventosRegistro["RegresoComida"],
        "Salida" : eventosRegistro["Salida"],
        "Registros" : total_registros,
        "Estatus" : estatus,
        "HorariosEntradaEsperados": hora_entrada,
        "HorarioSalidaEsperado": hora_salida,
        "HorasTrabajadas": horas_trabajadas,
        "Retraso" : retraso
    })

#---------------------------------------------------- Esta parte es la visual del programa ----------------------------------------------
#Creamos una clase para mostrar el modulo de resumen
class ModuloResumen:
    def __init__(self, notebook, get_dataframe_func):
        self.get_dataframe = get_dataframe_func
        self.tab_resumen = ttk.Frame(notebook)
        notebook.add(self.tab_resumen, text="Visualizar Resumen")

        #Creamos un botón para generar el resumen y llamamos al método generar_resumen
        btn_generar = ttk.Button(self.tab_resumen, text="Generar resumen", command=self.generar_resumen)
        btn_generar.pack(pady=10)
        #Generamos otro botón que será el asignado para exportar como excell
        btn_exportar_xlsx = ttk.Button(self.tab_resumen, text="Exportar como excel", command=self.exportar_excel)
        btn_exportar_xlsx.pack(pady=5)
        #Creamos un frame para encapsular el arbol donde veremos la información recopilada
        self.frame_tabla = ttk.Frame(self.tab_resumen)
        self.frame_tabla.pack(fill="both", expand=True)
        #Llamamos al arbol y lo asignamos dentro
        self.tree = ttk.Frame(self.tab_resumen)
        self.frame_tabla.pack(fil="both", expand=True)
        #Hacemos la representación de la tabla
        self.tree = ttk.Treeview(self.frame_tabla, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)
        #Definimos un scroll para visualizar todos los posibles datos que tenemos.
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
    #Definimos una función para generar el resumen
    def generar_resumen(self):
        df = self.get_dataframe()#Asignamos a una variable el dataframe generado anteriormente
        try:#En caso contrario hacemos un bloque de instrucciones try
            
            df["FechaHora"] = pd.to_datetime(df["Fecha"]+ " "+df["Hora"],errors="coerce")
            
            #====== Nuevo Bloque experimental ========================
            #====== Llenamos las fechas faltantes ====================
            fecha_minima = pd.to_datetime(df["Fecha"]).min()
            fecha_maxima = pd.to_datetime(df["Fecha"]).max()
            #=========================================================
            rango_fechas = pd.date_range(fecha_minima, fecha_maxima, freq="D").date.astype(str)
            print(rango_fechas)
            
            empleados = df["idEmpleado"].unique()
            fechas_completas = pd.MultiIndex.from_product(
                [empleados, rango_fechas], names=["idEmpleado", "Fecha"]
            )
            df_base = pd.DataFrame(index=fechas_completas).reset_index()
            #Posible fix a las fechas faltantes.
            #Creamos un diccionario que va a mapear cada idEmpleado con su respectivo nombre.
            mapa_nombres = df[['idEmpleado','Empleado']].drop_duplicates().set_index('idEmpleado')['Empleado']
            #Usamos ese mapa para añadir la columna de 'Empleado' a nuestro df.
            df_base['Empleado'] = df_base['idEmpleado'].map(mapa_nombres)
            df_completo = pd.merge(df_base, df.drop(columns=['Empleado']), on=["idEmpleado","Fecha"], how="left")
            #Encontramos la posible solución 
            print(df_completo.head(5))
            # Sacamos el rango de fechas de todo el dataset
            #Aquí ta el error
            resumen = (
                df_completo.groupby(["idEmpleado", "Empleado", "Fecha"])
                .apply(clasificarRegistro)
                .reset_index()
            )
            #Creamos un dataframe con el resumen generado
            self.df_resumen = resumen
            #print(self.df_resumen) #Descomentar para testing en caso de ser necesario

            #==============Mostramos el df en el treeview=============
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(resumen.columns)
            #Vamos llenando las columnas e insertando la información que encontremos
            for col in resumen.columns:
                self.tree.heading(col, text=str(col))
                self.tree.column(col, width=100)
            #Vamos llenando las filas e insertando la información que tenemos.
            for _, row in resumen.iterrows():
                fila = list(row)
                idx_estatus = resumen.columns.get_loc("Estatus")
                if fila[idx_estatus] == "COMPLETO":
                    fila[idx_estatus] = " COMPLETO"
                elif fila[idx_estatus] == "FALTANTE":
                    fila[idx_estatus] = "X FALTANTE"
                self.tree.insert("", "end", values=fila)
        except Exception as e:#Hacemos el manejo del error y se lo mostramos al usuario
            messagebox.showerror("Error", str(e))
            return
    
    #Esta función es la encargada de poder mostrar este resumen en otras ventanas, la llamamos dentro de buscar.py
    def get_resumen_df(self):
        return self.df_resumen if hasattr(self, "df_resumen") else None
    #Esta es la función encargada de poder exportar el df generado a un excell
    def exportar_excel(self):
        #Hacemos un bloque tolerante a fallas con try y except
        try:
            #Si no tenemos ningún csv, excell cargado entonces marcamos el error.
            if not hasattr(self, "df_resumen"):
                messagebox.showerror("Error", "Primero genera el resumen antes de exportar.")
                return

            # Diálogo para elegir ruta y nombre
            ruta_archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Guardar archivo como"
            )
            #Si no se toma una ruta entonces retornamos directamente
            if not ruta_archivo:
                return

            # Guardamos el archivo
            self.df_resumen.to_excel(ruta_archivo, index=False)
            #Mostramos un mensaje de que el archivo fue guardado correctamente.
            messagebox.showinfo("Éxito", f"Archivo guardado correctamente:\n{ruta_archivo}")
        #Manejamos el bloque de los posibles errores que se generen
        except Exception as e:
            #En caso de no poder guardar el archivo entonces mostramos el error correspondiente.
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
