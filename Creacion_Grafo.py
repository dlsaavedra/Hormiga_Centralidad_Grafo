# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:42:09 2023

@author: danie
"""

import networkx as nx
import random
import matplotlib.pyplot as plt
import pickle


#seed = random.seed(3)
#%%

def Create_Graph_random(num_nodes, num_edges):
    # Crear un grafo vacío
    G = nx.Graph()

    G.add_nodes_from(range(num_nodes))
    # Agregar aristas aleatorias al grafo
    for _ in range(num_edges):
        node1 = random.randint(0, num_nodes - 1)
        node2 = random.randint(0, num_nodes - 1)
        while node1 == node2 or G.has_edge(node1, node2):
            node1 = random.randint(0, num_nodes - 1)
            node2 = random.randint(0, num_nodes - 1)
        G.add_edge(node1, node2)
        
    return G


#%%
num_nodes = 10
num_edges = 5
G = Create_Graph_random(num_nodes, num_edges)
ws = nx.watts_strogatz_graph(10, 3, 0.1)
er = nx.erdos_renyi_graph(10, 0.15)
ba = nx.barabasi_albert_graph(10, 5)
red = nx.random_lobster(10, 0.9, 0.9)
# Ver el número de nodos y aristas del grafo
print("Nodos:", G.nodes())
print("Aristas:", G.edges())
print("Número de nodos:", G.number_of_nodes())
print("Número de aristas:", G.number_of_edges())


#%%

#G = nx.bull_graph()
#G = nx.diamond_graph()
#G= nx.tutte_graph()
#G = nx.balanced_tree(r = 2, h = 4)
G = nx.complete_graph(10)
# Calcular el grado de cada nodo
node_degrees = dict(G.degree())

# Ajustar el tamaño de los nodos en base a su grado
node_sizes = [1000/num_nodes * (node_degrees[node] + 0.1) for node in G.nodes()]
# Visualizar el grafo
plt.figure(figsize=(8, 6))
pos = nx.random_layout(G, seed = 1)
nx.draw_networkx(G, pos, with_labels=True, node_size=node_sizes, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray', width=1.5)
plt.title('Grafo Aleatorio con 20 Nodos y Aristas Aleatorias', fontsize=12)
plt.show()


# %% Medidas de centralidad


# Calcular estadísticos de centralidad
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)
# Imprimir los resultados de los estadísticos de centralidad
print("Grado de centralidad:", degree_centrality)
print("Cercanía de centralidad:", closeness_centrality)
print("Intermediación de centralidad:", betweenness_centrality)
print("Autovector de centralidad:", eigenvector_centrality)

#%% Plot Centralidad
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
#%%

# Guardar el objeto G en un archivo usando pickle
with open('grafo_prueba_complete10.obj', 'wb') as file:
    pickle.dump(G, file)