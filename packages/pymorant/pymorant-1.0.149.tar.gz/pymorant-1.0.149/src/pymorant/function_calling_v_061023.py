import json
import openai
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage, ChatMessage, SystemMessage
from pymorant import asignar_categorias

tools = [
    {
        "name": "get_message_info",
        "description": "Devuelve un resumen del texto recibido con una estructura definida.", # noqa
        "parameters": {
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "El nombre de la persona que envía el mensaje e.g. Juan, Pedro, Fernando.", # noqa
                },
                "ubicacion": {
                    "type": "string",
                    "description": "La ubicación donde vive la persona e.g. Tuxtla Gutierrez, Chalco, Tonalá, Tapachula", # noqa
                },
                "solicitud": {
                    "type": "string",
                    "description": "La solicitud/petición de la persona e.g necesito comentarle que quisiera unirme al apoyo del movimiento, quiero decirle que hay problemas en el municipio de inseguridad y etc.", # noqa
                },
                "categoria_solicitud":{
                  "type": "string",
                  "description": "La categoría de la solicitud proporcionada. e.g servicios_publicos, seguridad, infraestructura, educación."
                  
                },
                "urgencia": {
                    "type": "string",
                    "description": '''La urgencia de la solicitud de la persona e.g. alta, media, baja.
                  '''
                }
            },
            "required": ["solicitud"],
        },
    },
]

categoria_solicitudes = ["servicios_publicos","salud","seguridad",
                         "infraestructura","educacion","economia",
                         "temas_personales"]

cats_urgencia = ["alta","media","baja"]
                
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
'''                   

prompt_second_response = '''

    Tu papel como analista de texto es ser el asistente personal encargado de 
    leer y analizar mensajes recibidos de una persona. Tu objetivo principal es
    proporcionar respuestas lógicas y coherentes basadas en los resultados 
    generados por el function calling. En ningún caso debes inventar información
    ni agregar detalles adicionales lo recibido del function_calling.

    Por ejemplo, no inventes comentarios adicionales a la solicitud de las 
    personas.

    El cuerpo de tu resumen debe de ser de la siguiente manera:

    e.g.
    - *Remitente*: Jorge.\n
    -------------------------------------------------------\n
    - *Municipio*: Tapachula. \n
    -------------------------------------------------------\n
    - *Solicitud/Petición*: \n\n En su mensaje, se observa
    que está expresando su interés en apoyar al movimiento
    ya que busca abordar las irregularidades en el sistema
    educativo de su municipio y trabajar hacia una solución más justa e
    igualitaria. Manifiesta su deseo de participar en este proyecto y está
    dispuesto a discutir más formas de cómo podría contribuir a este cambio con 
    usted.
    -------------------------------------------------------\n
    - *Tipo_solicitud*: Infraestructura.
    -------------------------------------------------------\n
    - *Urgencia*: Media.

    No olvides que aunque no te proporcionen el nombre, ubicación o urgencia, 
    debes mencionar que no los proporcionó la persona que envía el mensaje o 
    que los prefirió mantener de forma anónima/desconocida.
'''

class SolicitudInfo:

      def __init__(self, openai_api_key, modelo="gpt-4"):
            self.openai_api_key = openai_api_key
            openai.api_key = openai_api_key
            self.modelo = modelo
            self.TOOLS = tools
            self.PROMPT_SECOND_RESPONSE = prompt_second_response
            self.categoria_solicitudes = categoria_solicitudes
            self.instrucciones_cat_urgencia = instrucciones_cat_urgencia
            self.cats_urgencia = cats_urgencia

      def get_message_info(self, nombre, ubicacion, solicitud, categoria_solicitud, urgencia):
    
            output = f"El mensaje lo envía la persona: {nombre}.\
            La persona proviene de: {ubicacion}.\
            La solicitud/petición que realiza es la siguiente:\
            {solicitud}.\
            El tipo de solicitud es: {categoria_solicitud}.\
            La urgencia de la solicitud es: {urgencia}."
    
            return json.dumps(output)

      def answer(self, mensaje, chat_history = []):
        
            categoria_solicitud = asignar_categorias(lista_asignar = [mensaje],
                                                     categorias = self.categoria_solicitudes,
                                                     modelo = self.modelo,
                                                     openai_api_key = self.openai_api_key,
                                                     )
            
            categoria_urgencia = asignar_categorias(lista_asignar = [mensaje],
                                                    categorias = self.cats_urgencia,
                                                    modelo = self.modelo,
                                                    openai_api_key = self.openai_api_key,
                                                    contexto = self.instrucciones_cat_urgencia)
                                                    
            mensaje_completo = f'''tipo de solicitud: {categoria_solicitud[0]}. \n\n 
                                urgencia: {categoria_urgencia[0]}. \n\n 
                                {mensaje}'''
            
            response = openai.ChatCompletion.create(
                temperature=0,
                model=self.modelo,
                messages=[{"role": "user", "content": str(chat_history)},
                          {"role": "user", "content": mensaje_completo}],
                functions=self.TOOLS,
                )

            message = response["choices"][0]["message"]

            function_call = message.get("function_call")

            if function_call["arguments"] != "{}":
                  function_name = function_call["name"]
                  nombre = json.loads(function_call["arguments"]).get("nombre")
                  ubicacion = json.loads(function_call["arguments"]).get("ubicacion") # noqa
                  solicitud = json.loads(function_call["arguments"]).get("solicitud") # noqa
                  solicitud_categoria = json.loads(function_call["arguments"]).get("categoria_solicitud") # noqa
                  urgencia = json.loads(function_call["arguments"]).get("urgencia") # noqa
                  function_response = self.get_message_info(
                      nombre=nombre,
                      ubicacion=ubicacion,
                      solicitud=solicitud,
                      categoria_solicitud=categoria_solicitud,
                      urgencia = urgencia
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
              
                  ans = second_response["choices"][0]["message"].content
                  # ans = json.loads(second_response["choices"][0]["message"].content)

                  return ans
            return '''Como requisito mínimo se necesita que proporciones un 
            mensaje lógico con una petición o solicitud. Vuelve a intentarlo, 
            por favor. No tengo permitido responder nada fuera del contexto de 
            análisis de mensajes.
            '''

###############################################################################
##########----------------PRUEBAS REALIZADAS--------------#####################
# mensaje = '''Me gustaría discutir el tema de los programas sociales y su
# impacto en nuestras comunidades. ¿Qué opina sobre discutir estos programas en
# una cena mañana?
# '''

