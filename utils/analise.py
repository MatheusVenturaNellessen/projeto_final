import pandas as pd

df_anac = pd.read_csv('database/csv_anac_resumo_anual_2025.csv', sep=';', encoding='latin1')

print(df_anac.info())

df_anac['HORAS VOADAS'] = df_anac['HORAS VOADAS'].str.replace(',', '.', regex=False)
df_anac['HORAS VOADAS'] = pd.to_numeric(df_anac['HORAS VOADAS'], errors='coerce')
df_anac['ANO'] = pd.to_datetime(df_anac['ANO'], errors='coerce')
df_anac['MÊS'] = pd.to_datetime(df_anac['MÊS'], errors='coerce')

# print('Quantidade de valores nulos em cada Serie/coluna:\n')
# print(df_anac.isna().sum())
# print('-------------------------------------------------')

# print('Percentual de valores nulos por Serie/coluna:\n')
# print(df_anac.isna().mean() * 100)
# print('-------------------------------------------------')

df_anac = df_anac.dropna() # exclui registros que contém valores nulos e/ou NaN do DataFrame

print(df_anac.info())