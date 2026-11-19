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

---

## Fase 2 — Observabilidad, persistencia y pruebas (US-05, US-06 y US-07)

En esta fase se incorporan mejoras para registrar la actividad del programa, configurar las tarifas externamente, almacenar las carreras y comprobar automáticamente la lógica de cálculo.

### 1. Configuración de tarifas mediante JSON

Las tarifas se encuentran en el archivo `config.json`, situado junto a `taximetro.py`.

```json
{
  "tarifa_parado": 0.02,
  "tarifa_movimiento": 0.05
}
```

Para cambiar una tarifa:

1. Abre `config.json`.
2. Modifica el valor correspondiente, manteniendo la estructura y el formato JSON.
3. Guarda el archivo.
4. Reinicia el programa para que cargue los nuevos valores.

Las tarifas se cargan una sola vez al arrancar el taxímetro. Por tanto, los cambios se aplican a las carreras iniciadas después de reiniciar el programa.

**Tarifas de respaldo:** si el archivo no existe, está mal formado o falta alguna de las claves necesarias, el programa registra una advertencia y utiliza las tarifas predeterminadas definidas en `TARIFAS_POR_DEFECTO`. Así puede continuar funcionando sin que un problema de configuración interrumpa su ejecución.

### 2. Almacenamiento del histórico de carreras

Las carreras finalizadas se guardan en el archivo `historial.csv`, situado junto a `taximetro.py`.

Cada carrera añade una fila con los siguientes datos:

| Campo | Contenido |
|---|---|
| `fecha` | Fecha de inicio de la carrera. |
| `hora` | Hora de inicio de la carrera. |
| `duracion_s` | Duración en segundos, redondeada a un número entero. |
| `importe` | Importe total de la carrera, con dos decimales. |

El archivo se crea automáticamente cuando se guarda la primera carrera. La cabecera se escribe una sola vez y las siguientes carreras se añaden al final, sin sobrescribir los registros anteriores.

### 3. Consulta de las carreras del día

La instrucción `h` permite consultar desde la terminal las carreras registradas durante el día actual.

Muestra la hora de inicio, la duración, el importe de cada carrera y el importe total acumulado del día.

Si no hay carreras registradas para la fecha actual, muestra un mensaje indicándolo.

### 4. Registro de eventos mediante Logging

El programa utiliza el módulo `logging` de Python para registrar los eventos relevantes de su ejecución en `taximetro.log`.

Se utilizan los niveles:

- `INFO`: para eventos normales, como el arranque, el inicio de una carrera, los cambios de estado y el cierre del programa.
- `WARNING`: para situaciones inesperadas que no interrumpen la ejecución, como introducir una orden desconocida o no poder cargar el archivo de tarifas.

El archivo permite consultar lo ocurrido durante la ejecución, incluyendo la fecha, la hora y el nivel de cada mensaje.

**Consultar el log en tiempo real**

Desde una segunda terminal, situada en la carpeta del proyecto, ejecuta:

```bash
tail -f taximetro.log
```

Este comando muestra las nuevas líneas del archivo a medida que se escriben. Para dejar de seguirlo, pulsa `Ctrl + C`.

### 5. Pruebas automatizadas con Pytest

El proyecto incorpora pruebas automatizadas para comprobar la función `importe_tramo()` sin necesidad de ejecutar una carrera completa.

**Preparación del entorno**

Desde la carpeta del proyecto, crea un entorno virtual:

```bash
python -m venv .venv
```

En Git Bash, actívalo con:

```bash
source .venv/Scripts/activate
```

Instala pytest:

```bash
python -m pip install pytest
```

Comprueba la instalación:

```bash
python -m pytest --version
```

**Ejecución de las pruebas**

Para ejecutar todos los tests:

```bash
python -m pytest
```

Para mostrar el nombre de cada test y su resultado:

```bash
python -m pytest -v
```

Los tests de `test_taximetro.py` comprueban:

- El cálculo de un tramo de 10 segundos en estado parado.
- El cálculo de un tramo de 10 segundos en movimiento.
- La generación de un `ValueError` cuando la duración es negativa.
- La suma de los importes de una carrera con tramos mixtos.

Las pruebas utilizan `pytest.approx()` para comparar importes decimales con una tolerancia adecuada.

**Resultado esperado:** cuatro pruebas superadas (`4 passed`).

## Alcance de la fase 1

La primera entrega implementa el MVP correspondiente a las historias de usuario US-01, US-02, US-03 y US-04.

Las funcionalidades de registro de operaciones, almacenamiento del histórico, configuración externa de tarifas y autenticación quedaban fuera del alcance de esa primera fase y se contemplaban en las siguientes entregas.
