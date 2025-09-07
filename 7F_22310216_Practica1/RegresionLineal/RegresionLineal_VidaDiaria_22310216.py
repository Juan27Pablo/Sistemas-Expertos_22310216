import numpy as np
import matplotlib.pyplot as plt

# Datos de ejemplo: km recorridos
km = np.array([0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500])
# Precio por litro
precio_litro = 20
# Litros usados y gasto real con un poco de ruido para simular datos reales
np.random.seed(0)  # para reproducibilidad
litros_usados = km / 11
gasto = litros_usados * precio_litro + np.random.normal(0, 5, size=len(km))  # ruido ±5 $

# Valor específico de w para comparar ($ por km)
w1 = precio_litro / 11  # costo estimado por km

# Pedir al usuario los km recorridos
km_usuario = float(input("Ingresa los kilómetros que recorriste: "))

# Calcular litros y gasto estimado
litros_usuario = km_usuario / 11
gasto_usuario = litros_usuario * precio_litro

print(f"\nHas consumido aproximadamente {litros_usuario:.2f} litros de gasolina.")
print(f"El gasto estimado en gasolina es: ${gasto_usuario:.2f}\n")

# Predicciones con w1 y cálculo del error
gasto_pred = w1 * km
E = (1 / (2 * len(km))) * np.sum(np.power(gasto - gasto_pred, 2))
print(f"Error cuadrático medio para w = {w1:.2f} $/km: {E:.4f}\n")

# Rango de valores de w para evaluar
w_values = np.linspace(1, 3, 50)  # $/km
E_values = []

# Cálculo del error cuadrático medio para cada w
for w in w_values:
    gasto_temp = w * km
    E_temp = (1 / (2 * len(km))) * np.sum(np.power(gasto - gasto_temp, 2))
    E_values.append(E_temp)

# Graficar w vs error
plt.figure(figsize=(10, 6))
plt.plot(w_values, E_values, label="Error medio E", color="red")
plt.scatter(w1, E, color="blue", zorder=3, label=f"Punto modelo ($w={w1:.2f}$, $E={E:.2f}$)")

plt.xlabel("Costo por km ($w$)")
plt.ylabel("Error cuadrático medio $E$")
plt.title("Error cuadrático medio según el costo por km")
plt.legend()
plt.grid(True)
plt.show()
