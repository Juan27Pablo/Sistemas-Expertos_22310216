def dijkstra(grafo, inicio, destino):
    L = {nodo: float('inf') for nodo in grafo}
    L[inicio] = 0
    predecesores = {nodo: None for nodo in grafo}
    T = set(grafo.keys())

    while T:
        # Nodo con distancia mínima
        v = min(T, key=lambda nodo: L[nodo])
        T.remove(v)
        if v == destino:
            break

        # Actualizar tiempos de viaje de vecinos
        for vecino, tiempo in grafo[v].items():
            if vecino in T:
                nueva_distancia = L[v] + tiempo
                if nueva_distancia < L[vecino]:
                    L[vecino] = nueva_distancia
                    predecesores[vecino] = v

    # Reconstruir ruta
    ruta = []
    nodo_actual = destino
    while nodo_actual is not None:
        ruta.insert(0, nodo_actual)
        nodo_actual = predecesores[nodo_actual]

    return L[destino], ruta

# Grafo con estaciones ficticias y tiempos en minutos
metro_ficticio = {
    'sol': {'luna': 3, 'estrella': 2},
    'luna': {'sol': 3, 'cometa': 4, 'galaxia': 2},
    'estrella': {'sol': 2, 'cometa': 3, 'orion': 5},
    'cometa': {'luna': 4, 'estrella': 3, 'orion': 1},
    'galaxia': {'luna': 2, 'orion': 2, 'nebula': 6},
    'orion': {'estrella': 5, 'cometa': 1, 'galaxia': 2, 'nebula': 3},
    'nebula': {'galaxia': 6, 'orion': 3, 'cosmos': 4},
    'cosmos': {'nebula': 4}
}

# Función para pedir estaciones válidas
def pedir_estacion(mensaje, grafo):
    while True:
        estacion = input(mensaje).strip().lower()
        if estacion in grafo:
            return estacion
        else:
            print("Estación no válida. Intente de nuevo.")

# Pedir estaciones de origen y destino
origen = pedir_estacion("Ingrese la estación de origen: ", metro_ficticio)
destino = pedir_estacion("Ingrese la estación de destino: ", metro_ficticio)

# Calcular ruta más corta
tiempo_total, ruta = dijkstra(metro_ficticio, origen, destino)
print(f"\nEl tiempo mínimo de viaje de '{origen}' a '{destino}' es: {tiempo_total} minutos")
print(f"La ruta más rápida es: {' -> '.join(ruta)}")
