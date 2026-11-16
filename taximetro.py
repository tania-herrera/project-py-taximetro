import time

antes = time.monotonic()
input("Escribe tu nombre: ")
despues = time.monotonic()
print(f"Tiempo transcurrido: {despues - antes:.2f} segundos")





tp = 0.02  #tarifa parado
tm = 0.05  #tarifa movimiento

def tarifa_cliente(i, p, m, f):
    carrera = input("Introduce una letra: \n"
    "i = inicio\t"
    "p = parado\t"
    "m = movimiento\t"
    "f = finaliza\n" \
    "a = ayuda\t"
    "s = salir\n").lower()

    estado_actual = 0
    inicio_tramo = 0
    importe_acumulado = 0.0

    """Consultar el instante actual.



Calcular el tiempo transcurrido desde el inicio del tramo.



Aplicar la tarifa correspondiente al estado anterior.



Añadir el importe al acumulado.



Actualizar el estado.



Registrar el nuevo inicio de tramo.

Evolución de inicio_tramo
1. Minuto 0
   
   Comienza la carrera.
   
   inicio_tramo = minuto 0.
2. Minuto 4
   
   Cambia a parada.
   
   Cierras movimiento y actualizas inicio_tramo al minuto 4.
3. Minuto 7
   
   Cambia a movimiento.
   
   Cierras parada y actualizas inicio_tramo al minuto 7.
4. Minuto 12
   
   Finaliza.
   
   Cierras el último tramo y calculas el importe definitivo."""

   
    while carrera != "s":
            if carrera == "i":
                i = time.monotonic()
                print("Carrera iniciada")           
            elif carrera == "p":
                p = time.monotonic() 
                print("tramo parado") 
            elif carrera == "m":
                m = time.monotonic()
                print("tramo en movimiento")
            continue
            if carrera == "f":
                f = time.monotonic()
                break
            print("¡Carrera finalizada!")

    def calcular_tarifa(t):
        

        calculo = tp * i 



    def calcular_tiempo
        if edad < 12:
            return 4.0
        else:
            return 7.5
    tarifa_parado = 0.02
    tarifa_movimiento = 0.05
    if edad < 12:
        return 4.0
    else:
        return 7.5
    carrera = input("Introduce una letra: \n").lower()

    

if entrada == "c":
    print("Un café")
elif entrada == "t":
    print("Un té")
else:
    print("No lo tenemos")

    print(f"El precio total de 3 cafés es: {total_cafes:.2f} €")

edad = int(input("Ingrese su edad: "))
costo = tarifa_cliente(inicio, finaliza)
print(f"El costo de la entrada es: {costo:.1f}€")

    