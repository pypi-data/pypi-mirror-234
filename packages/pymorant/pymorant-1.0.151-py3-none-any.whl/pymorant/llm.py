import ast
import os
import inspect
import math
import time
import pandas as pd
from .utils import limpiar_texto, TripleHyphenSeparatedListOutputParser, get_llm_cost # noqa
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ReduceDocumentsChain, MapReduceDocumentsChain # noqa
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.llms import OpenAI


def corregir_texto(lista_corregir, modelo, openai_api_key, chunk_size=30):

    if not isinstance(lista_corregir, list):
        raise TypeError("lista_corregir debe ser una lista")

    if not (isinstance(chunk_size, int) or isinstance(chunk_size, float)):
        raise TypeError("Chunk size debe ser un entero")

    if not isinstance(modelo, str):
        raise TypeError("Modelo debe ser un string")

    if not isinstance(openai_api_key, str):
        raise TypeError("OpenAI API Key debe ser un string")

    if chunk_size < 10:
        raise ValueError("Chunk size debe ser mayor o igual a 10")

    if chunk_size > 80:
        raise ValueError("Chunk size debe ser menor o igual a 80")

    costo_total = 0
    tokens_totales = 0
    start_time = time.time()  # Record the start time

    lista_limpia = []
    aux_dict = dict()
    answer = ["no_corregido"] * len(lista_corregir)

    for i, el in enumerate(lista_corregir):

        elemento = limpiar_texto(el) # noqa

        # ZWJ es un caracter que se utiliza para unir emojis
        elemento = elemento.replace("\u200d", "")

        if elemento == '':
            continue

        if elemento not in aux_dict:
            aux_dict[elemento] = {
                'correccion_ortografia': 'sin_correccion',
                'original': [i]
                }
            lista_limpia.append(elemento)
        else:
            aux_dict[elemento]['original'].append(i)

    output_parser = TripleHyphenSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    template_string = '''
    Eres un experto en limpieza de texto y ortografía. Te proporcionamos la
    siguiente lista: '{lista_input}'. Tu objetivo es corregir posibles faltas
    ortográficas y gramaticales de cada elemento de la lista.

    Regresarás una lista separada por triple guión medio (---) para separar
    cada uno de los elementos de la lista.

    Si un elemento está correctamente escrito, déjalo como está, sin hacer
    cambios. No es necesario que indiques si un texto no tiene errores
    ortográficos; simplemente déjalo sin modificar. Recuerda que las palabras
    en mayúsculas también pueden ir acentuadas.

    Asimismo, no hagas comentarios adicionales como: la lista corregida es... ,
    sólo debes de proporcionar lo que se te pide. Si encuentras dificultades
    para comprender algún texto, déjalo sin cambios.

    A cada elemento de la lista resultante, agrégale FORZOSAMENTE
    ' - ' (espacio, guion medio, espacio), seguido del elemento
    correspondiente de la lista original '{lista_input}', no corrijas la
    ortografía del elemento de esta lista.

    Recuerda que el formato es el siguiente:
    'elemento_corregido - elemento_original'.

    Por ejemplo si en la lista aparece "100 porsiento" deberás dejarlo como
    "100 porsiento" y no como "100 por ciento", y deberás devolver:
    '100 por ciento - 100 porsiento'.

    Otro ejemplo: si "no se" está en la lista original, deberás devolver:
    'no sé - no se'.

    Con una lista de tamaño 2, tú regresarías algo como esto:
    '100 por ciento - 100 porsiento' --- 'no sé - no se'.

    La precisión al agregar ' - ' es crucial, pues el
    resultado depende de ello.

    Devuelve una lista del mismo tamaño de la lista original. Identifica
    correctamente cuales son los elementos de la lista, no te confundas si un
    elemento contiene comas.

    Acata al 100 las instrucciones de formato. Recuerda que estás utilizando
    tres guiones medios (---) para separar los elementos de la lista.

    Instrucciones de formato: {format_instructions}
    '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["lista_input"],
        partial_variables={'format_instructions': format_instructions}
    )

    for i in range(math.ceil(len(lista_limpia) / chunk_size)):

        chunk = lista_limpia[i * chunk_size:(i + 1) * chunk_size]
        observaciones_corregidas = 0
        llm_output = []

        list_prompt = prompt.format_messages(
                lista_input=chunk,
                format_instructions=format_instructions)

        llm = ChatOpenAI(
            temperature=0.0, model=modelo, openai_api_key=openai_api_key
        )

        with get_openai_callback() as cb:
            model_output = llm(list_prompt)
            costo_total += cb.total_cost
            tokens_totales += cb.total_tokens

        content = model_output.content
        llm_output = output_parser.parse(content)

        if len(llm_output) == 1:
            llm_output = llm_output[0].strip('"\'.,[]*')
            llm_output = llm_output.split('---')

        for output in llm_output:
            try:
                output_list = output.split(' - ')
                key = limpiar_texto(output_list[1])
                value = output_list[0]

                aux_dict[key]["correccion_ortografia"] = limpiar_texto(value)
                observaciones_corregidas += 1
            except: # noqa
                if len(output_list) == 2:
                    print("--------------")
                    print(f'key:[{key}]')
                    print(f'value: {value}')
                    print("--------------")

        print("-----------------------------------")
        print(f'Chunk {i + 1} de {math.ceil(len(lista_limpia) / chunk_size)}')
        print(f'Tamaño del chunk: {len(chunk)}')
        print(f'Cantidad de observaciones corregidas generadas: {len(llm_output)}') # noqa
        print(f'Cantidad de obervaciones corregidas y asignadas: {observaciones_corregidas}') # noqa
        print("-----------------------------------\n")

    for key in aux_dict.keys():
        for i in aux_dict[key]["original"]:
            answer[i] = aux_dict[key]["correccion_ortografia"]

    for i, element in enumerate(answer):
        answer[i] = limpiar_texto(element)

    file_name = f"valores_corregidos_ortografia_{modelo}.txt"
    frame = inspect.currentframe()
    caller_filename = inspect.getouterframes(frame)[-1].filename
    directory = os.path.dirname(os.path.abspath(caller_filename))

    execution_time = time.time() - start_time
    nombre_fun = inspect.stack()[0][3]
    get_llm_cost(directory, nombre_fun, modelo, tokens_totales, costo_total, execution_time) # noqa

    file_path_documents = os.path.join(directory, "documents")

    if not os.path.exists(file_path_documents):
        os.mkdir(file_path_documents)

    # with open(f'{file_name}', 'w') as f:
    with open(f'{file_path_documents}/{file_name}', 'w') as f:
        for key in aux_dict.keys():
            if aux_dict[key]["correccion_ortografia"] in ("sin_correccion", "no_corregido"): # noqa
                continue
            f.write(f'texto: {key} - correccion_ortografia: {aux_dict[key]["correccion_ortografia"]}\n') # noqa

    return answer


def corregir_texto_excel(excel_file_path, columna, modelo, openai_api_key, chunk_size=30): # noqa
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Archivo {excel_file_path} no encontrado")

    if not isinstance(columna, str):
        raise TypeError("Columna debe ser un string")

    # Carga de datos
    df = pd.read_excel(excel_file_path)

    if columna not in df.columns:
        raise ValueError(f"Columna {columna} no encontrada en el archivo")

    # Limpieza de datos
    df = df.fillna(value='')

    lista_corregir = df[columna].to_list()

    # Asignación de categorías
    columna_corregida = corregir_texto(
        lista_corregir=lista_corregir,
        modelo=modelo,
        openai_api_key=openai_api_key,
        chunk_size=chunk_size
    )

    # Generar nueva columna
    df[f'{columna}_corregida_{modelo}'] = columna_corregida

    # Guarda el archivo
    df.to_excel(excel_file_path, index=False)
    print("El proceso ha terminado.")


def generar_variantes_texto(text, n, modelo, openai_api_key, contexto="Eres un experto en análisis de texto."): # noqa

    costo_total = 0
    tokens_totales = 0
    start_time = time.time()  # Record the start time

    output_parser = TripleHyphenSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    template_string = '''

    Contexto: {contexto}

    Recibes el siguiente texto: {text_input}. Tu tarea es crear {n_input}
    variaciones únicas de este texto, utilizando diferentes palabras y
    estructuras para transmitir el mismo significado. No puedes
    utilizar palabras que se puedan considerar ofensivas o sexuales.
    Por ejemplo, no utilizar la palabra "estimulante".

    Recuerda que debes crear {n_input} variaciones únicas del texto.
    No más de {n_input}, no menos de {n_input} variaciones.

    Es muy importante que NO numeres la lista.

    Usa triple guión medio (---) para separar las variaciones.

    Por ejemplo:
    ´Hola, ¿cómo estás? --- Hola, ¿qué tal? --- Hola, ¿qué onda?´

    Favor de mantener saltos de linea, comas, puntos, signos de
    interrogación, etc.

    {format_instructions}
    '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["text_input", "n_input"],
        partial_variables={
            'format_instructions': format_instructions,
            "contexto": contexto,
        })

    list_prompt = prompt.format_messages(
        text_input=text,
        n_input=n,
        format_instructions=format_instructions,
        contexto=contexto)

    llm = ChatOpenAI(
        temperature=0.6, openai_api_key=openai_api_key, model=modelo)

    with get_openai_callback() as cb:
        model_output = llm(list_prompt)
        costo_total += cb.total_cost
        tokens_totales += cb.total_tokens

    content = model_output.content

    llm_output = output_parser.parse(content)

    if len(llm_output) == 1:
        llm_output = llm_output[0].strip('"\'.,[]*')
        llm_output = llm_output.split('---')

    answer = []
    for output in llm_output:
        answer.append(output.strip('\'\n".,[]*- '))

    frame = inspect.currentframe()
    caller_filename = inspect.getouterframes(frame)[-1].filename
    directory = os.path.dirname(os.path.abspath(caller_filename))

    execution_time = time.time() - start_time
    nombre_fun = inspect.stack()[0][3]
    get_llm_cost(directory, nombre_fun, modelo, tokens_totales, costo_total, execution_time) # noqa

    return answer


