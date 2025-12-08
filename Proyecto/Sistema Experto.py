import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk # Necesario para el fondo
import os

# ============================
# CONFIGURACIÓN DE ARCHIVOS
# ============================
ARCHIVO_REGLAS = "politicas_banco.xlsx"
ARCHIVO_CLIENTES = "clientes_activos.xlsx"
IMAGEN_FONDO = "fondo_banco.jpg" # Nombre de tu imagen

# 1. Cargar Reglas
try:
    df_reglas = pd.read_excel(ARCHIVO_REGLAS, engine="openpyxl")
    df_reglas.columns = df_reglas.columns.str.lower().str.strip()
    df_reglas["historial_crediticio"] = df_reglas["historial_crediticio"].str.lower().str.strip()
    df_reglas["situacion_laboral"] = df_reglas["situacion_laboral"].str.lower().str.strip()
except Exception as e:
    messagebox.showerror("Error Crítico", f"No se encontró el archivo de reglas: {e}")
    exit()

# 2. Inicializar Base de Clientes
if not os.path.exists(ARCHIVO_CLIENTES):
    columnas = ["nombre", "telefono", "direccion", "deuda_total", "nombre_aval", "telefono_aval"]
    df_vacio = pd.DataFrame(columns=columnas)
    try:
        df_vacio.to_excel(ARCHIVO_CLIENTES, index=False, engine="openpyxl")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el archivo de clientes: {e}")

# ============================
# FUNCIONES DE LIMPIEZA
# ============================
def limpiar_interfaz():
    entry_ingresos.delete(0, tk.END)
    entry_monto.delete(0, tk.END)
    combo_plazo.current(0)
    combo_laboral.set('')
    combo_pagos.set('')
    combo_deudas.set('')
    combo_tarjeta.set('')
    entry_ingresos.focus()

