import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

#Lectura del archivo.
df = pd.read_csv("afa_2015_2022_spa.csv")

#Funcion que devuelve un diccionario con los dias y la cantidad de partidos que hubo por cada uno.
from datetime import datetime

def queDiaJugo(lista):
    day = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'viernes', 'Sabado', 'Domingo']
    days = {'Lunes':0, 'Martes':0, 'Miercoles':0, 'Jueves':0, 'viernes':0, 'Sabado':0, 'Domingo':0}
    for x in lista:
        d = datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S")
        days[day[d.weekday()]] = days[day[d.weekday()]]+1    
    return days


### RIVER BOCA SOLO DOMINGOS
# Queriamos saber si efectivamente los Boca-River se jugaban todos los domingos.
def p0():
    
    # Comenzamos generando dataFrame que contuviera solo los partidos jugados entre boca y river.
    ByR = df[((df['equipo_local'] == 'River Plate') | (df['equipo_local'] == 'Boca Juniors')) & ((df['equipo_visitante'] == 'River Plate') | (df['equipo_visitante'] == 'Boca Juniors'))].sort_values('fecha_encuentro')
    
    # Luego generamos una serie con todas las fecha de encuentro que tuvieron.
    lista_fechas_ByR = ByR['fecha_encuentro']
    #print(lista_fechas_ByR)
    
    # Creamos un dataFrame a base del diccionario de dias que jugaron.

    diasJugados = pd.DataFrame({'Dias':queDiaJugo(lista_fechas_ByR).keys(), 'cantidad':queDiaJugo(lista_fechas_ByR).values()})
    print(diasJugados)
    
    # Lo mostramos como un grafico de Barras junto a otro de torta.
    plt.style.use('dark_background')
    
    plt.figure(figsize=(10, 6), facecolor='#37474f')
    plt.subplot(211)
    plt.bar(diasJugados['Dias'], diasJugados['cantidad'])
    plt.title("Dias de la semana Boca vs River", color='white',fontname='Impact', fontsize=30, )
    plt.subplot(212)
    plt.pie(diasJugados['cantidad'][diasJugados['cantidad']>0],autopct='%1.1f%%',labels=diasJugados['Dias'][diasJugados['cantidad']>0])
    plt.show()
    
### RIVER BOCA SOLO DOMINGOS

# Esta funcion nos devuelve los valores en formato valor mas su porcentaje del total.
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

