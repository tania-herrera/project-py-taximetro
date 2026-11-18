# Taxímetro digital

Prototipo de taxímetro por terminal desarrollado en Python para **TaxiTech Solutions**.

**Fase 1 — MVP funcional (US-01 a US-04)**

El programa permite gestionar carreras de taxi desde la terminal, alternando entre los estados de parado y en movimiento, y calculando el importe acumulado según el tiempo transcurrido en cada estado.

## Cómo arrancarlo

Necesitas Python 3.10 o superior.

Desde la carpeta del proyecto, ejecuta:

```bash
python taximetro.py
```

## Cómo se usa

El programa permite introducir comandos desde la terminal. Escribe una letra y pulsa Intro:

| Orden | Qué hace |
|---|---|
| `i` | Inicia una carrera. El taxi comienza en estado parado. |
| `p` | Cambia el estado del taxi a parado. |
| `m` | Cambia el estado del taxi a en movimiento. |
| `f` | Finaliza la carrera y muestra la duración total y el importe a cobrar. |
| `a` | Muestra las instrucciones de uso. |
| `s` | Sale del programa, siempre que no haya una carrera en curso. |

Al finalizar una carrera, el programa permite iniciar otra sin necesidad de cerrarse.

## Tarifas y cálculo del importe

El importe se calcula acumulando el coste de cada tramo de la carrera según el estado del taxi:

| Estado del taxi | Tarifa |
|---|---:|
| Parado | 0,02 €/segundo |
| En movimiento | 0,05 €/segundo |

Cuando se produce un cambio de estado o se finaliza la carrera, se cierra el tramo actual y se calcula su importe:

**Importe del tramo = duración del tramo × tarifa correspondiente**

El importe de cada tramo se suma al acumulado de la carrera.

Al finalizar, se muestra el importe total en euros con dos decimales y la duración total de la carrera en segundos.

## Decisiones técnicas

### Estructura y control del programa

- **Bucle principal (`while True`):** se utiliza para mantener el programa activo y permitir gestionar varias carreras consecutivas. El bucle solo termina cuando el usuario introduce `s` y no existe ninguna carrera en curso.

- **Control del flujo con `continue`:** se utiliza cuando una instrucción no puede ejecutarse, por ejemplo, al intentar iniciar una segunda carrera o cambiar el estado cuando no hay ninguna activa. Así se evita ejecutar el resto de instrucciones de esa iteración.

- **Validación de estados:** antes de cambiar el estado del taxi se comprueba si la carrera está activa y si el estado solicitado es diferente del actual. Esto evita operaciones innecesarias y situaciones incoherentes.

### Gestión del tiempo y cálculo de tarifas

- **`time.monotonic()`:** se utiliza para medir el tiempo transcurrido, evitando depender del reloj del sistema, que puede sufrir ajustes.

- **Separación entre duración e importe:** `cerrar_tramo()` calcula el importe correspondiente al tramo finalizado y actualiza el instante de inicio del siguiente tramo. Por su parte, `calcular_duracion()` obtiene la duración total de la carrera desde su inicio, sin modificar sus datos. Esta separación permite consultar la duración independientemente de los cambios de estado.

- **Acumulación por tramos:** el importe se calcula al cerrar cada tramo, aplicando la tarifa correspondiente al estado del taxi durante ese intervalo.

### Organización de los datos

- **Diccionario de carrera:** se utiliza para agrupar el estado actual, el instante de inicio de la carrera, el inicio del tramo vigente y el importe acumulado. De esta manera, las funciones pueden trabajar con la información de una misma carrera.

- **Un único fichero (`taximetro.py`):** se mantiene toda la lógica en un mismo archivo para simplificar la estructura del primer prototipo. La separación en funciones permite mantener responsabilidades diferenciadas sin introducir todavía varios módulos.

## Alcance de esta fase

Esta entrega implementa el MVP correspondiente a las historias de usuario US-01, US-02, US-03 y US-04.

Las funcionalidades de registro de operaciones, almacenamiento del histórico, configuración externa de tarifas y autenticación quedan fuera del alcance de esta primera fase y se contemplan en las siguientes entregas.