def resumir_texto(lista_resumir, openai_api_key, modelo="gpt-3.5-turbo-16k", instrucciones="Realiza un resumen conciso del texto"): # noqa

    texto = ['\\n'.join(lista_resumir)]

    docs = [Document(page_content=t) for t in texto]

    openai_llm = OpenAI(temperature=0.0, openai_api_key=openai_api_key)

    num_tokens = openai_llm.get_num_tokens(texto[0])

    if num_tokens >= 3500:

        llm = ChatOpenAI(
            temperature=0, openai_api_key=openai_api_key, model=modelo
        )

        map_template = '''Eres el mejor analista de texto del mundo, se te
        proporciona el siguiente texto: {docs}'''+f"{instrucciones} Helpful Answer:" # noqa
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=llm, prompt=map_prompt)

        reduce_template = """Lo siguiente es un conjunto de resumenes:
        {doc_summaries}

        Toma esto y destílalo en un resumen final y consolidado de los temas
        principales.
        Helpful Answer:"""

        reduce_prompt = PromptTemplate.from_template(reduce_template)
        reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="doc_summaries"
        )

        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=combine_documents_chain,
            collapse_documents_chain=combine_documents_chain,
            token_max=16000
        )

        map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=map_chain,
            reduce_documents_chain=reduce_documents_chain,
            document_variable_name="docs",
            return_intermediate_steps=False
        )

        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1500, chunk_overlap=200
        )

        split_docs = text_splitter.split_documents(docs)
        resumen = map_reduce_chain.run(split_docs)
    else:
        prompt_template = """Eres el mejor analista de texto. Realiza un resumen
        conciso utilizando esta
        información: {text} . Que sea lo más breve posible."""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["text"]
        )

        chain = load_summarize_chain(
            llm=openai_llm,
            chain_type='stuff',
            verbose=True,
            prompt=PROMPT
        )

        resumen = chain.run(docs)

    return resumen


