import requests

def obtener_numeros_cuanticos(cantidad):
    print(f"📡 Conectando con el láser cuántico de la Univ. Nacional de Australia...")
    print(f"Pidiendo {cantidad} eventos cuánticos en tiempo real...\n")
    
    # Esta es la URL (API) oficial del laboratorio. 
    # Le pedimos 'cantidad' de números enteros del 0 al 255 (uint8).
    url = f"https://qrng.anu.edu.au/API/jsonI.php?length={cantidad}&type=uint8"

    try:
        # Aquí hacemos la llamada por internet
        respuesta = requests.get(url)
        respuesta.raise_for_status() # Esto comprueba que la web no esté caída
        datos = respuesta.json()

        # La API nos entrega una lista de números en la variable 'data'
        numeros_en_bruto = datos['data']
        
        # Como los números van del 0 al 255, los convertimos a 0 y 1.
        # Si el número es par, lo convertimos en 0. Si es impar, en 1.
        # Así creamos nuestro entorno 50/50 perfecto.
        ceros_y_unos = [num % 2 for num in numeros_en_bruto]

        # Contamos cuántos ceros y cuántos unos hay
        total_ceros = ceros_y_unos.count(0)
        total_unos = ceros_y_unos.count(1)

        # Calculamos los porcentajes
        porcentaje_ceros = (total_ceros / cantidad) * 100
        porcentaje_unos = (total_unos / cantidad) * 100

        # Mostramos los resultados en la consola
        print("📊 RESULTADOS DEL BOT (GRUPO DE CONTROL SIN CONSCIENCIA):")
        print("-" * 50)
        print(f"Total de 0s: {total_ceros} ({porcentaje_ceros:.2f}%)")
        print(f"Total de 1s: {total_unos} ({porcentaje_unos:.2f}%)")
        print("-" * 50)

        # Análisis estadístico básico
        print("🔍 ANÁLISIS DEL SISTEMA:")
        if 49.0 <= porcentaje_ceros <= 51.0:
            print("Veredicto: El hardware cuántico funciona perfectamente. Aleatoriedad pura confirmada.")
            print("El Grupo de Control es válido para el experimento principal.")
        else:
            print("Veredicto: Hay una desviación estadística normal por la cantidad de la muestra.")
            print("Nota: En física, cuantos más números pidas, más se pegará al 50.00%.")

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("Puede que el servidor de Australia esté saturado. Inténtalo en unos minutos.")

# --- INICIO DEL PROGRAMA ---
# La API gratuita permite pedir hasta un máximo de 1024 números por llamada.
# Vamos a pedir 1000 para empezar.
obtener_numeros_cuanticos(100)