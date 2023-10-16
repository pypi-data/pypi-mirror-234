import json
import openai
# from pymorant import asignar_categorias
from .llm import asignar_categorias

tools = [{
    "name": "get_message_info",
    "description": "Devuelve un resumen del texto recibido con una estructura definida.",  # noqa
    "parameters": {
        "type": "object",
        "properties": {
            "nombre": {
                "type": "string",
                "description": "El nombre de la persona que envía el mensaje e.g. Juan, Pedro, Fernando.",  # noqa
            },
            "ubicacion": {
                "type": "string",
                "description": "La ubicación donde vive la persona e.g. Tuxtla Gutierrez, Chalco, Tonalá, Tapachula",  # noqa
            },
            "solicitud": {
                "type": "string",
                "description": "La solicitud/petición de la persona e.g necesito comentarle que quisiera unirme al apoyo del movimiento, quiero decirle que hay problemas en el municipio de inseguridad y etc.",  # noqa
            },
            "categoria_solicitud": {
                "type": "string",
                "description": "La categoría de la solicitud proporcionada. e.g servicios_publicos, seguridad, infraestructura, educación." # noqa

            },
            "urgencia": {
                "type": "string",
                "description": "La urgencia de la solicitud de la persona e.g. alta, media, baja." # noqa
            }
        },
        "required": ["solicitud"],
    }
}]

categoria_solicitudes = [
    "servicios_publicos",
    "salud",
    "seguridad",
    "infraestructura",
    "educacion",
    "economia",
    "temas_personales"
]

categorias_urgencia = [
    "alta",
    "media",
    "baja"
]

instrucciones_cat_urgencia = '''Eres el mejor analista de texto y debes de categorizar
la urgencia de las solicitudes de un político basándote en las siguientes indicaciones:

alta:
Situaciones que requieren atención en el corto plazo.
Pueden afectar la productividad o la satisfacción del cliente.
Ejemplos incluyen: una falla en un sistema importante, una solicitud de un cliente importante, o una entrega de proyecto que se aproxima a su fecha límite.
   
media:
Situaciones que requieren atención pero no son urgentes.
Pueden ser programadas entre otras tareas.
Ejemplos incluyen: solicitudes de mejora, soporte técnico no crítico, o consultas generales.

baja:
Situaciones que no requieren atención inmediata.
Pueden ser programadas a largo plazo o cuando hay disponibilidad de recursos.
Ejemplos incluyen: solicitudes de información no urgentes, tareas de mantenimiento rutinario, o proyectos futuros.
''' # noqa

prompt_second_response = ''' Tu papel como analista de texto es ser el asistente personal encargado de
leer y analizar mensajes recibidos de una persona. Tu objetivo principal es
proporcionar respuestas lógicas y coherentes basadas en los resultados
generados por el function calling. En ningún caso debes inventar información
ni agregar detalles adicionales lo recibido del function_calling.

Por ejemplo, no inventes comentarios adicionales a la solicitud de las
personas.

Remitente es quien te está escribiendo el mensaje, el texto puede hablar
de otras personas, pero a ti te interesa guardar en Remitente solamente
a la persona que te escribe la solicitud.

Si te escriben: Felipe quiere saber que pasó con la coladera abierta en
su colonia. No está dando su nombre el remitente, sino que solo esta 
expresando que Felipe quiere saber que pasó con la coladera abierta, pero
el nombre del remitente no aparece en ese texto. En este ejemplo, no 
guardarás ningún Remitente. Es decir, en este ejemplo regresarás como
output:
  {
        "Remitente": "",
        "Ubicación": "",
        "Solicitud/Petición": "En su mensaje, se puede observar que el usuario está
        expresando su interés por saber que sucedió con la coladera abierta de su colonia."
        "Tipo_solicitud": "Infraestructura",
        "Urgencia": "Media"
      }
      
EN GENERAL,       

El output que debes entregar debe ser de la siguiente manera:

      {
        "Remitente": "Jorge",
        "Ubicación": "Tapachula",
        "Solicitud/Petición": "En su mensaje, se puede observar que Jorge está
        expresando su interés en apoyar al movimiento ya que busca abordar las
        irregularidades en el sistema educativo de su municipio y trabajar
        hacia una solución más justa e igualitaria. Jorge subraya la importancia de
        la colaboración y un enfoque inclusivo para lograr este objetivo.
        Además, manifiesta su deseo de participar activamente en este proyecto.
        Se observa que Jorge está dispuesto a discutir más formas de cómo
        podría contribuir a este cambio positivo con usted."
        "Tipo_solicitud": "Infraestructura",
        "Urgencia": "Alta"
      }

''' # noqa