def generar_categorias(text, n, modelo, openai_api_key):

    """
    Regresa una lista de n categorías del texto original, utilizando el modelo
    de lenguaje especificado.

    Parametros:
    text (str): texto original
    n (int): número de categorías a generar
    model (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    """

    costo_total = 0
    tokens_totales = 0
    start_time = time.time()  # Record the start time

    try:
        prompt = PromptTemplate(
            input_variables=["lista", "n_input"],
            template='''Recibí un resumen con características clave de las
            respuestas a una pregunta: '{lista}'. A partir de esta información,
            genera {n_input} categorías que representen los aspectos más
            relevantes. No expliques a que se refiere cada categoría.
            Devuelve estas categorías en una lista de Python lista para poder
            ser procesada.'''
        )

        chatopenai = ChatOpenAI(
            model_name=modelo, openai_api_key=openai_api_key
        )

        llmchain_chat = LLMChain(llm=chatopenai, prompt=prompt)

        with get_openai_callback() as cb:
            categorias = llmchain_chat.run({
                "lista": text,
                "n_input": n,
            })
            costo_total += cb.total_cost
            tokens_totales += cb.total_tokens

        categorias_list = ast.literal_eval(categorias)

        frame = inspect.currentframe()
        caller_filename = inspect.getouterframes(frame)[-1].filename
        directory = os.path.dirname(os.path.abspath(caller_filename))

        execution_time = time.time() - start_time
        nombre_fun = inspect.stack()[0][3]
        get_llm_cost(directory, nombre_fun, modelo, tokens_totales, costo_total, execution_time) # noqa

        return categorias_list
    except Exception as e:
        raise ValueError("Error al generar categorías: " + str(e))


