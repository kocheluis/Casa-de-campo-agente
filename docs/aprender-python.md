# Ramp-up de Python (para quien viene de C / Java)

> Guía práctica para el ramp-up del plan. La idea no es aprender "todo Python", sino lo
> necesario para leer y modificar los `tools/` del proyecto con confianza. Tú ya dominas
> lógica, tipos y bases de datos; aquí va sobre todo **qué cambia** respecto a C/Java.

## Módulo 1 — Entorno (✅ ya configurado)

| Acción | Comando |
|---|---|
| Activar el entorno (PowerShell) | `.\.venv\Scripts\Activate.ps1` |
| Desactivar | `deactivate` |
| Instalar dependencias | `pip install -r requirements.txt` |
| Ejecutar un script | `python tools/progress.py` |
| Abrir la consola interactiva (REPL) | `python` (sales con `exit()`) |

El **venv** es como el aislamiento de dependencias de Maven/Gradle, pero por carpeta.
El `requirements.txt` es tu lista de dependencias.

## Módulo 2 — Fundamentos: C/Java → Python

### Lo primero que choca
- **No hay llaves `{}`**: los bloques se definen por **indentación** (4 espacios). La
  indentación no es estética, es sintaxis obligatoria.
- **No hay `;`** al final de línea.
- **No declaras el tipo** de las variables: `x = 5` (no `int x = 5;`). El tipo existe
  (Python es fuertemente tipado en tiempo de ejecución), solo no lo escribes.
- **Comentarios** con `#` (no `//`). Bloques de doc con `"""triple comilla"""`.

### Tabla de equivalencias

| Concepto | C / Java | Python |
|---|---|---|
| Variable | `int n = 5;` | `n = 5` |
| Condicional | `if (a > b) { ... }` | `if a > b:` (cuerpo indentado) |
| Bucle contado | `for (int i=0;i<10;i++)` | `for i in range(10):` |
| Bucle sobre colección | `for (String s : lista)` | `for s in lista:` |
| Función | `int sum(int a,int b){return a+b;}` | `def sum(a, b): return a + b` |
| Array / Lista | `int[] / ArrayList` | `lista = [1, 2, 3]` |
| Mapa / Diccionario | `HashMap<K,V>` | `d = {"clave": "valor"}` |
| null | `null` | `None` |
| true / false | `true` / `false` | `True` / `False` |
| Y / O / No | `&&` `\|\|` `!` | `and` `or` `not` |
| Concatenar texto | `"Hola " + nombre` | `f"Hola {nombre}"` (f-string) |
| Imprimir | `System.out.println(x)` | `print(x)` |
| Longitud | `lista.size()` / `arr.length` | `len(lista)` |

### Tipos básicos
```python
n = 42              # int
precio = 99.9       # float
nombre = "Ana"      # str (texto)
activo = True       # bool
nada = None         # ausencia de valor (como null)
```

### Listas (como ArrayList) y diccionarios (como HashMap)
```python
clientes = ["Ana", "Luis", "Marta"]   # lista
clientes.append("Pedro")               # agregar
print(clientes[0])                     # "Ana" (índice desde 0)
print(len(clientes))                   # 4

cliente = {"nombre": "Ana", "telefono": "51999", "noches": 2}   # diccionario
print(cliente["nombre"])               # "Ana"
cliente["estado"] = "confirmado"       # agregar/actualizar clave
```

### Funciones
```python
def precio_total(noches, precio_noche):
    """Calcula el total de la reserva."""   # docstring (documentación)
    return noches * precio_noche

total = precio_total(3, 120)   # 360
```

### Control de flujo
```python
if total > 300:
    print("Reserva grande")
elif total > 100:           # 'else if' en Python es 'elif'
    print("Reserva media")
else:
    print("Reserva pequeña")

for cliente in clientes:    # recorre la lista directamente
    print(cliente)

i = 0
while i < 3:
    print(i)
    i += 1                  # no existe i++, se usa i += 1
```

### Imports (como los `import` de Java)
```python
import re                       # toda la librería
from pathlib import Path        # solo una parte
from config import env          # de un archivo nuestro (config.py)
```

## Módulo 3 — Leer el código real del proyecto

El mejor archivo para empezar a leer es **`tools/progress.py`**: usa solo la librería
estándar, está muy comentado y hace algo concreto (contar tareas y escribir el avance).

Recorrido sugerido:
1. **`tools/config.py`** — corto. Verás `import`, una función `env()`, y cómo se leen
   variables de entorno. Fíjate en los `"""docstrings"""`.
2. **`tools/progress.py`** — funciones, listas, diccionarios, bucles `for`, f-strings y
   expresiones regulares (`re`). Es el ejercicio 3 de abajo.
3. **`tools/db_client.py`** — una **clase** (`class DBClient`), que es como una clase de
   Java pero con `self` en vez de `this`, y el constructor se llama `__init__`.
4. **`tools/ai_reply.py`** — usa LiteLLM para llamar al LLM elegido (Claude/OpenAI/Gemini/DeepSeek).

### `requests` en 30 segundos (llamar a una API)
```python
import requests
r = requests.get("https://api.ejemplo.com/datos", timeout=20)
print(r.status_code)   # 200 si salió bien
print(r.json())        # convierte la respuesta JSON en un diccionario
```

## Ejercicios (hazlos en el REPL o en un archivo `.tmp/practica.py`)

1. **Variables y f-strings:** crea `nombre`, `noches` y `precio_noche`; imprime
   `"<nombre> reservó <noches> noches por S/ <total>"`.
2. **Lista + bucle:** crea una lista de 3 clientes (diccionarios con `nombre` y `noches`)
   y recorre imprimiendo el nombre de cada uno y su total.
3. **Leer código:** abre `tools/progress.py` y responde: ¿qué hace la función `bar()`?
   ¿qué tipo devuelve `parse_phases()`? (pista: una lista de diccionarios).
4. **Modificar y ver el efecto:** en `PROJECT_PLAN.md` marca una tarea del Ramp-up como
   `- [x]`, corre `python tools/progress.py` y observa cómo cambia el "Avance actual".

## Recursos
- Tutorial oficial (español): https://docs.python.org/es/3/tutorial/
- "Python para programadores" (si vienes de otro lenguaje): la sección de tipos y
  estructuras de datos del tutorial oficial es suficiente.
