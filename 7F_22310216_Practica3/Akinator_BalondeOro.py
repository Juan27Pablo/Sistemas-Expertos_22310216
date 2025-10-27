import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # Pillow para imágenes

DB_FILE = "balon_oro.json"

# --- FUNCIONES DE BASE DE CONOCIMIENTO ---
def cargar_conocimiento():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Base inicial (puedes usar tu árbol final corregido)
        return {
    "Es hombre?": {
        "si": {
            "Es sudamericano?": {
                "si": {
                    "Jugo en el Real Madrid?": {
                        "si": {
                            "Jugo en el AC Milan?": {
                                "si": "Kaka",
                                "no": "Ronaldo Nazario"
                            }
                        },
                        "no": {
                            "Es Argentino?": {
                                "si": "Lionel Messi",
                                "no": {
                                    "Jugo en el PSG?": {
                                        "si": "Ronaldinho",
                                        "no": "Rivaldo"
                                    }
                                }
                            }
                        }
                    }
                },
                "no": {
                    "Jugo en el Real Madrid?": {
                        "si": {
                            "Es ingles?": {
                                "si": "Michael Owen",
                                "no": {
                                    "Jugo tambien en la Serie A?": {
                                        "si": {
                                            "Es Italiano?": {
                                                "si": "Fabio Cannavaro",
                                                "no": "Luka Modric"
                                            }
                                        },
                                        "no": {
                                            "Es portugues?": {
                                                "si": {
                                                    "Jugo en el FC Barcelona?": {
                                                        "si": "Luis Figo",
                                                        "no": "Cristiano Ronaldo"
                                                    }
                                                },
                                                "no": {
                                                    "Jugo en Arabia?": {
                                                        "si": "Karim Benzema",
                                                        "no": "Zinedine Zidane"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "no": {
                            "Jugo en la Serie A?": {
                                "si": {
                                    "Es jugador del Milan?": {
                                        "si": {
                                            "Es de Paises Bajos?": {
                                                "si": {
                                                    "Llevaba el dorsal No. 9?": {
                                                        "si": "Marco Van Basten",
                                                        "no": "Ruud Gullit"
                                                    }
                                                }
                                            }
                                        },
                                        "no": {
                                            "Jugo en el Bayern Munich?": {
                                                "si": {
                                                    "Es aleman?": {
                                                        "si": "Lothar Matthaus",
                                                        "no": "Jean-Pierre Papin"
                                                    }
                                                },
                                                "no": {
                                                    "Jugo en la Juventus?": {
                                                        "si": {
                                                            "Es frances?": {
                                                                "si": "Michael Platini",
                                                                "no": "Roberto Baggio"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "no": {
                                    "Jugo en el FC Barcelona?": {
                                        "si": {
                                            "Es frances?": {
                                                "si": "Ousmane Dembele",
                                                "no": "Johan Cruyff"
                                            }
                                        },
                                        "no": "Rodri"
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


# --- CLASE PRINCIPAL DEL JUEGO ---
class AdivinaBalonOro:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivina Quién – Balón de Oro")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Canvas para fondo
        self.canvas = tk.Canvas(self.root, width=600, height=500)
        self.canvas.pack(fill="both", expand=True)

        # Imagen de fondo
        try:
            img = Image.open("Imagenes akinator/balon_oro.jpg")
            img = img.resize((600, 500))
            self.fondo_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.fondo_img, anchor="nw")
        except:
            messagebox.showwarning("Imagen", "Imagen de inicio no disponible")

        # Variables del juego
        self.base = cargar_conocimiento()
        self.nodo_actual = None
        self.historial = []

        self.mostrar_menu_principal()

    # --- Menú principal ---
    def mostrar_menu_principal(self):
        # Limpiar botones y textos anteriores
        self.limpiar_canvas()

        tk.Label(self.canvas, text="⚽ Adivina Quién – Balón de Oro ⚽",
                 font=("Arial", 18, "bold"), bg="#ffffff").place(x=120, y=30)

        btn_jugar = tk.Button(self.canvas, text="Jugar", font=("Arial", 14), width=15,
                              command=self.iniciar_juego)
        btn_salir = tk.Button(self.canvas, text="Salir", font=("Arial", 14), width=15,
                              command=self.root.quit)
        self.canvas.create_window(300, 200, window=btn_jugar)
        self.canvas.create_window(300, 260, window=btn_salir)

    # --- Iniciar juego ---
    def iniciar_juego(self):
        self.base = cargar_conocimiento()
        self.nodo_actual = self.base
        self.historial = []
        self.mostrar_pregunta(self.nodo_actual)

    # --- Mostrar pregunta o personaje ---
    def mostrar_pregunta(self, nodo):
        self.limpiar_canvas()
        if isinstance(nodo, str):
            tk.Label(self.canvas, text=f"¿Es {nodo}?", font=("Arial", 15), bg="#ffffff").place(x=200, y=150)
            btn_si = tk.Button(self.canvas, text="Sí", font=("Arial", 12), width=10,
                               command=lambda: self.mostrar_imagen_personaje(nodo))
            btn_no = tk.Button(self.canvas, text="No", font=("Arial", 12), width=10,
                               command=lambda: self.aprender_nuevo(nodo))
            self.canvas.create_window(200, 200, window=btn_si)
            self.canvas.create_window(400, 200, window=btn_no)
            return

        pregunta = list(nodo.keys())[0]
        tk.Label(self.canvas, text=pregunta, font=("Arial", 15, "bold"), wraplength=500, bg="#ffffff").place(x=50, y=100)
        btn_si = tk.Button(self.canvas, text="Sí", font=("Arial", 12), width=10,
                           command=lambda: self.procesar_respuesta(nodo, "si"))
        btn_no = tk.Button(self.canvas, text="No", font=("Arial", 12), width=10,
                           command=lambda: self.procesar_respuesta(nodo, "no"))
        self.canvas.create_window(200, 200, window=btn_si)
        self.canvas.create_window(400, 200, window=btn_no)

    # --- Procesar respuestas ---
    def procesar_respuesta(self, nodo, respuesta):
        pregunta = list(nodo.keys())[0]
        if respuesta in nodo[pregunta]:
            self.historial.append((nodo, respuesta))
            self.mostrar_pregunta(nodo[pregunta][respuesta])
        else:
            messagebox.showinfo("Error", "Respuesta no válida.")

    # --- Mostrar imagen del personaje ---
    def mostrar_imagen_personaje(self, personaje):
        self.limpiar_canvas()
        try:
            img = Image.open(f"Imagenes akinator/{personaje.replace(' ', '_')}.jpg")
            img = img.resize((400, 300))
            self.personaje_img = ImageTk.PhotoImage(img)
            tk.Label(self.canvas, image=self.personaje_img, bg="#ffffff").place(x=100, y=50)
        except:
            tk.Label(self.canvas, text="Imagen no disponible", bg="#ffffff").place(x=200, y=150)

        tk.Label(self.canvas, text=f"¡Adiviné! Es {personaje}", font=("Arial", 16, "bold"), bg="#ffffff").place(x=180, y=370)
        btn_jugar = tk.Button(self.canvas, text="Jugar otra vez", font=("Arial", 12), width=15,
                              command=self.iniciar_juego)
        btn_salir = tk.Button(self.canvas, text="Salir", font=("Arial", 12), width=15,
                              command=self.root.quit)
        self.canvas.create_window(200, 420, window=btn_jugar)
        self.canvas.create_window(400, 420, window=btn_salir)

    # --- Aprender un nuevo personaje ---
    def aprender_nuevo(self, personaje_erroneo):
        correcto = simpledialog.askstring("Aprender", "¿Quién era el personaje correcto?")
        if not correcto:
            self.fin_juego()
            return

        nueva_pregunta = simpledialog.askstring(
            "Aprender", f"Dame una pregunta que distinga a {correcto} de {personaje_erroneo}:")
        if not nueva_pregunta:
            self.fin_juego()
            return

        resp_correcta = simpledialog.askstring(
            "Aprender", f"Para {correcto}, la respuesta sería 'si' o 'no'?").lower().strip()
        if resp_correcta not in ["si", "no"]:
            messagebox.showwarning("Advertencia", "Respuesta inválida. No se guardaron cambios.")
            self.fin_juego()
            return

        nuevo_nodo = {
            nueva_pregunta: {
                resp_correcta: correcto,
                "no" if resp_correcta == "si" else "si": personaje_erroneo
            }
        }

        if self.historial:
            nodo_padre, resp = self.historial[-1]
            pregunta_padre = list(nodo_padre.keys())[0]
            nodo_padre[pregunta_padre][resp] = nuevo_nodo
        else:
            self.base = nuevo_nodo

        guardar_conocimiento(self.base)
        messagebox.showinfo("Aprendido", f"He aprendido sobre {correcto}. ¡Gracias! 🧠")
        self.fin_juego()

    # --- Final del juego ---
    def fin_juego(self):
        self.limpiar_canvas()
        tk.Label(self.canvas, text="¿Quieres jugar otra vez?", font=("Arial", 14), bg="#ffffff").place(x=180, y=200)
        btn_si = tk.Button(self.canvas, text="Sí", font=("Arial", 12), width=15, command=self.iniciar_juego)
        btn_no = tk.Button(self.canvas, text="Salir", font=("Arial", 12), width=15, command=self.root.quit)
        self.canvas.create_window(200, 250, window=btn_si)
        self.canvas.create_window(400, 250, window=btn_no)

    # --- Limpiar canvas de widgets ---
    def limpiar_canvas(self):
        # Elimina solo los widgets del canvas, dejando la imagen de fondo intacta
        for widget in self.canvas.winfo_children():
            widget.destroy()


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AdivinaBalonOro(root)
    root.mainloop()
