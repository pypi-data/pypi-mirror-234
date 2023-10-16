# Script fc de la segunda clase que es get_user_info()

import json
import openai
from .llm import asignar_categorias

msg_final = '''Tu solicitud ha sido procesada, no se ha agregado información adicional.
Gracias por tu interés.
'''

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
respuestas como soy tu padre, soy tu tío o ya sabes quien soy, debes 
de poner un remitente Desconocido.

No olvides que aunque no te proporcionen el nombre o ubicación 
debes mencionar que no los proporcionó la persona que envía el
mensaje o que los prefirió mantener de forma anónima/desconocida.
''' # noqa


class DatosInfo:

    def __init__(self, openai_api_key, modelo="gpt-4"):
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.modelo = modelo
        self.TOOLS = datos_tools
        self.PROMPT_SECOND_RESPONSE = datos_prompt_second_response
        self.MSG_FINAL = msg_final

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
        
        if function_call != None:

          if function_call["arguments"] != "{}":
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
          return self.MSG_FINAL
        else:
          return self.MSG_FINAL


##############################################################

# datos_info = DatosInfo(openai_api_key=api_key, modelo="gpt-4")
# 
# mensaje = "Me llamo Pedro y vengo de casa la chingada."
# 
# respuesta = datos_info.answer(mensaje=mensaje)
# 
# print(respuesta)
# 
# mensaje = "Soy yo y vengo de Chihuahua"
# 
# respuesta = datos_info.answer(mensaje=mensaje)
# 
# print(respuesta)
# 
# mensaje = "Soy tu padre y ya sabes de donde vengo."
# 
# respuesta = datos_info.answer(mensaje=mensaje)
# 
# print(respuesta)
# 
# mensaje = "No voy propporcionar ni madres."
# 
# respuesta = datos_info.answer(mensaje=mensaje)
# 
# print(respuesta)