def asignar_categorias(lista_asignar, categorias, modelo, openai_api_key, chunk_size=30, contexto="Eres un análista de datos"): # noqa

    costo_total = 0
    tokens_totales = 0
    start_time = time.time()  # Record the start time

    '''
    Regresa una lista de categorías asignadas a cada elemento de la lista
    original, utilizando el modelo de lenguaje especificado.

    Parametros:
    lista_asignar (list): lista de textos a asignar categorías
    categorias (list): lista de categorías a asignar
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''

    if not isinstance(categorias, list):
        raise TypeError("Categorias debe ser una lista")

    if not (isinstance(chunk_size, int) or isinstance(chunk_size, float)):
        raise TypeError("Chunk size debe ser un entero")

    if not isinstance(modelo, str):
        raise TypeError("Modelo debe ser un string")

    if not isinstance(openai_api_key, str):
        raise TypeError("OpenAI API Key debe ser un string")

    if chunk_size < 0:
        raise ValueError("Chunk size debe ser mayor o igual a 0")

    if chunk_size > 80:
        raise ValueError("Chunk size debe ser menor o igual a 80")

    answer = ["no_asignado"] * len(lista_asignar)
    lista_limpia = []
    aux_dict = dict()

    for i, el in enumerate(lista_asignar):

        elemento = limpiar_texto(el, quitar_acentos=True, quitar_caracteres_especiales=True, minusculas=True) # noqa

        if elemento == '':
            continue

        if elemento not in aux_dict:
            aux_dict[elemento] = {
                'categoria': 'sin_categoria',
                'original': [i]
            }
            lista_limpia.append(elemento)
        else:
            aux_dict[elemento]['original'].append(i)

    output_parser = CommaSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    template_string = '''
    Eres un experto en análisis de texto. Te proporcionamos la
    siguiente lista: '{lista_input}'. Tu objetivo es asignar SOLO una
    categoria de la lista de categorias '{categorias_input}'
    a cada elemento de la lista. Si un elemento no se ajusta a
    ninguna categoria o si no estas seguro, asigna "sin_categoria".

    Para cada elemento de la lista generada, tienes que regresarlo en el
    siguiente formato: "elemento_original - categoria_asignada". Por ejemplo,
    "no se - sin_categoria". Es decir, tienes que agregar " - " (espacio,
    guion medio, espacio) FORZOZAMENTE y el elemento correspondiente de la
    lista '{lista_input}'. Tienes que tener eficiencia perfecta al agregar
    el ' - ', ya que es de vida o muerte tu resultado.

    El elemento de la izquierda del ' - ' es estrictamente elemento de la
    lista original. Un ejemplo de la lista es:

    [no se - sin_categoria, cuidar el medio ambiente - medio_ambiente,
    aumento en el presupuesto de salud - salud]

    Devuelve una lista del mismo tamaño de la lista original ESTRICTAMENTE,
    utilizando el formato de lista de Python y no generes carácteres especiales
    como saltos de línea.

    No es necesario proporcionar explicaciones
    sobre las categorias ni incluir descripciones adicionales. Tu enfoque se
    centra en la asignación de categorias. Solamente entrega la lista. No
    menciones cosas como "aquí está la lista con ...", simplemente entrega la
    lista.

    Contexto: {contexto}

    Instrucciones de formato: {format_instructions}
    '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["lista_input", "categorias_input"],
        partial_variables={
            'format_instructions': format_instructions,
            "contexto": contexto
        }
    )

    for i in range(math.ceil(len(lista_limpia) / chunk_size)):

        chunk = lista_limpia[i * chunk_size:(i + 1) * chunk_size]
        categorias_asignadas = 0
        llm_output = []

        list_prompt = prompt.format_messages(
            lista_input=chunk,
            categorias_input=categorias,
            format_instructions=format_instructions,
            contexto=contexto)

        llm = ChatOpenAI(
            temperature=0.0, model=modelo, openai_api_key=openai_api_key
        )

        try:

            with get_openai_callback() as cb:
                model_output = llm(list_prompt)
                costo_total += cb.total_cost
                tokens_totales += cb.total_tokens

            content = model_output.content
            content = content.replace('\n', '')
            llm_output = output_parser.parse(content)

            if len(llm_output) == 1:
                llm_output = llm_output[0].strip('"\'.,[]*')
                llm_output = llm_output.split(',')

            for output in llm_output:
                try:
                    output_list = output.split(' - ')
                    key = limpiar_texto(output_list[0], quitar_acentos=True, quitar_caracteres_especiales=True, minusculas=True) # noqa
                    value = output_list[1].strip('\'" ')

                    aux_dict[key]["categoria"] = limpiar_texto(value, quitar_acentos=True, quitar_caracteres_especiales=True, minusculas=True) # noqa
                    categorias_asignadas += 1
                except: # noqa
                    if len(output_list) == 2:
                        print("--------------")
                        print(f'key:[{key}]')
                        print(f'value: {value}')
                        print("--------------")

        except: # noqa
            print("Error al asignar categorías, seguramente por tokens excedidos, baja el chunk size") # noqa

        print("-----------------------------------")
        print(f'Chunk {i + 1} de {math.ceil(len(lista_limpia) / chunk_size)}')
        print(f'Tamaño del chunk: {len(chunk)}')
        print(f'Cantidad de categorias generadas: {len(llm_output)}')
        print(f'Cantidad de categorias asignadas: {categorias_asignadas}')
        print("-----------------------------------\n")

    for key in aux_dict.keys():
        for i in aux_dict[key]["original"]:
            answer[i] = aux_dict[key]["categoria"]

    for i, element in enumerate(answer):
        answer[i] = limpiar_texto(element, quitar_acentos=True, quitar_caracteres_especiales=True, minusculas=True) # noqa

    # se genera el archivo con los valores categorizados
    file_name = f"valores_categorizados_{modelo}.txt"
    frame = inspect.currentframe()
    caller_filename = inspect.getouterframes(frame)[-1].filename
    directory = os.path.dirname(os.path.abspath(caller_filename))

    execution_time = time.time() - start_time
    nombre_fun = inspect.stack()[0][3]
    get_llm_cost(directory, nombre_fun, modelo, tokens_totales, costo_total, execution_time) # noqa

    file_path = os.path.join(directory, "documents")

    if not os.path.exists(file_path):
        os.mkdir(file_path)

    with open(f'{file_path}/{file_name}', 'w') as f:
        for key in aux_dict.keys():
            if aux_dict[key]["categoria"] in ("sin_categoria", "no_asignado"): # noqa
                continue
            f.write(f'texto: {key} - categoria: {aux_dict[key]["categoria"]}\n') # noqa

    return answer


