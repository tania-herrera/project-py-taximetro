import time


tarifa_parado = 0.02  #tarifa parada
tarifa_movimiento = 0.05  #tarifa movimiento
estado_inicial = "parado"


AYUDA = ("Taxímetro digital\n"
                 "i  iniciar carrera (empieza PARADO)\n"
                 "p  el taxi está parado\n"
                 "m  el taxi está en movimiento\n"
                 "f  finalizar la carrera y ver el total\n"
                 "a  ver esta ayuda\n"
                 "s  salir\n")





# Funciones auxiliares

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
                carrera = None  # Reinicia la carrera
            
        else:
            print("Orden desconocida. Escribe 'a' para ver la ayuda.")
     print("¡Hasta luego!")   
     


     
    
    
    
# Punto de entrada
if __name__ == "__main__":
    main()
