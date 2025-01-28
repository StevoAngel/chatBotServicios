from flask import Flask, request, jsonify
import random
import re

app = Flask(__name__)

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
    return unknown() if highestProbability[bestMatch] < 1 else bestMatch

def unknown():
    return random.choice(["Lo siento, no entendí esa pregunta. ¿Puedes reformularla?", "Revisa la pregunta, por favor", "Intenta nuevamente, por favor"])

def messageProbability(userMessage, recognizedWords, singleResponse, requiredWords=[]):
    messageCertainty = 0
    hasRequiredWords = True

    for word in userMessage:
        if word in recognizedWords:
            messageCertainty += 1

    percentage = float(messageCertainty) / float(len(recognizedWords)) if recognizedWords else 0

    for word in requiredWords:
        if word not in userMessage:
            hasRequiredWords = False
            break

    if hasRequiredWords or singleResponse:
        return int(percentage * 100)
    else:
        return 0

@app.route('/chatbot', methods=['POST'])
def chatbot():
    userInput = request.json.get("message")
    splitMessage = re.split(r'\s|[,:;.?!¿¡-]\s*', userInput.lower())
    response = checkAllMesagges(splitMessage)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