def asignar_categorias_excel(excel_file_path, categorias, columna, modelo, openai_api_key, chunk_size=30, contexto="Eres un análista de datos"): # noqa
    '''
    Asigna categorías a los textos de la columna especificada en el archivo
    de Excel especificado, utilizando el modelo de lenguaje especificado.

    Parametros:
    excel_file_path (str): ruta del archivo de Excel
    categorias (list): lista de categorías a asignar
    columna (str): nombre de la columna a asignar categorías
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''
    # Validaciones
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Archivo {excel_file_path} no encontrado")

    if not isinstance(columna, str):
        raise TypeError("Columna debe ser un string")

    # Carga de datos
    df = pd.read_excel(excel_file_path)

    if columna not in df.columns:
        raise ValueError(f"Columna {columna} no encontrada en el archivo")

    # Limpieza de datos
    df = df.fillna(value='')

    lista_asignar = df[columna].to_list()

    # Asignación de categorías
    categorias_asignadas = asignar_categorias(
        lista_asignar,
        categorias=categorias,
        modelo=modelo,
        openai_api_key=openai_api_key,
        chunk_size=chunk_size,
        contexto=contexto,
    )

    # Generar nueva columna
    df[f'{columna}_categorizada_{modelo}'] = categorias_asignadas

    # Guarda el archivo
    df.to_excel(excel_file_path, index=False)


def asignar_multicategorias(lista_asignar, categorias, modelo, openai_api_key, chunk_size=30, contexto="Eres un análista de datos"): # noqa

    '''
    Regresa una lista de categorías asignadas a cada elemento de la lista
    original, utilizando el modelo de lenguaje especificado (PERMITE
    MULTICATEGORIZACION).

    Parametros:
    lista_asignar (list): lista de textos a asignar categorías
    categorias (list): lista de categorías a asignar
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''
    costo_total = 0
    tokens_totales = 0
    start_time = time.time()

    if not isinstance(categorias, list):
        raise TypeError("Categorias debe ser una lista")

    if not (isinstance(chunk_size, int) or isinstance(chunk_size, float)):
        raise TypeError("Chunk size debe ser un entero")

    if not isinstance(modelo, str):
        raise TypeError("Modelo debe ser un string")

    if not isinstance(openai_api_key, str):
        raise TypeError("OpenAI API Key debe ser un string")

    if chunk_size < 10:
        raise ValueError("Chunk size debe ser mayor o igual a 10")

    if chunk_size > 80:
        raise ValueError("Chunk size debe ser menor o igual a 80")

    answer = ["no_asignado"] * len(lista_asignar)
    lista_limpia = []
    aux_dict = dict()

    for i, el in enumerate(lista_asignar):

        elemento = limpiar_texto(
            el,
            quitar_acentos=True,
            quitar_caracteres_especiales=True,
            minusculas=True
        )

        if elemento == '':
            continue

        if elemento not in aux_dict:
            aux_dict[elemento] = {
                'categoria': 'sin_categoria',
                'original': [i]
            }
            lista_limpia.append(elemento)
        else:
            aux_dict[elemento]['original'].append(i)

    output_parser = TripleHyphenSeparatedListOutputParser()
    format_instructions = output_parser.get_format_instructions()

    template_string = '''Eres un experto en análisis de texto. 
    Te proporcionamos la siguiente lista: '{lista_input}'. Tu objetivo es
    asignar UNA O MÁS categorías que consideres adecuadas de la lista de
    categorias '{categorias_input}' a cada elemento de la lista. Si un
    elemento no se ajusta a ninguna categoria o si no estas seguro, asigna
    "sin_categoria".

    Para cada elemento de la lista generada, tienes que regresarlo en el
    siguiente formato:
    "elemento_original - categoria_asignada_1/categoria_asignada_2/categoria_asignada_3".
    
    Por ejemplo, "no se - sin_categoria". Otro ejemplo,
    "Seguridad y economía - seguridad/economia". Otro ejemplo,
    "Seguridad y economia y salud - seguridad/economia/salud". Es decir, tienes que
    agregar " - " (espacio,guion medio, espacio) FORZOZAMENTE y el elemento
    correspondiente de la lista '{lista_input}'. Tienes que tener eficiencia
    perfecta al agregar el ' - ', ya que es de vida o muerte tu resultado.

    El elemento de la izquierda del ' - ' es estrictamente elemento de la lista
    original. Un ejemplo de la lista es:

    "'no se - sin_categoria' --- 'cuidar el medio ambiente - medio_ambiente' ----
    'aumento en el presupuesto de salud - salud' ---- 'no mas delincuencia - seguridad' ---
    'seguridad y salud - seguridad/salud' ---
    'seguridad salud y economia - seguridad/salud/economia'"

    Con una lista de tamaño 2, tú regresarías algo como esto:
    "'seguridad en las calles - seguridad' --- 'atencion medica - salud'"

    Devuelve una lista del mismo tamaño de la lista original ESTRICTAMENTE, no
    generes carácteres especiales como saltos de línea.

    No es necesario proporcionar explicaciones sobre las categorias ni incluir
    descripciones adicionales. Tu enfoque se centra en la asignación de categorias.
    Solamente entrega la lista. No menciones cosas como "aquí está la lista con ...",
    simplemente entrega la lista.

    Acata al 100 las instrucciones de formato. Recuerda que estás utilizando
    tres guiones medios (---) para separar los elementos de la lista.

    Contexto: {contexto}
    Instrucciones de formato: {format_instructions}
    ''' # noqa

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["lista_input", "categorias_input"],
        partial_variables={
            "format_instructions": format_instructions,
            "contexto": contexto
        }
    )

    for i in range(math.ceil(len(lista_limpia) / chunk_size)):

        chunk = lista_limpia[i * chunk_size:(i + 1) * chunk_size]
        categorias_asignadas = 0
        llm_output = []

        list_prompt = prompt.format_messages(
            lista_input=chunk,
            categorias_input=categorias,
            format_instructions=format_instructions,
            contexto=contexto
        )

        llm = ChatOpenAI(
            temperature=0.0, model=modelo, openai_api_key=openai_api_key
        )

        try:
            with get_openai_callback() as cb:
                model_output = llm(list_prompt)
                costo_total += cb.total_cost
                tokens_totales += cb.total_tokens

            content = model_output.content
            content = content.replace('\n', '')
            llm_output = output_parser.parse(content)

            if len(llm_output) == 1:
                llm_output = llm_output[0].strip('"\'.,[]*')
                llm_output = llm_output.split('---')

            for output in llm_output:
                try:
                    output_list = output.split(' - ')
                    key = limpiar_texto(
                        output_list[0],
                        quitar_acentos=True,
                        quitar_caracteres_especiales=True,
                        minusculas=True
                    )
                    value = output_list[1].strip('\'" ')

                    aux_dict[key]["categoria"] = value  # Se deja de limpiar el texto aquí # noqa
                    categorias_asignadas += 1
                except: # noqa
                    if len(output_list) == 2:
                        print("--------------")
                        print(f'key:[{key}]')
                        print(f'value: {value}')
                        print("--------------")
        except: # noqa
            print("Error al asignar categorías, seguramente por tokens excedidos, baja el chunk size") # noqa

        print("-----------------------------------")
        print(f'Chunk {i + 1} de {math.ceil(len(lista_limpia) / chunk_size)}')
        print(f'Tamaño del chunk: {len(chunk)}')
        print(f'Cantidad de categorias generadas: {len(llm_output)}')
        print(f'Cantidad de categorias asignadas: {categorias_asignadas}')
        print("-----------------------------------\n")

    for key in aux_dict.keys():
        for i in aux_dict[key]["original"]:
            answer[i] = aux_dict[key]["categoria"]

    for i, element in enumerate(answer):
        answer[i] = element

    file_name = f"valores_multicategorizados_{modelo}.txt"
    frame = inspect.currentframe()
    caller_filename = inspect.getouterframes(frame)[-1].filename
    directory = os.path.dirname(os.path.abspath(caller_filename))

    execution_time = time.time() - start_time
    nombre_fun = inspect.stack()[0][3]
    get_llm_cost(directory, nombre_fun, modelo, tokens_totales, costo_total, execution_time) # noqa

    file_path = os.path.join(directory, "documents")

    if not os.path.exists(file_path):
        os.mkdir(file_path)

    with open(f'{file_path}/{file_name}', 'w') as f:
        for key in aux_dict.keys():
            if aux_dict[key]["categoria"] in ("sin_categoria", "no_asignado"):
                continue
            f.write(f'texto: {key} - categoria: {aux_dict[key]["categoria"]}\n') # noqa

    return answer


