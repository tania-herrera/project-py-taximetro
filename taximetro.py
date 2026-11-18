import time
import logging


tarifa_parado = 0.02  #tarifa parada
tarifa_movimiento = 0.05  #tarifa movimiento
estado_inicial = "parado"


AYUDA = ("\nTaxímetro digital\n"
                 "i  iniciar carrera (empieza PARADO)\n"
                 "p  el taxi está parado\n"
                 "m  el taxi está en movimiento\n"
                 "f  finalizar la carrera y ver el total\n"
                 "a  ver esta ayuda\n"
                 "s  salir\n")





# Funciones auxiliares

# Crear el logger: fuera de las funciones -> Obtener el objeto que registra los mensajes
log = logging.getLogger("taximetro")

# Definir la función de configuración: fuera de main
def configurar_log():
    logging.basicConfig( # 	Configurar dónde y cómo se registra el log
        filename="taximetro.log", # El nombre del archivo donde se guardarán los registros
        level=logging.INFO, # registra los mensajes INFO y todos los niveles más graves
        encoding="utf-8",
        format="%(asctime)s - %(levelname)s - %(message)s", # Fecha y hora | Nivel de gravedad | Contenido del mensaje
        )


def tarifa(estado):  #Responsabilidad: calcular la tarifa según el estado del taxi
    if estado == "parado":
        return tarifa_parado 
    elif estado == "en movimiento": 
        return tarifa_movimiento 
    else:
        return 0.0


def cerrar_tramo(carrera):
    hasta = time.monotonic()
    tramo = hasta - carrera["desde"]
    carrera["importe"] += tramo * tarifa(carrera["estado"])
    carrera["desde"] = hasta
    return carrera

def calcular_duracion(carrera):
    duracion_total = time.monotonic() - carrera["inicio"]
    return duracion_total



# Función principal
def main():
     #Ejecutar la configuración del logger al inicio de main
     configurar_log()
     log.info("Arranque del taxímetro")

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
        elif instruccion == "i":
            if carrera is not None:
                print("Ya hay una carrera en curso. Finalizala con 'f'.\n")
                continue #vuelve al inicio del bucle
            carrera = {
                "estado": estado_inicial, 
                "desde": time.monotonic(), #no puede ser una variable externa porque el tiempo iniciaría al ejecutar el programa y no al iniciar la carrera.
                "importe": 0.00}
            carrera ["inicio"]= carrera["desde"] #registra el instante de inicio de la carrera
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
                carrera = cerrar_tramo(carrera)
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
                carrera = cerrar_tramo(carrera)
                duracion = calcular_duracion(carrera)
                print(f"Carrera finalizada.\n"
                      f"Duración del viaje: {duracion:.2f} segundos.\n"
                      f"Total a cobrar: {carrera['importe']:.2f} €.\n"
                      )
                log.info("Carrera finalizada: %.2f €.", carrera["importe"])
                carrera = None  # Reinicia la carrera
            
        else:
            print("Orden desconocida. Escribe 'a' para ver la ayuda.")
            log.warning("Orden desconocida: %r", instruccion)  # %: Es donde se insertará un valor | r: Muestra la representación del objeto y aparecen las comillas ' ' | instruccion: valor a insertar
     print("¡Hasta luego!")
     log.info("Cierre del taxímetro")   
     


     
    
    
    
# Punto de entrada
if __name__ == "__main__":
    main()
