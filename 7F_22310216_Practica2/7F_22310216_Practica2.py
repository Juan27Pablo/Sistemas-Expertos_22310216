import json
import os

# Archivo donde se guardará el conocimiento
DB_FILE = "knowledge.json"

# Conocimiento base inicial (simulación de entrevista de trabajo)
default_knowledge = {
   "hola": "¡Hola! ¿Cómo estás?",
    "como estas": "Muy bien, gracias. ¿Y tú?",
    "de que te gustaria hablar": "Podemos hablar de tecnología, música o lo que tú quieras."
}

# Función para cargar la base de conocimiento
def load_knowledge():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return default_knowledge.copy()

# Función para guardar el conocimiento
def save_knowledge(knowledge):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=4, ensure_ascii=False)

# Función principal del chat
def chat():
    print("Chatbot de Entrevista iniciado. Escribe 'salir' para terminar.")
    knowledge = load_knowledge()

    while True:
        user_input = input("Tú: ").strip().lower()
        if user_input == "salir":
            print("Chatbot: ¡Hasta pronto y mucho éxito en tu entrevista!")
            break

        # Buscar respuesta en la base de conocimiento
        if user_input in knowledge:
            print("Chatbot:", knowledge[user_input])
        else:
            print("Chatbot: No sé cómo responder a eso...")
            new_response = input("👉 ¿Qué debería responder a esa frase?: ")
            knowledge[user_input] = new_response
            save_knowledge(knowledge)
            print("Chatbot: ¡Gracias! He aprendido algo nuevo.")

# Ejecutar el chatbot
if __name__ == "__main__":
    chat()