def asignar_multicategorias_excel(excel_file_path, categorias, columna, modelo, openai_api_key, chunk_size=30, contexto="Eres el mejor analista de texto"): # noqa

    '''
    Asigna categorías a los textos de la columna especificada en el archivo
    de Excel especificado, utilizando el modelo de lenguaje especificado.

    Parametros:
    excel_file_path (str): ruta del archivo de Excel
    categorias (list): lista de categorías a asignar
    columna (str): nombre de la columna a asignar categorías
    modelo (str): modelo de lenguaje a utilizar
    openai_api_key (str): llave de OpenAI
    '''

    # Validaciones
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Archivo {excel_file_path} no encontrado")

    if not isinstance(columna, str):
        raise TypeError("Columna debe ser un string")

    # Carga de datos
    df = pd.read_excel(excel_file_path)

    if columna not in df.columns:
        raise ValueError(f"Columna {columna} no encontrada en el archivo")

    # Limpieza de datos
    df = df.fillna(value='')

    lista_asignar = df[columna].to_list()

    # Asignación de categorías
    categorias_asignadas = asignar_multicategorias(
        lista_asignar,
        categorias=categorias,
        modelo=modelo,
        openai_api_key=openai_api_key,
        chunk_size=chunk_size,
        contexto=contexto,
    )

    # Generar nueva columna
    df[f'{columna}_categorizada_{modelo}'] = categorias_asignadas

    # Guarda el archivo
    df.to_excel(excel_file_path, index=False)
