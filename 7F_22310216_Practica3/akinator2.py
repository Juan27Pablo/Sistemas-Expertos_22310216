import json
import os

DB_FILE = "balon_oro.json"

def cargar_conocimiento():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "Es hombre?": {
                "si": {
                    "Es sudamericano?": {
                        "si": {
                            "Jugo en la Liga de Espana?": {  
                                "si": {
                                    "Jugo en el Real Madrid?": {
                                        "si": "Kaka",         
                                        "no": {
                                            "Es Argentino?": {
                                                "si": "Lionel Messi",  
                                                "no": "Ronaldinho"    
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "no": {
                            "Jugo en la Premier League?": {
                                "si": {
                                    "Es ingles?": {
                                        "si": "Michael Owen",
                                        "no": "Cristiano Ronaldo"
                                    }
                                },
                                "no": {
                                    "Jugo en la Serie A?": {
                                        "si": "Luka Modric",
                                        "no": {
                                            "Jugo en la Ligue 1?": {
                                                "si": "Jean-Pierre Papin",
                                                "no": {
                                                    "Es aleman?": {
                                                        "si": "Lothar Matthaus",
                                                        "no": {
                                                            "Es frances?": {
                                                                "si": "Zinedine Zidane",
                                                                "no": "Andriy Shevchenko"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "no": {
                    "Juega en Europa?": {
                        "si": {
                            "Juega en la Liga F (Espana)?": {
                                "si": {
                                    "Juega en el FC Barcelona?": {
                                        "si": "Alexia Putellas",
                                        "no": "Aitana Bonmati"
                                    }
                                },
                                "no": "Ada Hegerberg"
                            }
                        },
                        "no": "Megan Rapinoe"
                    }
                }
            }
        }

def guardar_conocimiento(base):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(base, f, indent=4, ensure_ascii=False)

# --- APRENDER ---
def aprender(nodo, respuesta_jugador):
    print("No lo sabia...")
    correcto = input("Quien era el ganador o ganadora?: ").strip()
    nueva_pregunta = input(f"Dame una pregunta que distinga a {correcto} de {nodo}: ").strip()
    resp_correcta = input(f"Para {correcto}, la respuesta seria 'si' o 'no'?: ").strip().lower()

    # Creamos nuevo subnodo según la respuesta del jugador
    nuevo_nodo = {
        nueva_pregunta: {
            resp_correcta: correcto,
            "no" if resp_correcta == "si" else "si": nodo
        }
    }
    return nuevo_nodo

# --- FUNCION DE JUEGO ---
def jugar(nodo, base):
    if isinstance(nodo, str):
        print(f"?Es {nodo}?")
        resp = input("-> (si/no): ").strip().lower()
        if resp == "si":
            print(f"Adivine! Era {nodo}")
            return nodo
        else:
            nuevo_subnodo = aprender(nodo, resp)
            return nuevo_subnodo

    for pregunta, respuestas in nodo.items():
        print(pregunta)
        resp = input("-> (si/no): ").strip().lower()
        if resp in respuestas:
            resultado = jugar(respuestas[resp], base)
            if isinstance(resultado, dict):
                respuestas[resp] = resultado
                guardar_conocimiento(base)  # Guardamos inmediatamente
            return nodo
        else:
            print("Respuesta no valida. Usa 'si' o 'no'.")
            return jugar(nodo, base)

# --- PROGRAMA PRINCIPAL ---
def main():
    print("Bienvenido a 'Adivina Quien – Ganadores del Balon de Oro (1990-2025)'")
    print("Piensa en un ganador o ganadora del Balon de Oro y responde con 'si' o 'no'.")
    base = cargar_conocimiento()
    jugar(base, base)

if __name__ == "__main__":
    main()