# mensaje = '''ola, yo quiero ver si tengo la oprtunidad de platicarle que un
# grupo de personas y yo estamos interesados en apoyar de mas formas al movimiento
# de transformacion. Digame si tiene un rato libre esta semana para ponernos de
# acuerdo.
# '''

# mensaje = '''Mi nombre es Jorge, y soy residente de San Cristóbal de las Casas.
# He estado siguiendo de cerca el desarrollo de nuestro municipio y no puedo
# evitar notar ciertas irregularidades electorales que han surgido en los últimos
# tiempos. Es por eso que me dirijo a usted de una manera respetuosa para
# expresar mi interés en unirme al apoyo del movimiento y trabajar hacia un
# proceso electoral más justo y equitativo en mi municipio.
# '''

# api_key = "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"

# categoria_solicitudes = ["servicios_publicos","salud","seguridad",
#                          "infraestructura","educacion","economia",
#                          "temas_personales"]
                         
# categoria_solicitud = asignar_categorias(lista_asignar = [mensaje],
#                                          categorias = categoria_solicitudes,
#                                          modelo = "gpt-4",
#                                          openai_api_key = api_key,
#                                          )
# print(categoria_solicitud[0])
# 
# instrucciones_cat_urgencia = '''Eres el mejor analista de texto y debes de categorizar\
# la urgencia de las solicitudes de un político basándote en las siguientes indicaciones: \
#   alta:
# 
#     Situaciones que requieren atención en el corto plazo.
#     Pueden afectar la productividad o la satisfacción del cliente.
#     Ejemplos incluyen: una falla en un sistema importante, una solicitud de un cliente importante, o una entrega de proyecto que se aproxima a su fecha límite.
#                   
#   media:
# 
#     Situaciones que requieren atención pero no son urgentes.
#     Pueden ser programadas entre otras tareas.
#     Ejemplos incluyen: solicitudes de mejora, soporte técnico no crítico, o consultas generales.
#   
#   baja:
# 
#     Situaciones que no requieren atención inmediata.
#     Pueden ser programadas a largo plazo o cuando hay disponibilidad de recursos.
#     Ejemplos incluyen: solicitudes de información no urgentes, tareas de mantenimiento rutinario, o proyectos futuros.
# '''
#   
# cats_urgencia = ["alta","media","baja"]
# 
# categoria_urgencia = asignar_categorias(lista_asignar = [mensaje],
#                                         categorias = cats_urgencia,
#                                         modelo = "gpt-4",
#                                         openai_api_key = api_key,
#                                         contexto = instrucciones_cat_urgencia)
# print(categoria_urgencia[0])

# solicitud_info = SolicitudInfo(openai_api_key=api_key, modelo="gpt-4")

# mensaje_completo = f'''tipo de solicitud: {categoria_solicitud[0]}. \n\n
#                         urgencia: {categoria_urgencia[0]}. \n\n
#                         {mensaje}'''

# respuesta_1 = solicitud_info.answer(mensaje=mensaje_completo)
# print(respuesta_1)

# respuesta_1 = solicitud_info.answer(mensaje=mensaje)
# print(respuesta_1)






# z_1 = get_solicitud(respuesta_1)
# print(z_1)
# 
# aux_mensaje_1 = "Pedro"
# 
# mensaje_2 = f"{aux_mensaje_1} {z_1}"
# 
# respuesta_2 = solicitud_info.answer(mensaje = mensaje_2)
# print(respuesta_2)
# 
# z_2 = get_solicitud(respuesta_2)
# print(z_2)
# 
# aux_mensaje_2 = "De mi rancho"
# 
# mensaje_3 = f"{aux_mensaje_2} {z_2}"
# 
# respuesta_3 = solicitud_info.answer(mensaje = mensaje_3)
# print(respuesta_3)
# 
# z_3 = get_solicitud(respuesta_3)
# print(z_3)
# 
# aux_mensaje_3 = "De Cholula"
# 
# mensaje_4 = f"{aux_mensaje_3} {z_3}"
# 
# respuesta_4 = solicitud_info.answer(mensaje = mensaje_4)
# print(respuesta_4)
# 
# z_4 = get_solicitud(respuesta_4)
# print(z_4)
# 
# 
# 
# 
# 
