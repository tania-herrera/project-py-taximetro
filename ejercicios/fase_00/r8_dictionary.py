libro = {"titulo": "Orgullo y prejuicio", "paginas": 432}
print(f"El libro {libro['titulo']} \ntiene {libro['paginas']} páginas\n")

libro["titulo"] = "El gen egoísta"
libro["paginas"] += 50
print(f"El libro {libro['titulo']} \ntiene {libro['paginas']} páginas")