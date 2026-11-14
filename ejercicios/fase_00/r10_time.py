import time
antes = time.monotonic()
input("Escribe tu nombre: ")
despues = time.monotonic()
print(f"Tiempo transcurrido: {despues - antes:.2f} segundos")