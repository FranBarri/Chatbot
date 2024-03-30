import cv2
import os
import time
from shutil import copyfile
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Crear el chatbot bancario y entrenarlo
bot = ChatBot("Chatbot bancario")
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.spanish")
trainer.train("./data")

print("Bot: ¡Bienvenido al Chatbot del Banco!")

# Función para identificar huellas
def identificar_huella(sample_path):
    sample = cv2.imread(sample_path)
    sift = cv2.SIFT_create()
    kp_sample, des_sample = sift.detectAndCompute(sample, None)

    print("Bot: Identificando huella...")

    best_score = 0
    best_filename = None
    best_image = None
    best_kp1 = None
    best_kp2 = None
    best_mp = None

    for file in os.listdir("Huellas"):
        fingerprint_path = os.path.join("Huellas", file)
        fingerprint_image = cv2.imread(fingerprint_path)
        kp_fingerprint, des_fingerprint = sift.detectAndCompute(fingerprint_image, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des_sample, des_fingerprint, k=2)

        good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
        score = len(good_matches)

        if score > best_score:
            best_score = score
            best_filename = file
            best_image = fingerprint_image
            best_kp1 = kp_sample
            best_kp2 = kp_fingerprint
            best_mp = good_matches

    if best_score < 40:
        print("Bot: No se encontró ninguna huella que coincida.")
        time.sleep(3)
        
        while True:
            print("Bot: ¿Deseas añadir esta huella a la carpeta de huellas? (Si/No)")
            respuesta = input("Tú: ")
            
            if respuesta.lower() == "si":
                nueva_ruta = input("Bot: Ingresa la ruta donde se encuentra la huella que deseas añadir: ")
                nombre_huella = input("Bot: Ingresa el nombre que deseas darle a la nueva huella: ")
                nueva_ruta = os.path.abspath(nueva_ruta)
                
                if os.path.isfile(nueva_ruta):
                    nueva_ruta_destino = os.path.join("Huellas", nombre_huella + ".BMP")
                    copyfile(nueva_ruta, nueva_ruta_destino)
                    print("Bot: La huella ha sido añadida correctamente.")
                    return
                else:
                    print("Bot: La ruta proporcionada no es válida.")
                    continue  # Volver al inicio del bucle while
            elif respuesta.lower() == "no":
                print("Bot: ¿Puedo ayudarte en algo más?")
                return
            else:
                print("Bot: Responde únicamente 'Si' o 'No'.")

    else:
        print("Bot: Huella identificada.\nCoincide con:", best_filename, "\nPuntaje de coincidencia:", best_score)

        result = cv2.drawMatches(sample, best_kp1, best_image, best_kp2, best_mp, None)
        result = cv2.resize(result, None, fx=4, fy=4)

        cv2.imshow("Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Ciclo principal de interacción con el usuario
while True:
    try:
        pedido = input("Tú: ")
        
        if pedido.lower() == "identificar huella":
            fingerprint_path = input("Tú: Por favor, ingresa la ruta de la imagen de la huella que deseas identificar: ")
            identificar_huella(fingerprint_path)
        else:
            bot_input = bot.get_response(pedido)
            print("Bot: ", bot_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
