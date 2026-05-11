import tkinter as tk
from tkinter import messagebox
import requests
import threading
import csv
from datetime import datetime
import os
import time  # <-- NUEVO: Para poder hacer pausas

ARCHIVO_DATOS = "resultados_experimento.csv"

if not os.path.exists(ARCHIVO_DATOS):
    with open(ARCHIVO_DATOS, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha_Hora", "Total_0s", "Total_1s", "Porcentaje_0s", "Porcentaje_1s", "Objetivo_Foco"])

def realizar_medicion():
    lbl_estado.config(text="📡 Conectando con Australia... Mantén tu foco en el 1...", fg="blue")
    lbl_resultado.config(text="")
    btn_iniciar.config(state="disabled") 
    
    def llamada_cuantica():
        cantidad = 100
        url = f"https://qrng.anu.edu.au/API/jsonI.php?length={cantidad}&type=uint8"
        
        max_intentos = 5  # <-- NUEVO: Vamos a ser persistentes
        
        for intento in range(max_intentos):
            try:
                # 1. Intentamos pedir los datos
                respuesta = requests.get(url, timeout=10)
                respuesta.raise_for_status()
                datos = respuesta.json()
                
                # 2. Si llegamos aquí, no hubo error 500. ¡Procesamos los datos!
                ceros_y_unos = [num % 2 for num in datos['data']]
                total_ceros = ceros_y_unos.count(0)
                total_unos = ceros_y_unos.count(1)
                
                porcentaje_ceros = (total_ceros / cantidad) * 100
                porcentaje_unos = (total_unos / cantidad) * 100
                
                ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open(ARCHIVO_DATOS, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([ahora, total_ceros, total_unos, round(porcentaje_ceros, 2), round(porcentaje_unos, 2), 1])
                
                resultado_texto = (
                    f"Total de 0s: {total_ceros} ({porcentaje_ceros:.2f}%)\n"
                    f"Total de 1s: {total_unos} ({porcentaje_unos:.2f}%)"
                )
                
                lbl_resultado.config(text=resultado_texto, fg="black")
                lbl_estado.config(text="✅ Medición guardada en la base de datos", fg="green")
                
                break  # <-- ÉXITO TOTAL: Rompemos el bucle para que no siga intentándolo
                
            except Exception as e:
                # 3. Si hubo un error (el servidor se cayó), entra aquí
                if intento < max_intentos - 1:
                    # Avisamos en pantalla y esperamos 2 segundos
                    lbl_estado.config(text=f"⚠️ Servidor saturado. Reintentando ({intento+1}/{max_intentos})...", fg="orange")
                    time.sleep(2)
                else:
                    # Si ya falló 5 veces seguidas, entonces sí mostramos el cartel de error
                    lbl_estado.config(text="❌ Error de conexión crítico", fg="red")
                    messagebox.showerror("Error de Red", "El laboratorio australiano está colapsado ahora mismo. Espera unos minutos.")
            
        # Al final de todo (haya funcionado o no), volvemos a activar el botón
        btn_iniciar.config(state="normal")

    hilo = threading.Thread(target=llamada_cuantica)
    hilo.start()

# --- CONFIGURACIÓN DE LA VENTANA VISUAL ---
ventana = tk.Tk()
ventana.title("Experimento DHS - Foco Explorador")
ventana.geometry("450x350")
ventana.configure(bg="#f0f4f8") 

instrucciones = (
    "👁️ Foco Explorador Activo 👁️\n\n"
    "Concéntrate intensamente en el número 1.\n"
    "Visualiza que el universo colapsa en ese estado."
)
lbl_instrucciones = tk.Label(ventana, text=instrucciones, font=("Helvetica", 12, "bold"), bg="#f0f4f8")
lbl_instrucciones.pack(pady=20)

btn_iniciar = tk.Button(ventana, text="INICIAR MEDICIÓN", font=("Arial", 14, "bold"), 
                        bg="#2c3e50", fg="white", cursor="hand2", command=realizar_medicion)
btn_iniciar.pack(pady=10)

lbl_estado = tk.Label(ventana, text="Esperando al operador...", font=("Arial", 10, "italic"), bg="#f0f4f8", fg="gray")
lbl_estado.pack(pady=10)

lbl_resultado = tk.Label(ventana, text="", font=("Consolas", 14, "bold"), bg="#f0f4f8")
lbl_resultado.pack(pady=20)

ventana.mainloop()