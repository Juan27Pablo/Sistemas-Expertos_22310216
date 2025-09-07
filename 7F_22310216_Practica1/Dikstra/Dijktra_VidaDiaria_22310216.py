def dijkstra(w, a, z):
    L = {node: float('inf') for node in w}
    L[a] = 0  
    predecesores = {node: None for node in w}  
    T = set(w.keys())

    while T:
        v = min(T, key=lambda node: L[node])
        T.remove(v)
        if v == z:
            break  

        for x, weight in w[v].items():
            if x in T:
                nueva_distancia = L[v] + weight
                if nueva_distancia < L[x]:
                    L[x] = nueva_distancia
                    predecesores[x] = v  

    ruta = []
    nodo_actual = z
    while nodo_actual is not None:
        ruta.insert(0, nodo_actual)
        nodo_actual = predecesores[nodo_actual]

    return L[z], ruta


# Grafo de estaciones de metro con tiempo (en minutos) entre ellas
w = {
    'Insurgentes': {'Sevilla': 2, 'Chapultepec': 4},
    'Sevilla': {'Insurgentes': 2, 'Tacubaya': 6},
    'Chapultepec': {'Insurgentes': 4, 'Tacubaya': 3},
    'Tacubaya': {'Sevilla': 6, 'Chapultepec': 3, 'Centro': 8},
    'Centro': {'Tacubaya': 8, 'Zocalo': 5},
    'Zocalo': {'Centro': 5}
}

# Mostrar estaciones disponibles
print("📍 Estaciones disponibles:")
for estacion in w.keys():
    print(f" - {estacion}")

# Pedir inicio
while True:
    inicio = input("\nIngrese la estación de inicio: ").strip().title()
    if inicio in w:
        break
    else:
        print("⚠️ Estación inválida. Escoja una de la lista.")

# Pedir destino
while True:
    destino = input("Ingrese la estación de destino: ").strip().title()
    if destino in w:
        break
    else:
        print("⚠️ Estación inválida. Escoja una de la lista.")

# Calcular ruta
distancia, ruta = dijkstra(w, inicio, destino)
print(f"\n🛤️ El tiempo mínimo de '{inicio}' a '{destino}' es: {distancia} minutos")
print(f"➡️ La ruta más corta es: {' -> '.join(ruta)}")
