# Py-morant

Este proyecto incluye varias funciones útiles que desempeñan diferentes tareas.

## Instalación

Para instalar la paquetería pymorant en tu terminal escribe. 
```
pip install pymorant
```
Es recomendado usar un [ambiente virtual](https://docs.python.org/3/library/venv.html).

## Funciones

### 1. corregir_texto
```py
from pymorant import corregir_texto
```

Regresa el texto corregido ortográficamente, utilizando el modelo de lenguaje especificado.

**Parámetros**
- lista_corregir (str): lista de textos a corregir
- model (str): modelo de lenguaje a utilizar
- openai_key (str): llave de OpenAI

**Retorna**
- output (list): una lista con los textos corregidos

### 2. corregir_texto_excel
```py
from pymorant import corregir_texto_excel
```

Corrige los textos de la columna especificada en el archivo de Excel especificado, utilizando el modelo de lenguaje especificado.

**Parámetros**
- excel_file_path (str): ruta del archivo de Excel
- columna (str): nombre de la columna a corregir
- modelo (str): modelo de lenguaje a utilizar
- openai_api_key (str): llave de OpenAI
- chunk_size (int): tamaño de los chunks a procesar

### 3. generar_variantes_texto
```py
from pymorant import generar_variantes_texto
```

Regresa una lista de n variantes del texto original, utilizando el modelo de lenguaje especificado. Si formal=True, se generan variantes formales.

**Parámetros**
- text (str): texto original
- n (int): número de variantes a generar
- model (str): modelo de lenguaje a utilizar
- openai_key (str): llave de OpenAI
- formal (bool): si True, se generan variantes formales
- sex: sexo de la persona a la que se dirige el texto. Puede ser "H" (hombre), "M" (mujer) o "NA" (no aplica).

**Retorna**
- lista (list): lista con n variaciones del texto original

### 4. resumir_texto
```py
from pymorant import resumir_texto
```

Regresa un resumen del texto original, utilizando el modelo de lenguaje especificado.

**Parámetros**
- text (str): texto original
- model (str): modelo de lenguaje a utilizar
- openai_key (str): llave de OpenAI
- input_autogenerado (bool): si True, si el input es auto-generado por el modelo previamente.

**Retorna**
- texto (str): resumen del texto original

### 5. generar_categorias
```py
from pymorant import generar_categorias
```

Regresa una lista de n categorías del texto original, utilizando el modelo de lenguaje. especificado.

**Parámetros**
- text (str): texto original
- n (int): número de categorías a generar
- model (str): modelo de lenguaje a utilizar
- openai_key (str): llave de OpenAI

**Retorna**
- lista (list): lista de n categorias del texto original

### 6. asignar_categorias
```py
from pymorant import asignar_categorias
```

Regresa una lista de categorías asignadas a cada elemento de la lista original, utilizando el modelo de lenguaje especificado.

**Parámetros**
- lista_asignar (list): lista de textos a asignar categorías
- categorias (list): lista de categorías a asignar
- modelo (str): modelo de lenguaje a utilizar
- openai_api_key (str): llave de OpenAI

**Retorna**
- lista (list): lista de categorias asignadas

### 7. asignar_categorias_excel
```py
from pymorant import asignar_categorias_excel
```

Asigna categorías a los textos de la columna especificada en el archivo de Excel especificado, utilizando el modelo de lenguaje especificado.

**Parámetros**
- excel_file_path (str): ruta del archivo de Excel
- categorias (list): lista de categorías a asignar
- columna (str): nombre de la columna a asignar categorías
- modelo (str): modelo de lenguaje a utilizar
- openai_api_key (str): llave de OpenAI

## License
MIT
