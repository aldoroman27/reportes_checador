import tk as Tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import time, datetime, timedelta, date

#Comezamos definiendo los verdaderos horarios bases de nuestros trabajadores.
horarios_base = {
    "normal":{"entrada": time(8,0),"salida":time(18,00)}, #Horario normal de 08:00 - 18:00
    "becario_it":{"entrada":time(9,0),"salida":time(15,00)}, #Horario de becario TI 09:00 - 15:007
    "becario_calidad":{"entrada":time(8,0), "salida":time(14,00)}, #Horario del becario de calidad 08:00 - 14:00
    "becaria_compras":{"entrada":time(8,0), "salida":time(17,00)}, #Horario de la becaria de compras 08:00 - 17:00
    "becario_CONALEP":{"entrada":time(8,0),"salida":time(16,00)}, #Horario de becarios CONALEP 08:00 - 16:00
    "matutino":{"entrada":time(6,00),"salida":time(15,00)}, # Horario matutino (maquinados) 06:00 - 15:00
    "vespertino":{"entrada":time(15,00),"salida":time(23,00)} # Horario vespertino (maquinados) 15:00 - 23:00
}

#Definimos los rangos de los turnos por horario
rangos_turno = {
    "normal":{ #Horario normal
        "entrada":(time(6,10), time(10,15)),#Definimos un rango de entrada desde las 06:10 - 10:15 (máximo)
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
        "entrada":(time(8,00), time(9,00)),
        "salida_comida":(time(15,00),time(16,00)),
        "regreso_comida":(time(15,30), time(16,30))
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
    }
}

fecha_inicio_nuevos_horarios = date(2025,8,6) #Es decir que en 06/08/2025 iniciamos a contar los nuevos horarios

