import heapq
from collections import deque, defaultdict
import unicodedata

# Definición del grafo
localidades = {
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)],
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)],
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)],
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)],
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)],
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)],
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)],
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)],
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)],
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)]
}

# Función para normalizar el texto (eliminar tildes y convertir a minúsculas)
def normalizar_texto(texto):
    texto = texto.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Crear un diccionario de localidades normalizadas para validar entradas
localidades_normalizadas = {normalizar_texto(k): k for k in localidades.keys()}

# Función para solicitar una localidad válida
def solicitar_localidad(mensaje):
    while True:
        entrada = input(mensaje)
        localidad_normalizada = normalizar_texto(entrada)
        if localidad_normalizada in localidades_normalizadas:
            return localidades_normalizadas[localidad_normalizada]
        else:
            print("Localidad no válida. Inténtelo de nuevo.")

# 1. Encontrar la Ruta Más Corta entre dos Localidades
def dijkstra(grafo, origen, destino):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    padre = {nodo: None for nodo in grafo}
    queue = [(0, origen)]
    
    while queue:
        distancia_actual, nodo_actual = heapq.heappop(queue)
        
        if nodo_actual == destino:
            break
        
        for vecino, peso in grafo[nodo_actual]:
            distancia = distancia_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                padre[vecino] = nodo_actual
                heapq.heappush(queue, (distancia, vecino))
    
    # Reconstruir la ruta
    ruta = []
    nodo = destino
    while nodo:
        ruta.append(nodo)
        nodo = padre[nodo]
    ruta.reverse()
    
    return ruta, distancias[destino]

# 2. Identificar Localidades con Conexiones Cortas
def localidades_con_conexiones_cortas(grafo, max_distancia=15):
    localidades_cortas = []
    for localidad, conexiones in grafo.items():
        if all(distancia < max_distancia for _, distancia in conexiones):
            localidades_cortas.append(localidad)
    return localidades_cortas

# 3. Verificar la Conectividad del Grafo
def es_conexo(grafo):
    visitados = set()
    
    def dfs(nodo):
        stack = [nodo]
        while stack:
            actual = stack.pop()
            if actual not in visitados:
                visitados.add(actual)
                stack.extend(vecino for vecino, _ in grafo[actual] if vecino not in visitados)
    
    nodo_inicial = next(iter(grafo))
    dfs(nodo_inicial)
    
    return len(visitados) == len(grafo)

# 4. Rutas Alternativas entre dos Localidades sin Ciclos
def rutas_sin_ciclos(grafo, origen, destino):
    rutas = []
    queue = deque([(origen, [origen])])
    
    while queue:
        nodo_actual, ruta = queue.popleft()
        
        if nodo_actual == destino:
            rutas.append(ruta)
        else:
            for vecino, _ in grafo[nodo_actual]:
                if vecino not in ruta:  # Evitar ciclos
                    queue.append((vecino, ruta + [vecino]))
    
    return rutas

# 5. Ruta Más Larga sin Ciclos entre dos Localidades
def ruta_mas_larga(grafo, origen, destino):
    max_distancia = 0
    ruta_larga = []
    
    def dfs(nodo, ruta_actual, distancia_actual):
        nonlocal max_distancia, ruta_larga
        
        if nodo == destino:
            if distancia_actual > max_distancia:
                max_distancia = distancia_actual
                ruta_larga = list(ruta_actual)
            return
        
        for vecino, peso in grafo.get(nodo, []):
            if vecino not in ruta_actual:
                ruta_actual.append(vecino)
                dfs(vecino, ruta_actual, distancia_actual + peso)
                ruta_actual.pop()
    
    dfs(origen, [origen], 0)
    return ruta_larga, max_distancia

# Solicitar localidades de origen y destino al usuario
origen = solicitar_localidad("Ingrese la localidad de origen: ")
destino = solicitar_localidad("Ingrese la localidad de destino: ")

# Ejecución de funciones y salida de resultados
print("\n--- Ruta Más Corta ---")
ruta_corta, distancia_corta = dijkstra(localidades, origen, destino)
print(f"Ruta más corta entre {origen} y {destino}: {ruta_corta} con distancia de {distancia_corta} km")

print("\n--- Rutas Alternativas sin Ciclos ---")
rutas_alternativas = rutas_sin_ciclos(localidades, origen, destino)
print(f"Rutas alternativas sin ciclos entre {origen} y {destino}:")
for ruta in rutas_alternativas:
    print(" -> ".join(ruta))

print("\n--- Ruta Más Larga sin Ciclos ---")
ruta_larga, distancia_larga = ruta_mas_larga(localidades, origen, destino)
print(f"Ruta más larga sin ciclos entre {origen} y {destino}: {ruta_larga} con distancia de {distancia_larga} km")

print("\n--- Localidades con Conexiones Cortas (<15 km) ---")
localidades_cortas = localidades_con_conexiones_cortas(localidades)
print("Localidades con conexiones cortas:", localidades_cortas)

print("\n--- Conectividad del Grafo ---")
conexo = es_conexo(localidades)
print("El grafo es conexo" if conexo else "El grafo no es conexo")