# ============================
# FASE 3: REGISTRO FINAL
# ============================
def gestionar_cliente_aprobado(monto_nuevo, requiere_aval):
    ventana_datos = tk.Toplevel()
    ventana_datos.title("Formalización de Crédito")
    
    alto = 550 if requiere_aval else 350
    ventana_datos.geometry(f"450x{alto}")
    
    titulo = "¡CRÉDITO PRE-APROBADO CON AVAL!" if requiere_aval else "¡CRÉDITO APROBADO!"
    color = "#d39e00" if requiere_aval else "green"
    
    tk.Label(ventana_datos, text=titulo, fg=color, font=("Arial", 12, "bold")).pack(pady=10)

    # Cliente
    frame_cliente = tk.LabelFrame(ventana_datos, text="Datos del Solicitante", padx=10, pady=10)
    frame_cliente.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_cliente, text="Nombre Completo:").pack(anchor="w")
    entry_nombre = tk.Entry(frame_cliente, width=40)
    entry_nombre.pack(fill="x")
    tk.Label(frame_cliente, text="Teléfono:").pack(anchor="w")
    entry_tel = tk.Entry(frame_cliente, width=40)
    entry_tel.pack(fill="x")
    tk.Label(frame_cliente, text="Dirección:").pack(anchor="w")
    entry_dir = tk.Entry(frame_cliente, width=40)
    entry_dir.pack(fill="x")

    # Aval
    entry_nombre_aval = None
    entry_tel_aval = None

    if requiere_aval:
        frame_aval = tk.LabelFrame(ventana_datos, text="Datos del Aval / Fiador", padx=10, pady=10, fg="red")
        frame_aval.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_aval, text="Nombre del Aval:").pack(anchor="w")
        entry_nombre_aval = tk.Entry(frame_aval, width=40)
        entry_nombre_aval.pack(fill="x")
        tk.Label(frame_aval, text="Teléfono del Aval:").pack(anchor="w")
        entry_tel_aval = tk.Entry(frame_aval, width=40)
        entry_tel_aval.pack(fill="x")

    def guardar_registro():
        nombre = entry_nombre.get().strip().upper()
        telefono = entry_tel.get().strip()
        direccion = entry_dir.get().strip()
        nom_aval_txt = "N/A"
        tel_aval_txt = "N/A"

        if requiere_aval:
            nom_aval_txt = entry_nombre_aval.get().strip().upper()
            tel_aval_txt = entry_tel_aval.get().strip()
            if not nom_aval_txt or not tel_aval_txt:
                messagebox.showwarning("Faltan Datos", "Datos del AVAL son obligatorios.")
                return

        if not nombre or not telefono:
            messagebox.showwarning("Error", "Nombre y Teléfono son obligatorios.")
            return

        try:
            df_clientes = pd.read_excel(ARCHIVO_CLIENTES, engine="openpyxl")
        except:
            columnas = ["nombre", "telefono", "direccion", "deuda_total", "nombre_aval", "telefono_aval"]
            df_clientes = pd.DataFrame(columns=columnas)

        cliente_existente = df_clientes[df_clientes["nombre"] == nombre]
        guardado_exitoso = False

        if not cliente_existente.empty:
            deuda_actual = float(cliente_existente.iloc[0]["deuda_total"])
            if messagebox.askyesno("Cliente Recurrente", f"Cliente existe. Deuda: ${deuda_actual}\n¿Sumar nuevo monto?"):
                df_clientes.loc[df_clientes["nombre"] == nombre, "deuda_total"] = deuda_actual + monto_nuevo
                guardado_exitoso = True
                mensaje_final = f"Actualizado. Total: ${deuda_actual + monto_nuevo}"
        else:
            nuevo_registro = pd.DataFrame([{
                "nombre": nombre, "telefono": telefono, "direccion": direccion, 
                "deuda_total": monto_nuevo, "nombre_aval": nom_aval_txt, "telefono_aval": tel_aval_txt
            }])
            df_clientes = pd.concat([df_clientes, nuevo_registro], ignore_index=True)
            guardado_exitoso = True
            mensaje_final = "Cliente registrado exitosamente."

        if guardado_exitoso:
            try:
                df_clientes.to_excel(ARCHIVO_CLIENTES, index=False, engine="openpyxl")
                messagebox.showinfo("Éxito", mensaje_final)
                ventana_datos.destroy()
                limpiar_interfaz()
            except PermissionError:
                messagebox.showerror("Error", "Cierra el Excel antes de guardar.")

    tk.Button(ventana_datos, text="Guardar Registro", command=guardar_registro, bg="#007bff", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

# ============================
# FASE 2: REVISIÓN MANUAL
# ============================
def gestionar_revision_manual(monto):
    ventana_manual = tk.Toplevel()
    ventana_manual.title("Investigación de Riesgo Adicional")
    ventana_manual.geometry("400x400")
    ventana_manual.config(bg="#f8f9fa")

    tk.Label(ventana_manual, text="CASO BAJO REVISIÓN", fg="#dc3545", bg="#f8f9fa", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(ventana_manual, text="El sistema requiere más información.\nPor favor conteste:", bg="#f8f9fa").pack(pady=5)

    tk.Label(ventana_manual, text="1. ¿Tipo de Vivienda?", bg="#f8f9fa", font=("bold")).pack(pady=(10,0))
    combo_vivienda = ttk.Combobox(ventana_manual, values=["Propia (Pagada)", "Propia (Hipoteca)", "Rentada", "Familiar"], state="readonly")
    combo_vivienda.pack()

    tk.Label(ventana_manual, text="2. Antigüedad en su trabajo actual:", bg="#f8f9fa", font=("bold")).pack(pady=(10,0))
    combo_antiguedad = ttk.Combobox(ventana_manual, values=["Menos de 1 año", "1 a 3 años", "Más de 3 años"], state="readonly")
    combo_antiguedad.pack()

    tk.Label(ventana_manual, text="3. Número de personas dependientes:", bg="#f8f9fa", font=("bold")).pack(pady=(10,0))
    combo_dependientes = ttk.Combobox(ventana_manual, values=["Ninguna", "1 a 2", "3 o más"], state="readonly")
    combo_dependientes.pack()

    def evaluar_desempate():
        vivienda = combo_vivienda.get()
        antiguedad = combo_antiguedad.get()
        dependientes = combo_dependientes.get()

        if not vivienda or not antiguedad or not dependientes:
            messagebox.showwarning("Alerta", "Debe responder todas las preguntas extra.")
            return

        puntos = 0
        if "Propia" in vivienda: puntos += 2
        elif "Familiar" in vivienda: puntos += 1
        
        if "Más de 3" in antiguedad: puntos += 2
        elif "1 a 3" in antiguedad: puntos += 1
        
        if dependientes == "Ninguna": puntos += 1
        elif dependientes == "3 o más": puntos -= 1

        ventana_manual.destroy()
        
        if puntos >= 3:
            messagebox.showinfo("Resolución", "CONCLUSIÓN: APROBADO (Riesgo Controlado)")
            gestionar_cliente_aprobado(monto, requiere_aval=False)
        else:
            messagebox.showerror("Resolución", "CONCLUSIÓN: RECHAZADO DEFINITIVO")
            limpiar_interfaz()

    tk.Button(ventana_manual, text="EVALUAR RESPUESTAS", command=evaluar_desempate, bg="#ffc107", fg="black", font=("bold")).pack(pady=30)


# ============================
# FASE 1: MOTOR PRINCIPAL
# ============================
def inferir_historial(pagos_tardios, deudas_activas, tiene_tarjetas):
    if pagos_tardios == "sí": return "malo"
    if tiene_tarjetas == "no" and deudas_activas == "no": return "sin historial"
    if deudas_activas == "sí" and pagos_tardios == "no": return "regular"
    if tiene_tarjetas == "sí" and deudas_activas == "no" and pagos_tardios == "no": return "bueno"
    return "regular"

def motor_de_inferencia():
    try:
        if not entry_ingresos.get() or not entry_monto.get():
             messagebox.showwarning("Alerta", "Faltan datos numéricos.")
             return
        
        laboral = combo_laboral.get().lower().strip()
        resp_pagos = combo_pagos.get().lower()
        
        if not laboral or not resp_pagos:
            messagebox.showwarning("Alerta", "Faltan seleccionar opciones.")
            return

        ingresos = float(entry_ingresos.get())
        monto = float(entry_monto.get())
        plazo = int(combo_plazo.get())
        
        historial_inferido = inferir_historial(resp_pagos, combo_deudas.get().lower(), combo_tarjeta.get().lower())
        cuota = monto / plazo
        max_capacidad = ingresos * 0.35
        es_solvente = cuota <= max_capacidad

        regla = df_reglas[
            (df_reglas["historial_crediticio"] == historial_inferido) &
            (df_reglas["situacion_laboral"] == laboral)
        ]

        if not es_solvente:
            messagebox.showerror("Rechazado", f"Capacidad insuficiente.\nCuota: ${cuota:.2f} > Máx: ${max_capacidad:.2f}")
            limpiar_interfaz()
            return
            
        if regla.empty:
            accion_str = "REVISION MANUAL"
            riesgo = "Desconocido"
        else:
            accion_str = str(regla.iloc[0]["accion_recomendada"]).upper()
            riesgo = regla.iloc[0]["nivel_riesgo"]
        
        if "REVISION" in accion_str or "MANUAL" in accion_str:
            messagebox.showwarning("Atención", f"Perfil {historial_inferido} requiere INVESTIGACIÓN ADICIONAL.")
            gestionar_revision_manual(monto)
            
        elif "APROBAR" in accion_str:
            messagebox.showinfo("Éxito", f"Crédito APROBADO Directamente.\nRiesgo: {riesgo}")
            gestionar_cliente_aprobado(monto, requiere_aval=False)
            
        elif "AVAL" in accion_str:
            messagebox.showwarning("Condicionado", f"Crédito PRE-APROBADO.\nSe requiere AVAL por riesgo {riesgo}.")
            gestionar_cliente_aprobado(monto, requiere_aval=True)
            
        else:
            messagebox.showerror("Denegado", f"Solicitud RECHAZADA.\nRiesgo: {riesgo}")
            limpiar_interfaz()

    except ValueError:
        messagebox.showerror("Error", "Datos numéricos inválidos.")

# ============================
# INTERFAZ PRINCIPAL (CON FONDO)
# ============================
ventana = tk.Tk()
ventana.title("Sistema Experto Bancario - Enterprise AI")
# Hacemos la ventana un poco más grande para que luzca el fondo
ventana.geometry("600x750") 
# Color de respaldo por si falla la imagen
ventana.config(bg="#2c3e50") 

# --- CARGAR IMAGEN DE FONDO ---
try:
    # Cargar la imagen con Pillow
    pil_image = Image.open(IMAGEN_FONDO)
    # Redimensionarla al tamaño de la ventana (opcional, pero recomendado)
    pil_image = pil_image.resize((600, 750), Image.Resampling.LANCZOS)
    # Convertir a formato Tkinter
    bg_image_tk = ImageTk.PhotoImage(pil_image)
    
    # Crear un Label que contendrá la imagen y ocupará todo el fondo
    bg_label = tk.Label(ventana, image=bg_image_tk)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # ¡IMPORTANTE! Guardar una referencia para que no se borre de memoria
    bg_label.image = bg_image_tk
    print("Imagen de fondo cargada correctamente.")

except Exception as e:
    print(f"No se pudo cargar la imagen de fondo: {e}")
    # Si falla, no pasa nada, se verá el color de fondo configurado arriba

# --- TÍTULO PRINCIPAL (Con fondo transparente visualmente) ---
# Usamos un Frame pequeño para el título para darle un estilo de "etiqueta"
title_frame = tk.Frame(ventana, bg="#003366", bd=2, relief="ridge")
title_frame.pack(pady=20, ipadx=10, ipady=5)
tk.Label(title_frame, text="Sistema de Créditos Inteligente", font=("Arial", 16, "bold"), bg="#003366", fg="white").pack()

# --- CONTENEDOR PRINCIPAL (El recuadro blanco) ---
# Aumentamos el padding (padx, pady) externo para que se vea más fondo alrededor
frame = tk.Frame(ventana, bg="white", bd=3, relief="raised")
frame.pack(padx=40, pady=20, fill="both", expand=True)

# Sección Financiera
tk.Label(frame, text="-- Datos Económicos --", font=("Arial", 11, "bold"), bg="white", fg="#0056b3").pack(pady=(15,5))
tk.Label(frame, text="Ingresos Mensuales ($):", bg="white", font=("Arial", 9)).pack()
entry_ingresos = tk.Entry(frame, width=25, bd=2)
entry_ingresos.pack(pady=2)
tk.Label(frame, text="Monto a solicitar ($):", bg="white", font=("Arial", 9)).pack()
entry_monto = tk.Entry(frame, width=25, bd=2)
entry_monto.pack(pady=2)
tk.Label(frame, text="Plazo (meses):", bg="white", font=("Arial", 9)).pack()
combo_plazo = ttk.Combobox(frame, values=["12", "24", "36", "48"], state="readonly", width=22)
combo_plazo.current(0)
combo_plazo.pack(pady=2)

# Sección Perfil
tk.Label(frame, text="-- Perfil de Riesgo --", font=("Arial", 11, "bold"), bg="white", fg="#0056b3").pack(pady=(20,5))
tk.Label(frame, text="Situación Laboral:", bg="white", font=("Arial", 9)).pack()
combo_laboral = ttk.Combobox(frame, values=["Estable", "Independiente"], state="readonly", width=28)
combo_laboral.pack(pady=2)

tk.Label(frame, text="¿Pagos tarde recientes?", bg="white", font=("Arial", 9)).pack(pady=(5,0))
combo_pagos = ttk.Combobox(frame, values=["Sí", "No"], state="readonly", width=15)
combo_pagos.pack(pady=2)
tk.Label(frame, text="¿Deudas activas?", bg="white", font=("Arial", 9)).pack(pady=(5,0))
combo_deudas = ttk.Combobox(frame, values=["Sí", "No"], state="readonly", width=15)
combo_deudas.pack(pady=2)
tk.Label(frame, text="¿Maneja tarjeta de crédito?", bg="white", font=("Arial", 9)).pack(pady=(5,0))
combo_tarjeta = ttk.Combobox(frame, values=["Sí", "No"], state="readonly", width=15)
combo_tarjeta.pack(pady=2)

# Botones (Dentro del frame blanco para que se vean limpios)
frame_botones = tk.Frame(frame, bg="white")
frame_botones.pack(pady=30)

btn_procesar = tk.Button(frame_botones, text="ANALIZAR CON IA", command=motor_de_inferencia, 
                         bg="#28a745", fg="white", font=("Arial", 10, "bold"), height=2, width=18, cursor="hand2")
btn_procesar.grid(row=0, column=0, padx=10)

btn_salir = tk.Button(frame_botones, text="SALIR", command=ventana.destroy, 
                      bg="#dc3545", fg="white", font=("Arial", 10, "bold"), height=2, width=10, cursor="hand2")
btn_salir.grid(row=0, column=1, padx=10)

ventana.mainloop()