### Sigue importando la localia del equipo? Nos preguntamos que tanta incidencia tiene jugar como local.
# La tendencia ira en descenso a lo largo del tiempo?
def p1():
    plt.style.use('dark_background')
    # LOCALES
    # Comenzamos almacenando los datos de los equipos jugando como locales.
    # Para trabajar mas comodo decidimos agregar una columna mas al dataFrame, donde nos mostrara el año en que se jugo.
    # pasamos todas las fechas a una lista.
    dfaux = df['fecha_encuentro'].tolist()
    # Luego de eso modificamos los Strings para quedarnos con las fechas.
    for x in range(len(dfaux)):
        dfaux[x] = str(dfaux[x])[0:4]
    # Generamos una serie a base de esa lista.
    dfaux = pd.Series(dfaux)
    # Le agregamos nombre
    dfaux.name = 'Año jugado'    
    # Y hacemos un dataFrame con la nueva columna ('Año jugado).
    dfLoV = df.join(dfaux, how='outer')
     # Agregue fechas en lugares especificos, ya que los datos de 'fecha_encuentro' no existian.
    dfLoV.iloc[104,34] = '2015'
    dfLoV.iloc[329,34] = '2015'
    dfLoV.iloc[1595,34] = '2018'
     # *****
    
    print(dfLoV[['Año jugado','fecha_encuentro','torneo','resultado']].to_string())
    ##aro = dfLoV[(dfLoV['Año jugado']== 'nan')]
    ##print(aro[['Año jugado','fecha_encuentro','torneo','resultado']])
    
    # Almacenamos datos de nuestro data frame agrupados por los equipos que jugaron de local y contamos sus resultados.
    resultados_local = dfLoV.groupby('equipo_local')['resultado'].value_counts()
    print(resultados_local)
    
    # Procedemos a ver si se encuentra algun outlier. Lo tomamos de la siguiente manera: En los locales
    # hay algun equipo que este teniendo mas victorias, derrotas o empates que el resto? 
    Q1 = resultados_local.quantile(0.25)
    Q3 = resultados_local.quantile(0.75)
    IQR = Q3 - Q1

    bS = (Q3 + 1.5 *IQR)
    bI = (Q1 - 1.5 *IQR)

    ubicacionOutliers = (resultados_local < bI) | (resultados_local > bS)
    # Agrupamos los resultados de los equipos que jugaron de local.
    Lganados = (df['resultado'] == 'L').sum()
    Lperdidos = (df['resultado'] == 'V').sum()
    Lempate = (df['resultado'] == 'E').sum()
    outliersL = df[df['resultado']=='L'].groupby('equipo_local')['resultado'].value_counts()[ubicacionOutliers].sum()
    outliersV = df[df['resultado']=='V'].groupby('equipo_local')['resultado'].value_counts()[ubicacionOutliers].sum()
    outliersE = df[df['resultado']=='E'].groupby('equipo_local')['resultado'].value_counts()[ubicacionOutliers].sum()
    
    print(f"Locales ganados: {Lganados}")
    print(f"Locales perdidos: {Lperdidos}")
    print(f"Locales empatados: {Lempate}")
    print(f"Outlaiers Ganados: {outliersL}")
    print(f"Outlaiers perdidos: {outliersV}")
    print(f"Outlaiers empatados: {outliersE}")
    # Ya que encontramos que solo existen outliers en los partidos ganados por locales, los restamos de la cuenta para
    # datos mas precisos.
    Lganados = int(Lganados-outliersL)
    
    print("\n")
    # Mostramos quienes son los equipos que resultan atipicos en alguno de sus resultados.
    print(resultados_local[ubicacionOutliers])
    plt.figure(figsize=(10, 6), facecolor='#37474f')
    plt.boxplot(resultados_local,vert=False)
    
    plt.show()
    
    ### VISITANTE
    # Ahora haremos lo mismo pero con los visitantes: almacenando los datos de los equipos jugando como visitantes.
    # Creamos una serie que agrupe los equipos visitantes y cuente sus resultados.
    resultados_visitante = df.groupby('equipo_visitante')['resultado'].value_counts()
    #print(resultados_visitante)
    
    # Busamos si hay algun outlier.
    Q1 = resultados_visitante.quantile(0.25)
    Q3 = resultados_visitante.quantile(0.75)
    IQR = Q3 - Q1

    bS = (Q3 + 1.5 *IQR)
    bI = (Q1 - 1.5 *IQR)

    ubicacionOutliers = (resultados_visitante < bI) | (resultados_visitante > bS)
    # En vista de que no lo encontramos seguiremos normalemente.
    print(resultados_visitante[ubicacionOutliers])

    # Agrupamos las Victorias, Derrotas y empates de los equipos jugando como visitante.
    Vperdidos = (df['resultado'] == 'L').sum()
    Vganados = (df['resultado'] == 'V').sum()
    Vempate = (df['resultado'] == 'E').sum()
    outliersL = df[df['resultado']=='L'].groupby('equipo_visitante')['resultado'].value_counts()[ubicacionOutliers].sum()
    outliersV = df[df['resultado']=='V'].groupby('equipo_visitante')['resultado'].value_counts()[ubicacionOutliers].sum()
    outliersE = df[df['resultado']=='E'].groupby('equipo_visitante')['resultado'].value_counts()[ubicacionOutliers].sum()

    print(f"Visitante perdidos: {Vperdidos}")
    print(f"Visitante ganados: {Vganados}")
    print(f"Visitante empatados: {Vempate}")
    print(f"Outlaiers perdidos: {outliersL}")
    print(f"Outlaiers ganados: {outliersV}")
    print(f"Outlaiers empatados: {outliersE}")

    # Visualizamos la cantidad de victorias como visitantes y como locales con un grafico de torta.
    plt.figure(figsize=(10, 6), facecolor='#37474f')
    colores = ['orange', 'blue']
    Comparativa_visitante_local = pd.Series({'Locales ganados':Lganados, 'Visitantes ganados':Vganados})
    Comparativa_visitante_local.plot(kind='pie',label=f'Partidos jugados de visitante: {Vganados+Lganados}', autopct=make_autopct([Vganados,Lganados]))
    
    plt.show()
    
    # Usamos el dataFrame que hicimos anteriormente para visualizar los resultados a lo largo del tiempo.
    agrupacion = dfLoV.groupby('Año jugado')['resultado'].value_counts()
    plt.figure(figsize=(10, 6), facecolor='#37474f')
    agrupacion.plot(kind='bar',color=['#FFD700','#C0C0C0','#8C7853'],width=0.8,
             figsize=(10,4))
    plt.tight_layout()
    
    plt.show()

############

