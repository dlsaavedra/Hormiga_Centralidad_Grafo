# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 15:27:00 2023

@author: danie
"""



import os
os.chdir('/Users/danielsaavedramorales/Library/CloudStorage/OneDrive-UniversidadCatólicadeChile/Desktop/Codigo_Python_otros/Centralidad_Grafos')

import networkx as nx
import matplotlib.pyplot as plt
import pickle
#from Creacion_Grafo import Create_Graph_random
from Class_Hormiga import Hormiga_centrality_basic,Hormiga_centrality_basic_progress ,evaluar_tiempo_funcion, Hormiga_centrality_espera, Hormiga_centrality_espera_progress
#from tqdm import tqdm  # Importar la librería tqdm
import numpy as np
import timeit
import itertools
from matplotlib.widgets import Slider
import matplotlib as mpl


#%% Cargar Grafo

    
with open('grafo_prueba_complete10.obj', 'rb') as file:
    G= pickle.load(file)
    
#%% Dibujar Grafo
# Calcular el grado de cada nodo
node_degrees = dict(G.degree())

# Ajustar el tamaño de los nodos en base a su grado
node_sizes = [1000/G.number_of_nodes() * (node_degrees[node] + 0.1) for node in G.nodes()]


# Visualizar el grafo
plt.figure(figsize=(8, 6))
pos = nx.random_layout(G, seed = 1)
nx.draw_networkx(G, pos, with_labels=True, node_size=node_sizes, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray', width=1.5)
plt.title('Grafo Aleatorio con 100 Nodos y Aristas Aleatorias', fontsize=12)
plt.show()

#%% # Calcular estadísticos de centralidad

proporciones_por_simulacion = Hormiga_centrality_basic(G,num_hormigas = 20, steps = 1000, epochs = 1000 )
promedio_proporciones = np.mean(proporciones_por_simulacion, axis=0)
desviacion_estandar_proporciones = np.std(proporciones_por_simulacion, axis=0)
print("Nodo central Hormigas", np.argmax(promedio_proporciones))

proporciones_por_simulacion_espera = Hormiga_centrality_espera(G,num_hormigas = 20, steps = 1000, epochs = 1000, t_espera=  1)
promedio_proporciones_espera = np.mean(proporciones_por_simulacion_espera, axis=0) 
desviacion_estandar_proporciones = np.std(proporciones_por_simulacion_espera, axis=0)
print("Nodo central Hormigas Espera", np.argmax(promedio_proporciones_espera))
#%%

degree_centrality = nx.degree_centrality(G)
print("Nodo central degree", np.argmax(list(degree_centrality.values())))
closeness_centrality = nx.closeness_centrality(G)
print("Nodo central closeness",np.argmax(list(closeness_centrality.values())))
betweenness_centrality = nx.betweenness_centrality(G)
print("Nodo central betweeness", np.argmax(list(betweenness_centrality.values())))
eigenvector_centrality = nx.eigenvector_centrality(G)
print("Nodo central eigenvector", np.argmax(list(eigenvector_centrality.values())))
# Calcular el PageRank Centrality
pagerank_centralities = nx.pagerank(G)
print("Nodo central pagerank",np.argmax(list(pagerank_centralities.values())))

#%%
import matplotlib as mpl
# Imprimir los resultados de los estadísticos de centralidad
plt.close("all")
mpl.use('module://matplotlib_inline.backend_inline')

print("Grado de centralidad:", degree_centrality)
print("Cercanía de centralidad:", closeness_centrality)
print("Intermediación de centralidad:", betweenness_centrality)
print("Autovector de centralidad:", eigenvector_centrality)
print("hormigas de centralidad:", promedio_proporciones)
print("PageRank de centralidad:", pagerank_centralities)
plt.bar(list(degree_centrality.keys()),list(degree_centrality.values()))
plt.title("degree_centrality")
plt.show()
plt.bar(list(closeness_centrality.keys()),list(closeness_centrality.values()))
plt.title("closeness_centrality")
plt.show()
plt.bar(list(betweenness_centrality.keys()),list(betweenness_centrality.values()))
plt.title("betweenness_centrality")
plt.show()
plt.bar(list(eigenvector_centrality.keys()),list(eigenvector_centrality.values()))
plt.title("eigenvector_centrality")
plt.show()
plt.bar(list(pagerank_centralities.keys()),list(pagerank_centralities.values()))
plt.title("pagerank_centrality")
plt.show()
plt.bar(range(len(promedio_proporciones)),promedio_proporciones/max(promedio_proporciones))
plt.title("hormigas_centrality")
plt.show()
plt.bar(range(len(promedio_proporciones_espera)),promedio_proporciones_espera/max(promedio_proporciones_espera))
plt.title("hormigas_centrality espera")
plt.show()


#%% Evolución en el costo tiempo en el numero de nodos, pasos y cantidad de hormigas.

list_num_nodes = [10**n for n in range(1,7)]
params_steps = [10**n for n in range(3)]
params_num_hormigas = [10**n for n in range(3)]
params_epoch = 1
Grafos = [Create_Graph_random(num_nodes, num_nodes * 3) for num_nodes in list_num_nodes]
grilla_combinada = list(itertools.product(Grafos, params_steps, params_num_hormigas))
# Crear la nueva grilla con el elemento constante
nueva_grilla = [tupla + (params_epoch,) for tupla in grilla_combinada]

resultado_tiempo = evaluar_tiempo_funcion(Hormiga_centrality_basic, 
                                          nueva_grilla, num_repeticiones = 10)

#%% Tiempo Centrality basic
# 1MM step 10000 hormigas = 1000 37.3seg 
# 1MM step 1000 hormigas = 1000 16.5seg 
# 1MM step 100 hormigas = 1000 14.8seg 
# 1MM step 10000 hormigas = 100 3.6seg 
# 1MM step 10000 hormigas = 10 0.7seg 
# 1MM step 100000 hormigas = 10 2.3seg
# 1MM step 100000 hormigas = 100 22.4seg  
# 1MM step 10 hormigas = 10000 147seg   
timeit.timeit(lambda : Hormiga_centrality_basic(Grafos[5], num_hormigas=10000, steps = 10, epochs=1), number=1)

#%%% Evolución del histograma

proporciones_por_step = Hormiga_centrality_espera_progress(G,num_hormigas = 1000, steps = 1000, t_espera = 1)
#proporciones_por_step = Hormiga_centrality_basic_progress(G,num_hormigas = 100, steps = 1000)

mpl.use('WebAgg')
plt.close("all")

array = proporciones_por_step

def update(val):
    
    st = round(step.val)
    #print(st)
    # Redraw histogram
    ax.cla()
        
    ax.bar(range(len(array[st,])),array[st,])
    plt.draw()

def reset(event):
    
    step.reset()

ax = plt.subplot(111)
plt.subplots_adjust(left=0.25, bottom=0.25)


step0 = 30


plt.bar(range(len(array[step0,])),array[step0,])
plt.title("hormigas_centrality")

axcolor = 'lightgray'
axstep = plt.axes([0.25, 0.1, 0.65, 0.1], facecolor=axcolor)
step = Slider(axstep, 'Step', 0, array.shape[0]-1,valstep=1, valinit=step0,)
step.on_changed(update)

resetax = plt.axes([0.9, 0.025, 0.1, 0.04])
button_reset = plt.Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
button_reset.on_clicked(reset)

plt.show()
#%%
