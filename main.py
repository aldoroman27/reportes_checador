#Importamos nuestra librería de pandas para poder manipular los datos tanto de csv como de xlxs
import pandas as pd
from datetime import time, datetime, timedelta

df = pd.read_csv('./reporte_todos.csv', skip_blank_lines=True, header=None) #Abrimos nuestro archivo csv para comenzar con la manipulación

print(df)
#df.columns = ["idEmpleado", "Empleado","Fecha", "Hora", "Vacia", "Tipo", "Dispositivo"] #Renombramos las oclumnas de nuestro csv

df.columns = ["Vacia1", "idEmpleado", "Empleado", "Fecha", "Vacia2", "Vacia3", "Normal"]

# 3. Limpiar espacios y convertir columna de fecha
df["Fecha"] = df["Fecha"].astype(str).str.strip()
df["FechaHora"] = pd.to_datetime(df["Fecha"], errors="coerce")

# 4. Separar en columnas de fecha y hora
df["Fecha"] = df["FechaHora"].dt.date.astype(str)
df["Hora"] = df["FechaHora"].dt.time.astype(str)

# 5. Eliminar columnas innecesarias
df = df.drop(columns=["Vacia1", "Vacia2", "Vacia3", "Normal", "FechaHora"])

# 6. Reordenar columnas
df = df[["idEmpleado", "Empleado", "Fecha", "Hora"]]

# 7. Mostrar para verificar
print(df.head())

#Creamos una función para clasificar por el tiempo el registro, es decir los registros del checador poniendo rangos de horas
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

    for _, row in grupo_ordenado.iterrows(): #Interactuamos hasta encontrar una ,
        fecha_hora = row["FechaHora"]
        if not isinstance(fecha_hora, datetime): #Si no es una fecha entonces pasamos a ejecutar el siguiente bloque de instrucciones
            continue
        hora = fecha_hora.time() #Definimos nuestra hora.
        
        #Definimos los rangos de entrada en este caso es de 7:20 - 9:30 am
        if time(7,30) <= hora <= time(9,30) and eventosRegistro["Entrada"] is None:
            eventosRegistro["Entrada"] = hora #Si entra dentro de este rango entonces lo clasificamos como Entrada
        #Definimos los rangos de comida, que empiezan desde las 12:00 - 15:10
        elif time(12,00) <= hora <= time(15,10) and eventosRegistro["SalidaComida"] is None:
            eventosRegistro["SalidaComida"] = hora
        #Definimos nestros rangos de salida de la comida, que puede ser desde las 13:45 - 15:55
        elif time(13,45) <= hora <= time(15,55) and eventosRegistro["RegresoComida"] is None:
            eventosRegistro["RegresoComida"] = hora
        elif hora >= time(17,0) and eventosRegistro["Salida"] is None:
            eventosRegistro["Salida"] = hora
        
    total_registros = len(grupo_ordenado)
    estatus = "COMPLETO" if all(eventosRegistro.values()) else "FALTANTE"

    return pd.Series({
        "Entrada" : eventosRegistro["Entrada"],
        "SalidaComida" : eventosRegistro["SalidaComida"],
        "RegresoComida" : eventosRegistro["RegresoComida"],
        "Salida" : eventosRegistro["Salida"],
        "Registros" : total_registros,
        "Estatus" : estatus
    })

df_dias = df.groupby(["idEmpleado", "Empleado", "Fecha"], group_keys=False).apply(clasificarRegistro).reset_index()


hora_tolerancia = time(8,11,0)

def calcular_tiempos(row):
    try:
        entrada = row["Entrada"]
        salida_comida = row["SalidaComida"]
        regreso_comida = row["RegresoComida"]
        salida = row["Salida"]

        #Si alguno de los valores es NONE retornamos los valores por defecto
        if None in [entrada, salida_comida, regreso_comida, salida]:
            return pd.Series({
                "Horas trabajadas":None,
                "Minutos Retardo":None
            })

        #Convertimos a DateTime
        base_date = datetime(2025, 1, 1)
        entrada_dt = datetime.combine(base_date, entrada)
        salida_dt = datetime.combine(base_date, salida)
        salida_comida_dt = datetime.combine(base_date, salida_comida)
        regreso_comida_dt = datetime.combine(base_date, regreso_comida)

        #Calculamos la jornada y el descanso
        jornada = salida_dt - entrada_dt
        descanso = regreso_comida_dt - salida_comida_dt
        horas_trabajadas = jornada - descanso

        #Calculo de los minutos de retardo
        if entrada > hora_tolerancia:
            tolerancia_dt = datetime.combine(base_date, hora_tolerancia)
            retardo = int((entrada_dt - tolerancia_dt).total_seconds() // 60)
        else:
            retardo = 0
        horas_str = str(horas_trabajadas).split(" ")[-1][:5]  #Mostramos las horas trabajadas en un formato correcto Ej: '09:12'
        return pd.Series({
            "HorasTrabajadas":horas_str, #Asignamos los valores que sacamos
            "MinutosRetardo":retardo #Asignamos el valor que sacamos
        })
    except Exception as e:
        print("Error en la fila: ")
        print(row)
        print("Expeción: ", e)
        return pd.Series([None, None], index=["HorasTrabajadas", "MinutosRetardo"])

resultados = df_dias.apply(calcular_tiempos, axis=1)


df_dias = pd.concat([df_dias, resultados], axis=1)

#Verificamos la información que sea correcta imprimiendo los datos.
print(df_dias[["idEmpleado","Empleado","Fecha", "Entrada","SalidaComida","RegresoComida", "Salida" ,"HorasTrabajadas", "MinutosRetardo", "Estatus"]].head())


#df_dias.to_excel("reporte_final_todos.xlsx", index=False)#Guardamos nuestro archivo en un archivo .xlsx

