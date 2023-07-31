import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("afa_2015_2022_spa.csv")

df['fecha'] = pd.to_datetime(df['fecha'])

# Agrupar los datos por el nombre del torneo
grupo_torneo = df.groupby('torneo')

print("Sector Amarillas")
# Calcular el total de tarjetas amarillas de local para cada torneo
total_amarillas_local_por_torneo = grupo_torneo['amarillas_local'].mean()

# Calcular el total de tarjetas amarillas de visitante para cada torneo
total_amarillas_visitante_por_torneo = grupo_torneo['amarillas_visitante'].mean()

# Combinar los resultados en un nuevo DataFrame
resultados_por_torneo = pd.DataFrame({
    'tarjetas_amarillas_local': total_amarillas_local_por_torneo,
    'tarjetas_amarillas_visitante': total_amarillas_visitante_por_torneo
})

print(resultados_por_torneo)

# Definir una función de agregación personalizada para calcular el promedio total de amarillas por partido
def promedio_total_amarillas_por_partido(group):
    total_amarillas=(group['amarillas_local'].sum() + group['amarillas_visitante'].sum())
    return pd.Series({'promedio_amarillas_totales': total_amarillas / len(group)})

# Agrupar los datos por el nombre del torneo y aplicar la función de agregación personalizada
promedio_total_amarillas = df.groupby('torneo').apply(promedio_total_amarillas_por_partido).reset_index()
print(promedio_total_amarillas)
# Definir el orden personalizado de los campeonatos (por ejemplo, en función de su importancia o relevancia)
orden_personalizado_campeonatos = ['Campeonato 2015', 'Transicion 2016', 'Campeonato 2016/17', 'Campeonato 2017/18', 'Campeonato 2018/19', 'Superliga 2019/20','Campeonato 2021', 'Campeonato 2022']

# Ordenar el DataFrame según el orden personalizado de los campeonatos
promedio_total_amarillas['torneo'] = pd.Categorical(promedio_total_amarillas['torneo'], categories=orden_personalizado_campeonatos, ordered=True)

promedio_total_amarillas.sort_values(by='torneo', inplace=True)

# Crear el gráfico de líneas
plt.figure(figsize=(10, 6))
plt.plot(promedio_total_amarillas['torneo'], promedio_total_amarillas['promedio_amarillas_totales'], marker='o', linestyle='-', color='r')
plt.xlabel('Torneo')
plt.ylabel('Promedio de Amarillas totales por partido')
plt.title('Promedio de Amarillas totales por campeonato (orden personalizado)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

print("Sector Rojas")
# Calcular el total de tarjetas rojas de local para cada torneo
total_rojas_local_por_torneo = grupo_torneo['rojas_local'].mean()

# Calcular el total de tarjetas amarillas de visitante para cada torneo
total_rojas_visitante_por_torneo = grupo_torneo['rojas_visitante'].mean()

# Combinar los resultados en un nuevo DataFrame
resultados_por_torneoR = pd.DataFrame({
    'tarjetas_rojas_local': total_rojas_local_por_torneo,
    'tarjetas_rojas_visitante': total_rojas_visitante_por_torneo
})

print(resultados_por_torneoR)

# Definir una función de agregación personalizada para calcular el promedio total de rojas por partido
def promedio_total_rojas_por_partido(group):
    total_rojas=(group['rojas_local'].sum() + group['rojas_visitante'].sum())
    return pd.Series({'promedio_rojas_totales': total_rojas / len(group)})

# Agrupar los datos por el nombre del torneo y aplicar la función de agregación personalizada
promedio_total_rojas = df.groupby('torneo').apply(promedio_total_rojas_por_partido).reset_index()
print(promedio_total_rojas)
# Definir el orden personalizado de los campeonatos (por ejemplo, en función de su importancia o relevancia)
orden_personalizado_campeonatos = ['Campeonato 2015', 'Transicion 2016', 'Campeonato 2016/17', 'Campeonato 2017/18', 'Campeonato 2018/19', 'Superliga 2019/20','Campeonato 2021', 'Campeonato 2022']

# Ordenar el DataFrame según el orden personalizado de los campeonatos
promedio_total_rojas['torneo'] = pd.Categorical(promedio_total_rojas['torneo'], categories=orden_personalizado_campeonatos, ordered=True)

promedio_total_rojas.sort_values(by='torneo', inplace=True)

# Crear el gráfico de líneas
plt.figure(figsize=(10, 6))
plt.plot(promedio_total_rojas['torneo'], promedio_total_rojas['promedio_rojas_totales'], marker='o', linestyle='-', color='r')
plt.xlabel('Torneo')
plt.ylabel('Promedio de Rojas totales por partido')
plt.title('Promedio de Rojas totales por campeonato (orden personalizado)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Agrupar los datos por el nombre del torneo y contar la cantidad de partidas en cada grupo
cantidad_partidas_por_torneo = df.groupby('torneo').size().reset_index(name='cantidad_partidas')

print(cantidad_partidas_por_torneo)

# Ordenar el DataFrame original 'df' cronológicamente por la columna 'fecha'
df.sort_values(by='fecha', inplace=True)

# Definir una función de agregación personalizada para calcular el promedio de goles totales por partido
def promedio_goles_totales_por_partido(group):
    total_goles = group['goles_local'].sum() + group['goles_visitante'].sum()
    return pd.Series({'promedio_goles_totales': total_goles / len(group)})

# Agrupar los datos por el nombre del torneo y aplicar la función de agregación personalizada
total_goles = df.groupby('torneo').apply(promedio_goles_totales_por_partido).reset_index()

# Ordenar el DataFrame 'total_goles' según el orden personalizado de los campeonatos
total_goles['torneo'] = pd.Categorical(total_goles['torneo'], categories=orden_personalizado_campeonatos, ordered=True)
total_goles.sort_values(by='torneo', inplace=True)

# Crear el gráfico de líneas
plt.figure(figsize=(10, 6))
plt.plot(total_goles['torneo'], total_goles['promedio_goles_totales'], marker='o', linestyle='-', color='r')
plt.xlabel('Torneo')
plt.ylabel('Promedio de goles totales por partido')
plt.title('Promedio de goles totales por campeonato (orden personalizado)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



