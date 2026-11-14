def precio_entrada(edad):
    if edad < 12:
        return 4.0
    else:
        return 7.5


edad = int(input("Ingrese su edad: "))
costo = precio_entrada(edad)
print(f"El costo de la entrada es: {costo:.1f}€")
