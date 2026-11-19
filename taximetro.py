import time
import logging
import json
from pathlib import Path
import csv
from datetime import datetime

# Rutas del proyecto
CARPETA = Path(__file__).parent
CONFIG = CARPETA / "config.json"
LOG = CARPETA / "taximetro.log"
HISTORIAL = CARPETA / "historial.csv"

# Tarifas de respaldo
TARIFAS_POR_DEFECTO= {
  "tarifa_parado": 0.02,
  "tarifa_movimiento": 0.05
    }

# Crear el logger: fuera de las funciones -> Obtener el objeto que registra los mensajes
log = logging.getLogger("taximetro")


estado_inicial = "parado"


AYUDA = ("\nTaxímetro digital\n"
                 "i  iniciar carrera (empieza PARADO)\n"
                 "p  el taxi está parado\n"
                 "m  el taxi está en movimiento\n"
                 "f  finalizar la carrera y ver el total\n"
                 "h historial de carreras de hoy\n"
                 "a  ver esta ayuda\n"
                 "s  salir\n")





# Funciones auxiliares

# Definir la función de configuración: fuera de main
def configurar_log():
    logging.basicConfig( # 	Configurar dónde y cómo se registra el log
        filename="taximetro.log", # El nombre del archivo donde se guardarán los registros
        level=logging.INFO, # registra los mensajes INFO y todos los niveles más graves
        encoding="utf-8",
        format="%(asctime)s - %(levelname)s - %(message)s", # Fecha y hora | Nivel de gravedad | Contenido del mensaje
        )

def cargar_tarifas(ruta=CONFIG):
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8")) # json.loass: interpreta ese texto y lo convierte en un objeto de Python | ruta.read_text() lee el contenido del archivo como texto.
        # datos ahora es un diccionario con el contenido del json

        tarifas_json = {
            "tarifa_parado": float(datos["tarifa_parado"]),
            "tarifa_movimiento": float(datos["tarifa_movimiento"])
        }

        log.info("Tarifas cargadas de %s: %s", ruta, tarifas_json)
        return tarifas_json # el diccionario cargado, no tiene un nombre. Éste se asigna en el main cuando llamamos a esta funcion.

    except (OSError, ValueError, KeyError) as error:
        log.warning(
            "No se pudo leer %s (%s); uso tarifas por defecto",
            ruta,
            error
        )
        return dict(TARIFAS_POR_DEFECTO) #Devolvemos una copia para proteger el diccionario original
        # el diccionario cargado, no tiene un nombre. Éste se asigna en el main cuando llamamos a esta funcion.

def guardar_carrera(inicio, duracion, importe, ruta=HISTORIAL): # Responsabilidad: guardar una carrera en el CSV
    existe = ruta.exists()

    with open(ruta, "a", newline="", encoding="utf-8") as fichero:
        escritor = csv.writer(fichero)

        if not existe:
            escritor.writerow(["fecha", "hora", "duracion_s", "importe"])

        escritor.writerow([
            inicio.strftime("%Y-%m-%d"),
            inicio.strftime("%H:%M:%S"),
            round(duracion),
            f"{importe:.2f}"
        ])

def carreras_de_hoy(ruta=HISTORIAL):
    if not ruta.exists():
        return []

    hoy = datetime.now().strftime("%Y-%m-%d")
    carreras = []

    with open(ruta, "r", newline="", encoding="utf-8") as fichero:
        lector = csv.DictReader(fichero) #DictReader utiliza la primera fila del CSV como claves de los diccionarios.

        for fila in lector:
            if fila["fecha"] == hoy:
                carreras.append(fila)

    return carreras


def importe_tramo(segundos, estado, tarifas):
    if segundos < 0:
        raise ValueError("Los segundos no pueden ser negativos")
    if estado == "parado":
        precio = tarifas["tarifa_parado"]
    elif estado == "en movimiento":
        precio = tarifas["tarifa_movimiento"]
    else:
        precio = 0.0
    return segundos * precio
    

def cerrar_tramo(carrera, tarifas):
    hasta = time.monotonic()
    tramo = hasta - carrera["ultimo_tramo"]
    carrera["importe"] += importe_tramo(
        tramo,
        carrera["estado"],
        tarifas)
    carrera["ultimo_tramo"] = hasta
    return carrera

