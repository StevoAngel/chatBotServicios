import streamlit as st
import re
import random

# Funciones del chatbot
def checkAllMesagges(message):
    highestProbability = {}

    def response(botResponse, listOfWords, singleResponse=False, requiredWords=[]):
        nonlocal highestProbability
        highestProbability[botResponse] = messageProbability(message, listOfWords, singleResponse, requiredWords)

    response("¡Hola! Soy tu asistente virtual. ¿Cómo puedo ayudarte hoy?",
             ["hola", "buenas", "tardes", "buen", "día", "noches", "saludos", "que", "tal", "como", "estas"], False)
    response("¡Perfecto! ¿Podrías decirme cuál es el nombre del servicio que deseas pagar? (Ejemplo: luz, agua, internet)",
             ["pagar", "pago", "pagos"], False)
    response("¡Muy bien! Te ayudaré a obtener tu estado de cuenta, por favor indícame tu cuenta CLABE o número de cliente y tu clave secreta",
             ["estado", "cuenta", "bancario", "banco"], False)
    response(f"Tu saldo al día de hoy es de ${round(random.uniform(1000, 10000), 2)} MXN, tu última compra fue por: ${round(random.uniform(100, 800), 2)} MXN",
             ["cliente", "clabe", "secreta", "clave"], False)
    response("¡Gracias! Ingresa por favor el número de servicio que se encuentra en tu recibo del servicio",
             ["agua", "luz", "internet"], False)
    response("¡Gracias! El monto a pagar por este servicio es: $150.00 MXN. ¿Deseas continuar?",
             ["numero"], False, ["numero"])
    response("¡Listo! Tu pago de $150.00 MXN para el servicio se ha realizado con éxito. ¡Gracias por usar nuestro servicio!",
             ["si", "continuar", "adelante", "sigue", "yes"], True, ["si"])
    response("Entendido, vamos a empezar de nuevo. ¿Qué servicio te gustaría pagar?",
             ["no", "negativo", "mal", "error"], True, ["no"])
    response("Claro, aquí tienes más detalles sobre los servicios:\n- Luz: Paga tu factura de electricidad.\n- Agua: Paga tu factura de agua.\n- Internet: Paga tu servicio de conexión a Internet.",
             ["info", "informacion", "acerca", "de"], False)
    response("¡Adiós! Gracias por usar nuestro servicio. ¡Que tengas un buen día!",
             ["adios", "gracias", "por", "todo", "hasta", "luego", "bye", "thanks", "thank"])

    bestMatch = max(highestProbability, key=highestProbability.get)
    return unknownQuestion() if highestProbability[bestMatch] < 1 else bestMatch


def unknownQuestion():
    response = ["Lo siento, no entendí esa pregunta. ¿Puedes reformularla?",
                "Revisa la pregunta, por favor", "Intenta nuevamente, por favor"][random.randrange(3)]
    return response


def getResponse(userInput):
    splitMessage = re.split(r'\s|[,:;.?!¿¡-]\s*', userInput.lower())
    return checkAllMesagges(splitMessage)


def messageProbability(userMessage, recognizedWords, singleResponse, requiredWord=[]):
    messageCertainty = 0
    hasRequiredWords = True

    for word in userMessage:
        if word in recognizedWords:
            messageCertainty += 1

    percentage = float(messageCertainty) / float(len(recognizedWords))

    for word in requiredWord:
        if word not in userMessage:
            hasRequiredWords = False
            break

    return int(percentage * 100) if hasRequiredWords or singleResponse else 0

# Aplicación con Streamlit
st.title("Chatbot Para Consultas Bancarias o Pagos de Servicios")
st.write("Bienvenido, soy tu asistente virtual. ¡Hablemos!")

# Mantener historial de conversación
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar historial de mensajes
chat_container = st.container()
with chat_container:
    for msg in st.session_state["messages"]:
        st.markdown(f"**Tú:** {msg['user']}")
        st.markdown(f"**Bot:** {msg['bot']}")

# Entrada del usuario con formulario para borrar automáticamente
with st.form(key="user_input_form", clear_on_submit=True):
    user_input = st.text_input("Escribe tu mensaje aquí:")
    submit_button = st.form_submit_button(label="Enviar")

if submit_button and user_input:
    # Respuesta del chatbot
    bot_response = getResponse(user_input)
    # Actualizar historial
    st.session_state["messages"].append({"user": user_input, "bot": bot_response})
    # Recargar el contenedor automáticamente para que el cuadro de diálogo se mantenga actualizado
    chat_container.empty()
    with chat_container:
        for msg in st.session_state["messages"]:
            st.markdown(f"**Tú:** {msg['user']}")
            st.markdown(f"**Bot:** {msg['bot']}")