class SolicitudInfo:

    def __init__(self, openai_api_key, modelo="gpt-4"):
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.modelo = modelo
        self.TOOLS = tools
        self.PROMPT_SECOND_RESPONSE = prompt_second_response
        self.categoria_solicitudes = categoria_solicitudes
        self.instrucciones_cat_urgencia = instrucciones_cat_urgencia
        self.categorias_urgencia = categorias_urgencia

    def get_message_info(self, nombre, ubicacion, solicitud, categoria_solicitud, urgencia): # noqa

        output = f"El mensaje lo envía la persona: {nombre}.\
            La persona proviene de: {ubicacion}.\
            La solicitud/petición que realiza es la siguiente:\
            {solicitud}.\
            El tipo de solicitud es: {categoria_solicitud}.\
            La urgencia de la solicitud es: {urgencia}."

        return json.dumps(output)

    def answer(self, mensaje, chat_history=[]):

        categoria_solicitud = asignar_categorias(
            lista_asignar=[mensaje],
            categorias=self.categoria_solicitudes,
            modelo=self.modelo,
            openai_api_key=self.openai_api_key
        )

        categoria_urgencia = asignar_categorias(
            lista_asignar=[mensaje],
            categorias=self.categorias_urgencia,
            modelo=self.modelo,
            openai_api_key=self.openai_api_key,
            contexto=self.instrucciones_cat_urgencia
        )

        mensaje_completo = f'''tipo de solicitud: {categoria_solicitud[0]}. \n\n
                                urgencia: {categoria_urgencia[0]}. \n\n
                                {mensaje}''' # noqa

        response = openai.ChatCompletion.create(
            temperature=0,
            model=self.modelo,
            messages=[
                {
                    "role": "user",
                    "content": str(chat_history)
                },
                {
                    "role": "user",
                    "content": mensaje_completo
                }
            ],
            functions=self.TOOLS,
        )

        message = response["choices"][0]["message"]

        function_call = message.get("function_call")

        if function_call is not None and function_call["arguments"] != "{}":
            function_name = function_call["name"]
            nombre = json.loads(function_call["arguments"]).get("nombre")
            ubicacion = json.loads(function_call["arguments"]).get("ubicacion")  # noqa
            solicitud = json.loads(function_call["arguments"]).get("solicitud")  # noqa
            solicitud_categoria = json.loads(function_call["arguments"]).get("categoria_solicitud")  # noqa
            urgencia = json.loads(function_call["arguments"]).get("urgencia")  # noqa
            function_response = self.get_message_info(
                nombre=nombre,
                ubicacion=ubicacion,
                solicitud=solicitud,
                categoria_solicitud=categoria_solicitud,
                urgencia=urgencia
            )

            second_response = openai.ChatCompletion.create(
                temperature=0,
                model=self.modelo,
                messages=[
                    {
                        "role": "user", "content": str(chat_history)
                    },
                    {
                        "role": "system",
                        "content": self.PROMPT_SECOND_RESPONSE
                    },
                    {
                        "role": "user", "content": mensaje_completo
                    },
                    message,
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    },
                ],
            )
            ans = json.loads(second_response["choices"][0]["message"].content)
            return ans
        return None


datos_tools = [{
    "name": "get_user_info",
    "description": "Devuelve un resumen del texto recibido con una estructura definida.",  # noqa
    "parameters": {
        "type": "object",
        "properties": {
            "nombre": {
                "type": "string",
                "description": "El nombre de la persona que envía el mensaje e.g. Juan, Pedro, Fernando.",  # noqa
            },
            "ubicacion": {
                "type": "string",
                "description": "La ubicación donde vive la persona e.g. Tuxtla Gutierrez, Chalco, Tonalá, Tapachula",  # noqa
            }
        }
    }
}]

datos_prompt_second_response = ''' Tu papel como analista de texto es ser el asistente personal encargado de
leer y analizar mensajes recibidos de una persona. Tu objetivo principal es
proporcionar respuestas lógicas y coherentes basadas en los resultados
generados por el function calling. En ningún caso debes inventar información
ni agregar detalles adicionales lo recibido del function_calling.

Por ejemplo, no inventes comentarios adicionales a la solicitud de las
personas.

El output que debes entregar debe ser de la siguiente manera:

      {
        "Remitente": "Jorge",
        "Ubicación": "Tapachula"
      }
      
Si en ubicación te proporcionan información como: vengo de mi casa,
vengo de mi rancho, vengo de casa la chingada ni frases similares.

Recuerda que como Remitente debe de ser un nombre propio, si recibes
respuestas como soy tu padre, soy tu tío o ya sabes quien soy, debes ignorar
la respuesta.

Si no identificas el nombre regresa ''

Si no identificas la ubicación regresa ''

''' # noqa


class DatosInfo:

    def __init__(self, openai_api_key, modelo="gpt-4"):
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.modelo = modelo
        self.TOOLS = datos_tools
        self.PROMPT_SECOND_RESPONSE = datos_prompt_second_response

    def get_user_info(self, nombre, ubicacion): # noqa

        output = f"El mensaje lo envía la persona: {nombre}.\
            La persona proviene de: {ubicacion}."

        return json.dumps(output)

    def answer(self, mensaje, chat_history=[]):

        response = openai.ChatCompletion.create(
            temperature=0,
            model=self.modelo,
            messages=[
                {
                    "role": "user",
                    "content": str(chat_history)
                },
                {
                    "role": "user",
                    "content": mensaje
                }
            ],
            functions=self.TOOLS,
        )

        message = response["choices"][0]["message"]

        function_call = message.get("function_call")

        if function_call is not None and function_call["arguments"] != "{}":
            function_name = function_call["name"]
            nombre = json.loads(function_call["arguments"]).get("nombre")
            ubicacion = json.loads(function_call["arguments"]).get("ubicacion")  # noqa

            function_response = self.get_user_info(
                nombre=nombre,
                ubicacion=ubicacion
            )

            second_response = openai.ChatCompletion.create(
                temperature=0,
                model=self.modelo,
                messages=[
                    {
                        "role": "user", "content": str(chat_history)
                    },
                    {
                        "role": "system",
                        "content": self.PROMPT_SECOND_RESPONSE
                    },
                    {
                        "role": "user", "content": mensaje
                    },
                    message,
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    },
                ],
            )
            ans = json.loads(second_response["choices"][0]["message"].content)
            return ans
        return None
