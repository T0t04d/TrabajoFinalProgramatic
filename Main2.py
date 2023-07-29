import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("afa_2015_2022_spa.csv")


### RIVER BOCA SOLO DOMINGOS
ByR = df[((df['equipo_local'] == 'River Plate') | (df['equipo_local'] == 'Boca Juniors')) & ((df['equipo_visitante'] == 'River Plate') | (df['equipo_visitante'] == 'Boca Juniors'))].sort_values('fecha_encuentro')
lista_fechas_ByR = ByR['fecha_encuentro']
print(lista_fechas_ByR)

from datetime import datetime
def fueDomingo(lista):
    days = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'viernes', 'Sabado', 'Domingo']
    for x in lista:
        d = datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S")
        if days[d.weekday()] != 'Domingo':
            return False
    return True
print(fueDomingo(lista_fechas_ByR))
### RIVER BOCA SOLO DOMINGOS


### Sigue importando la localia del equipo?

cl = pd.Series((df.groupby('equipo_local')['resultado'].value_counts()),name='r')
print(cl)
q1 = cl.quantile(0.25)
q3 = cl.quantile(0.75)
iqr = q3 - q1

#Calculo de bigotes inferior y superior:
bI = (q1 - 1.5 *iqr)
bS = (q3 + 1.5 *iqr)


#Ubicacion outliers
ubicacionOutliers = (cl < bI) | (cl > bS)
#print(f"Ubicacion de Outliers:\n{ubicacionOutliers}")
print(f"Lista de OutLiers:\n{cl[ubicacionOutliers]}")

'''cv = pd.Series((df.groupby('equipo_visitante')['resultado'].value_counts()),name='r')
print(cv)
q1 = cv.quantile(0.25)
q3 = cv.quantile(0.75)
iqr = q3 - q1

#Calculo de bigotes inferior y superior:
bI = (q1 - 1.5 *iqr)
bS = (q3 + 1.5 *iqr)


#Ubicacion outliers
ubicacionOutliers = (cv < bI) | (cv > bS)
#print(f"Ubicacion de Outliers:\n{ubicacionOutliers}")
print(f"Lista de OutLiers:\n{cv[ubicacionOutliers]}")'''

'''plt.title('Local o visitante')
plt.boxplot(cv, vert=False)
plt.show()'''

resultados.plot()
plt.show()

