import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# --- Datos del juego ---
personajes = [
    {"nombre": "Alicia Torres", "profesion": "Chef profesional", "historia": "Estaba nerviosa mientras preparaba la cena, murmurando algo sobre una traicion."},
    {"nombre": "Bruno Diaz", "profesion": "Empresario hotelero", "historia": "Discutia por telefono sobre una inversion perdida. Su tono era furioso."},
    {"nombre": "Carmen Vega", "profesion": "Escritora de novelas", "historia": "Parecia tranquila, pero tomaba notas sobre los presentes. Decia que todo era material para su libro."},
    {"nombre": "Diego Luna", "profesion": "Musico", "historia": "Ensayaba una melodia triste en el piano. Sus ojos estaban rojos, como si hubiera llorado."},
    {"nombre": "Estela Rios", "profesion": "Investigadora privada", "historia": "Observaba a todos con atencion, tomando notas en su libreta."},
    {"nombre": "Juan", "profesion": "Victima inocente", "historia": "Se encontraba relajado en la mansion, sin sospechar que seria la victima del crimen."}
]

lugares = ["Cocina", "Estudio", "Biblioteca", "Jardin", "Habitacion principal"]
armas = ["Cuchillo", "Pistola", "Veneno", "Estatua", "Candelabro"]

historias_finales = [
    {"texto": "Un crimen impactante sucedio y la victima fue Juan."}
]