def calcular_duracion(carrera):
    duracion_total = time.monotonic() - carrera["inicio_mono"]
    return duracion_total



# Función principal
def main():
     #Ejecutar la configuración del logger al inicio de main
     configurar_log()
     log.info("Arranque del taxímetro")

     tarifas = cargar_tarifas()
     carrera = None
     print(AYUDA)
     
     while True:
        instruccion = input("Introduce una letra: \n" \
             "> ").strip().lower()
        if instruccion == "s":
            if carrera is not None:
                print("Hay una carrera en curso. Finalizala con 'f' antes de salir.\n")
                continue #vuelve al inicio del bucle
            break
        elif instruccion == "a":
            print(AYUDA)

        elif instruccion == "h":
            historial_hoy= carreras_de_hoy()
            if historial_hoy:
                total_dia = 0.0
                for i in historial_hoy:
                    hora = i["hora"]
                    duracion = int(i["duracion_s"])
                    importe = float(i["importe"])
                    total_dia += importe

                    print(
                        f"  {hora}  "
                        f"{duracion:>5} s,  "
                        f"{importe:>8.2f} €"
                    )

                print(f"  Total del día: {total_dia:.2f} €\n")
            else:
                print ("Hoy no hay carreras registradas.\n")    
        
        elif instruccion == "i":
            if carrera is not None:
                print("Ya hay una carrera en curso. Finalizala con 'f'.\n")
                continue #vuelve al inicio del bucle
            ahora = time.monotonic()
            carrera = {
                "estado": estado_inicial, 
                "inicio": datetime.now(),
                "inicio_mono": ahora, #no puede ser una variable externa porque el tiempo iniciaría al ejecutar el programa y no al iniciar la carrera.
                "ultimo_tramo": ahora,
                "importe": 0.00}
        
            print(f"Carrera iniciada. El taxi está {carrera['estado'].upper()}.\n")
            log.info("Carrera iniciada")
        elif instruccion == "p" or instruccion == "m":
            estado_solicitado = "parado" if instruccion == "p" else "en movimiento"
            if carrera is None:
                print("No hay ninguna carrera en curso. Iniciala con 'i'.\n")
                continue #vuelve al inicio del bucle 
            elif carrera["estado"] == estado_solicitado:
                print(f"El taxi ya estaba {estado_solicitado.upper()}.\n")
                 
            else:
                carrera = cerrar_tramo(carrera, tarifas)
                carrera["estado"] = estado_solicitado
                duracion = calcular_duracion(carrera)
                print(f"El taxi está {carrera['estado'].upper()}.\n"
                      f"Duración del viaje: {duracion:.2f} segundos.\n"
                      f"El importe acumulado es: {carrera['importe']:.2f} €.\n"
                    )
                log.info("Cambio de estado a %s (%.2f €  acumulados).", carrera["estado"], carrera["importe"])
        elif instruccion == "f":
            if carrera is None:
                print("No hay ninguna carrera en curso. Iniciala con 'i'.\n")
                continue #vuelve al inicio del bucle 
            else:
                carrera = cerrar_tramo(carrera, tarifas)
                duracion = calcular_duracion(carrera)
                print(f"Carrera finalizada.\n"
                      f"Duración del viaje: {duracion:.2f} segundos.\n"
                      f"Total a cobrar: {carrera['importe']:.2f} €.\n"
                      )
                log.info("Carrera guardada: %d s, %.2f €",
                    round(duracion),
                    carrera["importe"])
                guardar_carrera(
                    carrera["inicio"],
                    duracion,
                    carrera["importe"]
                )
                carrera = None  # Reinicia la carrera
            
        else:
            print("Orden desconocida. Escribe 'a' para ver la ayuda.")
            log.warning("Orden desconocida: %r", instruccion)  # %: Es donde se insertará un valor | r: Muestra la representación del objeto y aparecen las comillas ' ' | instruccion: valor a insertar
     print("¡Hasta luego!")
     log.info("Cierre del taxímetro")   
     


     
    
    
    
# Punto de entrada
if __name__ == "__main__":
    main()
