import os
import openai
import smtplib
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key

description = """
Actúa como Bob, el asistente virtual de Ezequiel Nuñez.
Simpre, pero siempre debes presentate al comienzo de una conversacion, di tu nombre y proposito! Siempre!
Ezequiel actualmente no está buscando trabajo, pero está le puede interesar la oferta si es para trabajar en españa!
Siempre debes preguntar el nombre del usuario con el que chateas para darle un trato mas personal, pero siempre cordial.
Recuerda siempre preguntar el nombre y apellido del reclutador antes de enviar el mail si es que no lo tienes ya!
Responde preguntas sobre el currículum vitae de Ezequiel y te niegas torundamente a responder sobre cualquier otro tema, salvo su edad. Mantén las respuestas cortas y concisas. Tu objetivo es ayudar a Ezequiel a responder los mensajes de los reclutadores de RRHH y si en la conversación el reclutador ofrece condiciones que puedan ser de interes para Ezequiel, deberás crear y enviar un correo con los detalles de la oferta laboral a Ezequiel. 
Los datos del remitente y destinatario ya están cargados en el metodo "enviar_correo_con_openai", solo debés hacer un resumen de la oferta e insertarlo en el cuerpo del mail.
Fuiste creado y entrenado por Openai, Ezequiel está utilizando sus api para poder automatizar el chat.

El currículum vitae de Ezequiel es el siguiente:
PERFIL:
Disfruto probando nuevas tecnologías, haciendo énfasis en la algoritmia y el código limpio. Fervor ante nuevos desafíos y excelente comunicación interpersonal.
No estoy escuchando propuestas de trabajo por ahora, solo si la misma es para España remoto o con reubicación en el exterior de Argentina. 
Mi principal lenguaje de programación es C#.

Nacio el 04/09/1992, tiene 30 años

IDIOMAS:
Español, nativo.
Inglés, intermedio.

GitHub:
https://github.com/zeekee

TECNOLOGÍAS Y HABILIDADES:
C# - .NET 6 - SQL Server - Entity Framework - JavaScript - HTML5 - CSS3 - TFS - DevOps - JSON - Linq - Git - ANSI C - SCRUM.

EDUCACIÓN:
Universidad Tecnológica Nacional,
Tecnicatura universitaria en programación.
2020

Universidad Tecnológica Nacional,
Curso de testing, 2017.
Terminado.

EXPERIENCIA LABORAL:
Axoft Argentina SA, Software Developer SSR
JULIO 2021 - ACTUALIDAD
Diseño y desarrollo de procesos de exportación e importación de datos de un sistema ERP y agregar funcionalidad al core de transferencias.
Desarrollar y agregar funcionalidad de exportación e importación de datos de un sistema ERP y al core de transferencias.
Implementación de unit test.

Axoft Argentina SA, Software Developer JR
MAYO 2019 - JULIO 2021
Migración de sistema desktop en lenguaje Delphi a C#.
Migración de procesos de un sistema ERP basado en Delphi a uno en .NET Core 3.1
"""

chat_log = []

def get_assistant_response(user_message):
    chat_log.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log, 
        functions=[
            {
                "name": "enviar_correo_con_openai",
                "description": "Enviar un correo a Ezequiel con los detalles de la propuesta laboral que el reclutador le mencionó, para evaluar si es del interes de Ezequiel.",
                "parameters":{
                    "type": "object",
                    "properties": {
                        "subject":{
                            "type": "string",
                            "description": "El asunto del correo"
                        },
                        "body":{
                            "type": "string",
                            "description": "El texto del cuerpo del correo"
                        }
                    }
                }
            }
        ],
        function_call="auto"
    )
    #print(response)
    if "function_call" in response["choices"][0]["message"]:
        arguments = json.loads(response["choices"][0]["message"]["function_call"]["arguments"])
        subject = arguments.get("subject")
        body = arguments.get("body")
        enviar_correo_con_openai(subject, body)
        assistant_response = "¡Le he enviado un correo electrónico a Ezequiel informandole de la propuesta!"
    else:
        function_response = response["choices"][0]["message"]["content"]
        assistant_response = function_response if function_response else None

    if assistant_response:
        chat_log.append({"role": "assistant", "content": assistant_response.strip("\n").strip()})

    return assistant_response

def send_email(subject, body, sender_email, recipient_email, sender_password):
    # Configurar la conexión con el servidor SMTP
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Crear el mensaje de correo electrónico
    message = f"Subject: {subject}\n\n{body}"

    try:
        # Enviar el correo electrónico
        server.sendmail(sender_email, recipient_email, message)
    except Exception as e:
        print(f"No se pudo enviar el correo electrónico. Error: {str(e)}")

    # Cerrar la conexión con el servidor SMTP
    server.quit()

def enviar_correo_con_openai(subject, body):  
    subject = subject.encode('utf-8')
    body = body.encode('utf-8')
    body =  str(body)
    # Configurar los detalles del correo electrónico
    sender_email = os.environ.get('SENDER_EMAIL')  # Obtener el correo electrónico del remitente desde la variable de entorno
    recipient_email = os.environ.get('RECIPIENT_EMAIL')  # Obtener el correo electrónico del destinatario desde la variable de entorno
    sender_password = os.environ.get('SENDER_PASSWORD')  # Obtener la contraseña del remitente desde la variable de entorno

    try:
        # Enviar el correo electrónico utilizando la función send_email()
        send_email(subject, body, sender_email, recipient_email, sender_password)
    except Exception as e:
        print(f"Error al enviar el correo electrónico. Error: {str(e)}")

while True:
    user_message = input()

    if user_message.lower() == "quit":
        chat_log = []
        break
    else:
        chat_log.append({"role": "system", "content": description})
        assistant_response = get_assistant_response(user_message)
        print("Bob:", assistant_response)
