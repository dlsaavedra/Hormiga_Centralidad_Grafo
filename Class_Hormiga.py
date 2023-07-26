# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 15:24:32 2023

@author: danie
"""

import pickle
import networkx as nx
import random
from tqdm import tqdm  # Importar la librería tqdm
import numpy as np
import timeit

class Hormiga:
    def __init__(self, identificador, posicion=None):
        self.id = identificador
        self.posicion = posicion
        self.espera = 0
        
    def moverse(self, grafo):
        if self.posicion is None:
            # Colocar la hormiga en un nodo aleatorio si no tiene posición inicial
            self.posicion = random.choice(list(grafo.nodes()))
        else:
            # Obtener los vecinos del nodo actual
            vecinos = list(grafo.neighbors(self.posicion))
            if vecinos:
                # Mover la hormiga a un vecino aleatorio
                self.posicion = random.choice(vecinos)

    def moverse_espera(self, grafo):
        if self.espera > 0: 
            self.espera -= 1
            return False
        elif self.posicion is None:
            # Colocar la hormiga en un nodo aleatorio si no tiene posición inicial
            self.posicion = random.choice(list(grafo.nodes()))
            return True
        else:
            # Obtener los vecinos del nodo actual
            vecinos = list(grafo.neighbors(self.posicion))
            if vecinos:
                # Mover la hormiga a un vecino aleatorio
                self.posicion = random.choice(vecinos)
                return True

class Hormiguero:
    def __init__(self, num_hormigas, grafo):
        self.hormigas = [Hormiga(i) for i in range(num_hormigas)]
        self.grafo = grafo
        self.num_hormigas = num_hormigas
        self.mover_hormigas_basic()
        
        
    def mover_hormigas_basic(self):
        for hormiga in self.hormigas:
            hormiga.moverse(self.grafo)

    def mover_hormigas_espera(self, t_espera):
        conteo_hormigas = self.contar_hormigas_por_nodo()
        for hormiga in self.hormigas:
            if hormiga.moverse_espera(self.grafo):
                hormiga.espera = round(conteo_hormigas[hormiga.posicion]**t_espera) - 1
               
    def contar_hormigas_por_nodo(self):
        conteo_hormigas = {nodo: 0 for nodo in self.grafo.nodes()}
        for hormiga in self.hormigas:
            conteo_hormigas[hormiga.posicion] += 1
        return conteo_hormigas
    
    def proporcion_hormigas_por_nodo(self):
        conteo_hormigas = self.contar_hormigas_por_nodo()
        for aux in conteo_hormigas:
            conteo_hormigas[aux] /= self.num_hormigas
        return conteo_hormigas


#%% Funciones

def Hormiga_centrality_basic(grafo, num_hormigas = 1000, steps = 1000, epochs = 100):

    proporciones_por_simulacion = []
    for _ in tqdm(range(epochs)):
        # Crear el hormiguero con 5 hormigas y el grafo aleatorio
       
        hormiguero = Hormiguero(num_hormigas = num_hormigas, grafo = grafo)
        # Mover las hormigas durante 10 pasos
        for _ in range(steps):
            hormiguero.mover_hormigas_basic()
        # Obtener la proporción de hormigas en cada nodo
        proporciones_hormigas = hormiguero.proporcion_hormigas_por_nodo()

        # Guardar las proporciones en la lista de resultados
        proporciones_por_simulacion.append(list(proporciones_hormigas.values()))
    
    return np.array(proporciones_por_simulacion) 

def Hormiga_centrality_basic_progress(grafo, num_hormigas = 1000, steps = 100):
    
    proporciones_por_step = []
    hormiguero = Hormiguero(num_hormigas = num_hormigas, grafo = grafo)
    # Mover las hormigas durante 10 pasos
    for _ in range(steps):
        hormiguero.mover_hormigas_basic()
        proporciones_por_step.append(list(hormiguero.proporcion_hormigas_por_nodo().values()))
        
    return np.array(proporciones_por_step)



def Hormiga_centrality_espera(grafo, num_hormigas = 1000, steps = 1000, epochs = 100, t_espera = 1):

    proporciones_por_simulacion = []
    for _ in tqdm(range(epochs)):
        # Crear el hormiguero con 5 hormigas y el grafo aleatorio
       
        hormiguero = Hormiguero(num_hormigas = num_hormigas, grafo = grafo)
        # Mover las hormigas durante 10 pasos
        for _ in range(steps):
            hormiguero.mover_hormigas_espera(t_espera = t_espera)
        # Obtener la proporción de hormigas en cada nodo
        proporciones_hormigas = hormiguero.proporcion_hormigas_por_nodo()

        # Guardar las proporciones en la lista de resultados
        proporciones_por_simulacion.append(list(proporciones_hormigas.values()))
    
    return np.array(proporciones_por_simulacion) 

def Hormiga_centrality_espera_progress(grafo, num_hormigas = 1000, steps = 100, t_espera = 1):
    
    proporciones_por_step = []
    hormiguero = Hormiguero(num_hormigas = num_hormigas, grafo = grafo)
    # Mover las hormigas durante 10 pasos
    for _ in range(steps):
        hormiguero.mover_hormigas_espera( t_espera = t_espera)
        proporciones_por_step.append(list(hormiguero.proporcion_hormigas_por_nodo().values()))
        
    return np.array(proporciones_por_step)

def evaluar_tiempo_funcion(funcion, parametros, num_repeticiones):
    resultados = {}

    for params in parametros:
        
        # Medir el tiempo de ejecución
        tiempo_promedio = timeit.timeit(lambda: funcion(*params), number=num_repeticiones) / num_repeticiones

        # Registrar el tiempo promedio en el diccionario de resultados
        resultados[(params)] = tiempo_promedio

    return resultados
