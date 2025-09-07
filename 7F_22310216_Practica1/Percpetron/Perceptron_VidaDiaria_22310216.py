import numpy as np

# Datos de entrenamiento (bias + características)
x0 = [1, 1, 1, 1]  # bias
x1 = [0, 0, 1, 1]  # Probabilidad de lluvia (0=no, 1=sí)
x2 = [0, 1, 0, 1]  # Paraguas disponible (0=no, 1=sí)
y = [0, 0, 1, 1]   # Decisión final (0=no llevar, 1=llevar)

# Pesos iniciales y tasa de aprendizaje
w = np.array([0.5, 0.5, 0.5], dtype=float)
learning_rate = 0.5

# Función escalón
def step(z):
    return 1 if z >= 0.5 else 0  # Umbral para 0/1

# Entrenamiento del perceptrón
while True:
    total_error = 0
    for i in range(len(y)):
        x = np.array([x0[i], x1[i], x2[i]])
        y_est = step(np.dot(w, x))
        error = y[i] - y_est
        w += learning_rate * error * x
        total_error += abs(error)
    
    if total_error == 0:
        break

print("Perceptrón entrenado. Pesos finales:", w)

# Interacción con el usuario
print("\n--- Decide si llevar paraguas ---")
lluvia = int(input("¿Hay probabilidad de lluvia? (0=no, 1=sí): "))
paraguas = int(input("¿Tienes paraguas en casa? (0=no, 1=sí): "))

x_usuario = np.array([1, lluvia, paraguas])
decision = step(np.dot(w, x_usuario))

if decision == 1:
    print("➡️ Deberías llevar paraguas.")
else:
    print("➡️ No necesitas llevar paraguas.")
