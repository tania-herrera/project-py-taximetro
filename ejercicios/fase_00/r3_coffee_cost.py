PRECIO_CAFE = "1.20"
type_precio = type(PRECIO_CAFE)
print(type_precio)
total_cafes = float(PRECIO_CAFE) * 3
type_total = type(total_cafes)
print(type_total)
print(f"El precio total de 3 cafés es: {total_cafes:.2f} €")