### Existe una relacion entre la cantidad de zurdos y el porcentaje de goles de los equipos?
# Acaso el tener una mayor proporcion jugando a favor de un equipo afectaria los resultado?
def p2():
    # Para tener un mejor control de los datos generamos cuatro variables teniendo en cuenta si jugaban de local o visitante.
    # De esta manera podriamos comprar los datos de partidos de una manera mas justa.
    # Ademas contamos como un dato que sumaria a 'victorias_menos_zurdos_...' todas aquellas victorias en las cuales ambos equipos tuvieran la misma proporcion de zurdos.
    victorias_mas_zurdos_local = df[((df['proporcion_zurdos_local']>df['proporcion_zurdos_visitante']) & (df['resultado']=='L')) ].shape[0]
    victorias_menos_zurdos_local = df[((df['proporcion_zurdos_local']<=df['proporcion_zurdos_visitante']) & (df['resultado']=='L')) ].shape[0]
    victorias_mas_zurdos_visitante = df[((df['proporcion_zurdos_local']<df['proporcion_zurdos_visitante']) & (df['resultado']=='V')) ].shape[0]
    victorias_menos_zurdos_visitante = df[((df['proporcion_zurdos_local']>=df['proporcion_zurdos_visitante']) & (df['resultado']=='V')) ].shape[0]

    print(df[['resultado','proporcion_zurdos_local','proporcion_zurdos_visitante']].head(10))
    print(f"Victorias donde hubo mas zurdos de local: {victorias_mas_zurdos_local}") #| ((df['proporcion_zurdos_local']<df['proporcion_zurdos_visitante']) & (df['resultado']=='V'))
    print(f"Victorias donde hubo menos zurdos de local: {victorias_menos_zurdos_local}") #| ((df['proporcion_zurdos_local']>df['proporcion_zurdos_visitante']) & (df['resultado']=='V'))
    print(f"Victorias dinde hubo mas zurdos de visitante: {victorias_mas_zurdos_visitante}") 
    print(f"Victorias donde hubo menos zurdos de visitante: {victorias_menos_zurdos_visitante}")

    # Generamos una serie con los datos anteriores.
    gana_masOmenos_zurdos = pd.Series({'victorias mas zurdos (local)':victorias_mas_zurdos_local,'victorias menos zurdos (local)':victorias_menos_zurdos_local,'victorias mas zurdos (visitante)':victorias_mas_zurdos_visitante,'victorias menos zurdos (visitante)':victorias_menos_zurdos_visitante})
    lista_victorias=[victorias_mas_zurdos_local,victorias_menos_zurdos_local,victorias_mas_zurdos_visitante,victorias_menos_zurdos_visitante]
    # Y con ello enseñamos los resultados con un grafico de torta.
    gana_masOmenos_zurdos.plot(kind='pie',autopct=make_autopct(lista_victorias))
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6), facecolor='#37474f')
    plt.show()
    
    
    
    ### Existe una relacion entre la cantidad de goles antes y despues del VAR?
def p3():
    # Definir una función de agregación personalizada para calcular el promedio de goles totales por partido
    def promedio_goles_totales_por_partido(group):
        total_goles = group['goles_local'].sum() + group['goles_visitante'].sum()
        return pd.Series({'promedio_goles_totales': total_goles / len(group)})

    # Agrupar los datos por el nombre del torneo y aplicar la función de agregación personalizada
    total_goles = df.groupby('torneo').apply(promedio_goles_totales_por_partido).reset_index()

    # Ordenar el DataFrame 'total_goles' según el orden personalizado de los campeonatos
    orden_personalizado_campeonatos = ['Campeonato 2015', 'Transicion 2016', 'Campeonato 2016/17', 'Campeonato 2017/18', 'Campeonato 2018/19', 'Superliga 2019/20','Campeonato 2021', 'Campeonato 2022']
    total_goles['torneo'] = pd.Categorical(total_goles['torneo'], categories=orden_personalizado_campeonatos, ordered=True)
    total_goles.sort_values(by='torneo', inplace=True)

    # Crear el gráfico de líneas
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6), facecolor='#37474f')
    plt.plot(total_goles['torneo'], total_goles['promedio_goles_totales'], marker='+', linestyle='-', color='r')
    plt.xlabel('Torneo')
    plt.ylabel('Promedio de goles totales por partido')
    plt.title('Promedio de goles totales por campeonato (orden personalizado)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    ### Existe una relacion entre la cantidad de amarillas y rojas antes y despues del VAR?
def p4():
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
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6), facecolor='#37474f')
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
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6), facecolor='#37474f')
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
    ####
    
ventana = tk.Tk()
ventana.config(width = 600, height = 350, bg="#2E2B2B")
ventana.resizable(False, False)
import tkinter.font as tkFont
label = ttk.Label(text='CAMPEONATOS ARGENTINA 2015-2022',font=tkFont.Font(family="Lucida Grande", size=18,weight='bold'),background="#2E2B2B", foreground='white')
label.place(x = 65, height=70)


boton = tk.Button(text = "Los Boca-River se juegan solo los domingos?",command=p0,background="#595568",activebackground="#2E2B2B",width=60,height=2)
boton.place(x = 80, y = 80)

boton1 = tk.Button(text = "Importa la localia del equipo?", command=p1,background="#595568",activebackground="#2E2B2B",width=60,height=2)
boton1.place(x = 80, y = 130)

boton2 = tk.Button(text = "Existe una relacion entre la cantidad de zurdos y la cantidad de victorias?", command=p2,background="#595568",activebackground="#2E2B2B",width=60,height=2)
boton2.place(x = 80, y = 180)

boton3 = tk.Button(text = "Existe una relacion entre la cantidad de goles antes y despues del VAR?", command=p3,background="#595568",activebackground="#2E2B2B",width=60,height=2)
boton3.place(x = 80, y = 230)

boton4 = tk.Button(text = "Existe una relacion entre la cantidad de amarillas y rojas antes y despues del VAR?", command=p4,background="#595568",activebackground="#2E2B2B",width=60,height=2)
boton4.place(x = 80, y = 280)

ventana.mainloop()