# --- Clase principal ---
class ClueGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Clue Interactivo")
        self.root.geometry("1000x700")
        self.pistas_restantes = 6
        self.boton_bg = "white"
        self.boton_fg = "black"
        self.bg_color = "#1a237e"  # fondo azul oscuro
        self.frame_inicio()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def frame_inicio(self):
        self.clear_window()
        self.root.config(bg=self.bg_color)
        tk.Label(self.root, text="CLUE INTERACTIVO", font=("Arial", 26, "bold"), bg=self.bg_color, fg="white").pack(pady=20)
        tk.Button(self.root, text="Jugar", font=("Arial", 16), width=15, bg=self.boton_bg, fg=self.boton_fg,
                  command=self.menu_caso).pack(pady=15)
        tk.Button(self.root, text="Salir", font=("Arial", 16), width=15, bg=self.boton_bg, fg=self.boton_fg,
                  command=self.root.quit).pack(pady=10)

    def menu_caso(self):
        self.clear_window()
        self.root.config(bg=self.bg_color)
        self.pistas_restantes = 6

        # Seleccion aleatoria del caso (culpable NO puede ser Juan)
        posibles_culpables = [p for p in personajes if p["nombre"] != "Juan"]
        self.culpable = random.choice(posibles_culpables)["nombre"]
        self.arma = random.choice(armas)
        self.lugar = random.choice(lugares)
        self.historia_final = historias_finales[0]

        tk.Label(self.root, text="Un crimen ha ocurrido...", font=("Arial", 20, "bold"), bg=self.bg_color, fg="white").pack(pady=10)
        texto_intro = (
            "Durante una tranquila tarde en la mansion, un crimen sacudio a todos los presentes.\n"
            "Tu mision es descubrir quien es el culpable, con que arma y en que lugar ocurrio el asesinato.\n\n"
            "Historias de cada personaje:"
        )
        tk.Label(self.root, text=texto_intro, wraplength=900, justify="left", bg=self.bg_color, fg="white").pack(pady=10)

        info = tk.Text(self.root, height=20, width=120, font=("Arial", 10), bg="white")
        info.pack(pady=10)
        info.insert(tk.END, "Historias de los personajes:\n")
        for p in personajes:
            info.insert(tk.END, f"\n- {p['nombre']} ({p['profesion']}): {p['historia']}\n")
        info.config(state="disabled")

        tk.Button(self.root, text="Comenzar investigacion", font=("Arial", 14), width=22, bg=self.boton_bg, fg=self.boton_fg,
                  command=self.iniciar_juego).pack(pady=15)
        tk.Button(self.root, text="Volver al inicio", font=("Arial", 12), bg=self.boton_bg, fg=self.boton_fg,
                  command=self.frame_inicio).pack(pady=5)

    def iniciar_juego(self):
        self.historia_personas = self.crear_historia_personas()
        self.historia_armas = self.crear_historia_armas()
        self.frame_juego()

    def crear_historia_personas(self):
        historias = {}
        for p in personajes:
            if p["nombre"] == self.culpable:
                historias[p["nombre"]] = f"Actuaba de manera sospechosa cerca del lugar del crimen."
            elif p["nombre"] == "Juan":
                historias[p["nombre"]] = p["historia"]
            else:
                historias[p["nombre"]] = p["historia"]
        return historias

    def crear_historia_armas(self):
        historia = {}
        for a in armas:
            if a == self.arma:
                historia[a] = "Mostraba signos de haber sido usado recientemente."
            else:
                historia[a] = "Parecia estar en su lugar, sin senales de uso."
        return historia

    def frame_juego(self):
        self.clear_window()
        self.root.config(bg=self.bg_color)
        tk.Label(self.root, text="Investigacion en curso", font=("Arial", 20, "bold"), bg=self.bg_color, fg="white").pack(pady=10)

        boton_frame = tk.Frame(self.root, bg=self.bg_color)
        boton_frame.pack(pady=5)
        tk.Button(boton_frame, text="Pista: Persona", font=("Arial", 12), width=18, bg=self.boton_bg, fg=self.boton_fg,
                  command=self.pista_persona).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(boton_frame, text="Pista: Arma", font=("Arial", 12), width=18, bg=self.boton_bg, fg=self.boton_fg,
                  command=self.pista_arma).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(boton_frame, text="Pista: Lugar", font=("Arial", 12), width=18, bg=self.boton_bg, fg=self.boton_fg,
                  command=self.pista_lugar).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(boton_frame, text="Hacer acusacion", font=("Arial", 14), width=20, bg=self.boton_bg, fg=self.boton_fg,
                  command=self.hacer_acusacion).grid(row=0, column=3, padx=5, pady=5)

        self.info_text = tk.Text(self.root, height=30, width=120, font=("Arial", 10), bg="white")
        self.info_text.pack(pady=10)

        self.historial = []
        self.actualizar_info("Selecciona una pista para comenzar tu investigacion.")

    def usar_pista(self):
        if self.pistas_restantes <= 0:
            messagebox.showwarning("Sin pistas", "Ya has usado las 6 pistas disponibles. Debes hacer tu acusacion.")
            return False
        self.pistas_restantes -= 1
        return True

    def actualizar_info(self, mensaje):
        self.historial.append(mensaje)
        texto = f"Pistas restantes: {self.pistas_restantes}\n\n"
        texto += "Sospechosos:\n" + "\n".join([p["nombre"] for p in personajes if p["nombre"] != "Juan"]) + "\n\n"
        texto += "Armas:\n" + "\n".join(armas) + "\n\n"
        texto += "Lugares:\n" + "\n".join(lugares) + "\n\n"
        texto += "Historial de pistas:\n"
        for item in self.historial:
            texto += f"- {item}\n"
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, texto)
        self.info_text.config(state="disabled")

    def pista_persona(self):
        if not self.usar_pista(): return
        nombre = simpledialog.askstring("Pista: Persona", "Escribe el nombre del personaje que deseas investigar:", parent=self.root)
        if nombre in self.historia_personas:
            self.actualizar_info(f"Pista Persona ({nombre}): {self.historia_personas[nombre]}")
        else:
            self.actualizar_info("Pista Persona: Nombre no valido.")

    def pista_arma(self):
        if not self.usar_pista(): return
        nombre = simpledialog.askstring("Pista: Arma", "Escribe el nombre del arma que deseas revisar:", parent=self.root)
        if nombre in self.historia_armas:
            self.actualizar_info(f"Pista Arma ({nombre}): {self.historia_armas[nombre]}")
        else:
            self.actualizar_info("Pista Arma: Arma no valida.")

    def pista_lugar(self):
        if not self.usar_pista(): return
        lugar = simpledialog.askstring("Pista: Lugar", "Escribe el lugar que deseas investigar:", parent=self.root)
        if lugar == self.lugar:
            self.actualizar_info(f"Pista Lugar ({lugar}): Se encontro algo sospechoso en este lugar.")
        else:
            self.actualizar_info(f"Pista Lugar ({lugar}): Este lugar parece estar en orden.")

    def hacer_acusacion(self):
        culpable = simpledialog.askstring("Acusacion", "¿Quien es el culpable?", parent=self.root)
        arma = simpledialog.askstring("Acusacion", "¿Que arma se uso?", parent=self.root)
        lugar = simpledialog.askstring("Acusacion", "¿Donde ocurrio el crimen?", parent=self.root)

        if (culpable == self.culpable) and (arma == self.arma) and (lugar == self.lugar):
            messagebox.showinfo("Resultado", f"¡Correcto! Has resuelto el caso.\n\n{self.historia_final['texto']}")
        else:
            messagebox.showerror("Incorrecto", f"Fallaste. El culpable era {self.culpable}, con el {self.arma} en el {self.lugar}.\n\n{self.historia_final['texto']}")

        self.frame_fin()

    def frame_fin(self):
        self.clear_window()
        tk.Label(self.root, text="Fin del juego", font=("Arial", 24, "bold"), bg=self.bg_color, fg="white").pack(pady=30)
        tk.Button(self.root, text="Jugar de nuevo", font=("Arial", 16), width=20, bg=self.boton_bg, fg=self.boton_fg,
                  command=self.menu_caso).pack(pady=15)
        tk.Button(self.root, text="Salir", font=("Arial", 16), width=20, bg=self.boton_bg, fg=self.boton_fg,
                  command=self.root.quit).pack(pady=15)

# --- Ejecutar la aplicacion ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ClueGame(root)
    root.mainloop()
