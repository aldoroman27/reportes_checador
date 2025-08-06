import pandas as pd

df = pd.read_excel('./TransactionsReport.xlsx', skiprows=3)

# Filtrar solo las filas con fecha válida en 'Fecha/Hora'
df = df[df['Fecha/Hora'].apply(lambda x: pd.to_datetime(x, errors='coerce')).notnull()].copy()

# Eliminar columnas innecesarias
columnas_a_eliminar = ['Unnamed: 0', 'Unnamed: 4', 'Código de Trabajo', "Tipo de Registro"]
df.drop(columns=columnas_a_eliminar, inplace=True, errors='ignore')

df.columns = ["idEmpleado", "Empleado", "Fecha"]

# Resetear índice
df.reset_index(drop=True, inplace=True)

print(df)