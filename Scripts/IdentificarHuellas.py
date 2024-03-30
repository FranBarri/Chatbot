import os
from PIL import Image, ImageTk
import cv2
from shutil import copyfile

def identificar_huella(sample_path):
    sample = cv2.imread(sample_path)
    sift = cv2.SIFT_create()
    kp_sample, des_sample = sift.detectAndCompute(sample, None)

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
        return {
            "mensaje": "Bot: No se encontró ninguna huella que coincida.",
            "resultado": None
        }
    else:
        result = cv2.drawMatches(sample, best_kp1, best_image, best_kp2, best_mp, None)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB
        
        # Convertir la imagen de coincidencia a formato compatible con tkinter
        image = Image.fromarray(result)
        image_tk = ImageTk.PhotoImage(image)
        
        return {
            "mensaje": "Bot: Huella identificada.\nCoincide con: {}\nPuntaje de coincidencia: {}".format(best_filename, best_score),
            "resultado": {
                "image_tk": image_tk
            }
        }


def agregar_huella(nueva_ruta, nombre_huella):
    nueva_ruta = os.path.abspath(nueva_ruta)
    
    if os.path.isfile(nueva_ruta):
        nueva_ruta_destino = os.path.join("Huellas", nombre_huella)
        copyfile(nueva_ruta, nueva_ruta_destino)
        return "Bot: La huella ha sido añadida correctamente."
    else:
        return "Bot: La ruta proporcionada no es válida."