#Definimos a los empleados con turnos "Especiales"
empleados_turnos = {
    17: "becario_it", #Becario de Ti
    11: "vespertino", #Maquinados vespertino
    29: "matutino", #Maquinados matutino
    33: "matutino", #Maquinados matutino
    35: "vespertino", #Maquinados vespertino
    36: "becario_CONALEP",#Becario de Conalep IVAN
    7: "becario_CONALEP" #Becario de Conalep Luis Barragán
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
        "Salida" : None,
        "Turno" : None
    }

    #Tomamos el id del empleado actual
    id_empleado = grupo_ordenado["idEmpleado"].iloc[0]
    #Fecha en la que se hace el registro
    fecha_registro = grupo_ordenado["FechaHora"].dt.date.min()
    #Definimos entonces el horario.
    turno = empleados_turnos.get(id_empleado, "normal")
    """"
    Esta es una verificación temporal, si el empleado tiene vespertino o matutino y la fecha del registro es menor a 06/08/2025
    entonces se le asginará autamitacmente el horario de normal.
    """
    if turno in ["vespertino", "matutino"] and fecha_registro < fecha_inicio_nuevos_horarios:
        turno = "normal"

    #Definimos los horarios de entrada y salida de los trabajadores en común.
    hora_entrada = horarios_base[turno]["entrada"]
    hora_salida = horarios_base[turno]["salida"]

    #Verificar esta parte.
    """
    if id_empleado == 4 and fecha_registro.weekday() == 2:
        hora_salida = time(14,00)
        rangos_turno["becaria_compras"]["salida_comida"] == (time(12,00))
        rango_vuelta_comida["becaria_compras"] == (time())
    """

    #Definimos la salida mínima de los empleados
    salida_minima = (datetime.combine(datetime.today(),hora_salida) - timedelta(minutes=30)).time()
    #Definimos los rangos de entrada
    rango_ent = rangos_turno[turno]["entrada"]
    #Definimos los rangos de salida a comer
    rango_sal_comida = rangos_turno[turno]["salida_comida"]
    #Definimos los rangos de regreso de comida.
    rango_reg_comida = rangos_turno[turno]["regreso_comida"]

    #Comenzamos a iterar en nuestro dataframe
    for idx,row in grupo_ordenado.iterrows():
        #Obtenemos la fecha y hora del registro
        fecha_hora = row["FechaHora"]
        is_last = idx == len(grupo_ordenado)-1
        #Si no es una datetime nuestra fecha_hora
        if not isinstance(fecha_hora, datetime):
            continue
        #Definimos la hora usando .time en nuestra variable fecha_hora
        hora = fecha_hora.time()
        """
        Definimos los rangos de entradas dependiendo de cada uno de los empleados.
        """
        #Si el primer registro que se detecta encaja dentro de los rangos y la entrada es definida como None entonces:
        if rango_ent[0] <= hora <= rango_ent[1] and eventosRegistro["Entrada"] is None:
            eventosRegistro["Entrada"] = hora #Se asigna ese registro de hora como la Entrada
        #Si el segundo registro que se detecta encaja dentro de los rangos y la SalidaComida está como None entonces:
        elif rango_sal_comida[0] <= hora <= rango_sal_comida[1] and eventosRegistro["SalidaComida"] is None:
            eventosRegistro["SalidaComida"] = hora #Asignamos la hora de ese registro a nuestra SalidaComida
        #Si el tercer registro que se detecta encaja dentro de los rangos y RegresoComida está como None entonces:
        elif rango_reg_comida[0] <= hora <= rango_reg_comida[1] and eventosRegistro["RegresoComida"] is None:
            eventosRegistro["RegresoComida"] = hora #Asignamos entonces la hora de ese registro a nuestro RegresoComida
        #Si el último registro es None entonces
        elif eventosRegistro["Salida"] is None:
            #Verificamos que sea el último y que además la hora sea mayor o igual a la salida mínima que tenemos
            if is_last and hora >= salida_minima:
                eventosRegistro["Salida"] = hora #Asignamos entonces el registro como nuestra Salida        

    #Hacemos un conteo de los registros por día
    total_registros = len(grupo_ordenado)
    #Si se tiene más de 4 registros es considerado como completo, en caso de tener menos de 4 se considera como FALTANTE de registro
    estatus = "COMPLETO" if total_registros >= 4 else "FALTANTE"

    #Hacemos el cálculo de las horas trabajadas
    horas_trabajadas = "-"
    if eventosRegistro["Entrada"] and eventosRegistro["Salida"]:
        entrada_dt = datetime.combine(datetime.today(), eventosRegistro["Entrada"])
        salida_dt = datetime.combine(datetime.today(), eventosRegistro["Salida"])
        if salida_dt > entrada_dt:
            delta = salida_dt - entrada_dt
            horas_trabajadas = str(delta)

    #Hacemos el cáulculo del retardo.
    tolerancia = (datetime.combine(datetime.today(), hora_entrada)+timedelta(minutes=0)).time()
    retraso = "-"
    if eventosRegistro["Entrada"] and eventosRegistro["Entrada"] > tolerancia:
        entrada_real = datetime.combine(datetime.today(), eventosRegistro["Entrada"])
        tarde_dt = datetime.combine(datetime.today(), tolerancia)
        retraso = str(entrada_real - tarde_dt)

    #Retornamos una serie de pandas con la información que recogimos.
    return pd.Series({
        "Entrada" : eventosRegistro["Entrada"],#Asignamos la hora de de entrada
        "SalidaComida" : eventosRegistro["SalidaComida"],#Asignamos la hora de salida a comer
        "RegresoComida" : eventosRegistro["RegresoComida"],#Asignamos la hora de regreso de comida
        "Salida" : eventosRegistro["Salida"],#Asignamos la hora de salida
        "Registros" : total_registros,#Asignamos el conteo total de registros que se tuvieron
        "Estatus" : estatus,#Asignamos si el estatus fue completo o faltante
        "HorariosEntradaEsperados": hora_entrada,#Definimos los horarios esperados
        "HorarioSalidaEsperado":hora_salida,#Hora de salida esperada (varía entre becario-trabajador)
        "HorasTrabajadas": horas_trabajadas,#Un conteo de horas trabajadas
        "Retraso" : retraso #El conteo de minutos después de que pasara la hora de entrada

    })

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
        if df is None:#Si el dataframe está vacío entonces mostramos un mensaje de error
            messagebox.showerror("Error", "Primero debes importar un archivo.")
            return
        try:#En caso contrario hacemos un bloque de instrucciones try
            
            df["FechaHora"] = pd.to_datetime(df["Fecha"]+ " "+df["Hora"],errors="coerce")
            resumen = df.groupby(["idEmpleado", "Empleado", "Fecha"]).apply(clasificarRegistro).reset_index()

            #Creamos un dataframe con el resumen generado
            self.df_resumen = resumen

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
                    fila[idx_estatus] = "✅ COMPLETO"
                else:
                    fila[idx_estatus] = "❌ FALTANTE"
                self.tree.insert("", "end", values=fila)
        except Exception as e:#Hacemos el manejo del error y se lo mostramos al usuario
            messagebox.showerror("Error", str(e))
    
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
