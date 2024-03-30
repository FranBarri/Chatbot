import cv2
import os

# Cargar la imagen de la huella de muestra
sample_path = "Huellas/1__M_Left_index_finger.BMP"
sample = cv2.imread(sample_path)

# Inicializar variables
best_score = 0
filename = None

# Obtener el tamaño de la imagen de muestra
sample_height, sample_width, _ = sample.shape

# Recorrer todas las imágenes en la carpeta "Huellas"
for file in os.listdir("Huellas"):
    # Construir la ruta completa del archivo
    filepath = "Huellas/" + file
    
    # Verificar si el archivo es una imagen
    if os.path.isfile(filepath) and filepath.lower().endswith(('.bmp', '.jpg', '.jpeg', '.png')):
        # Cargar la imagen del conjunto de datos
        fingerprint_image = cv2.imread(filepath)
        
        # Redimensionar la imagen del conjunto de datos para que tenga el mismo tamaño que la imagen de muestra
        fingerprint_image_resized = cv2.resize(fingerprint_image, (sample_width, sample_height))
        
        # Comparar las imágenes byte a byte
        diff = cv2.compare(sample, fingerprint_image_resized, cv2.CMP_NE)

        # Verificar si la matriz de diferencias está vacía
        if not diff.any():
            # Las imágenes son idénticas
            filename = file
            break

# Imprimir el resultado
if filename is not None:
    print("La huella de muestra coincide con la huella:", filename)
else:
    print("No se encontraron coincidencias en las huellas.")
