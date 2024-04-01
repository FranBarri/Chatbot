import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Chatbot import iniciar_chatbot, obtener_respuesta
from IdentificarHuellas import identificar_huella, agregar_huella

# Crear el chatbot bancario y entrenarlo
bot = iniciar_chatbot()

# Crear la interfaz de usuario
root = tk.Tk()
root.title("Chatbot Bancario")

# Crear un cuadro de texto para mostrar la conversación
conversation_text = tk.Text(root, wrap="word", width=50, height=20)
conversation_text.grid(row=0, column=0, padx=10, pady=10)
conversation_text.config(state="disabled")

# Crear una etiqueta para mostrar la primera imagen
imagen_label = tk.Label(root)
imagen_label.grid(row=0, column=1, padx=10, pady=10)

# Función para manejar la selección de archivo
def seleccionar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Bitmap files", "*.bmp")])
    if file_path:
        resultado = identificar_huella(file_path)
        mostrar_mensaje(resultado["mensaje"])
        if resultado["resultado"]:
            mostrar_imagen(resultado["resultado"]["image_tk"])
            
# Función para agregar una nueva huella
def agregar_nueva_huella(nueva_ruta):
    if nueva_ruta:
        resultado = identificar_huella(nueva_ruta)
        mostrar_mensaje(resultado["mensaje"])
        if not resultado["resultado"]:
            mostrar_mensaje("Bot: ¿Deseas añadir esta huella a la carpeta de huellas? (Si/No)")
            entrada_text.focus_set()
            entrada_text.bind("<Return>", lambda event: manejar_respuesta_si(event, nueva_ruta))

def manejar_respuesta_si(event, nueva_ruta):
    respuesta = entrada_text.get().lower()
    mostrar_mensaje("Tú: " + respuesta)
    if respuesta == "si":
        entrada_text.unbind("<Return>")
        nombre_archivo = os.path.basename(nueva_ruta)
        mensaje = agregar_huella(nueva_ruta, nombre_archivo)  # Agregar la huella con el nombre correcto
        mostrar_mensaje(mensaje)
        entrada_text.delete(0, tk.END)
        entrada_text.bind("<Return>", manejar_entrada)  # Volver a bindear la tecla Enter
        entrada_text.focus_set()  # Re-enfocar la entrada de texto
    elif respuesta == "no":
        mostrar_mensaje("Bot: ¿Puedo ayudarte en algo más?")
        entrada_text.config(state=tk.NORMAL)
        entrada_text.focus_set()
        entrada_text.delete(0, tk.END)
    else:
        mostrar_mensaje("Bot: Por favor, responde 'Si' o 'No'.")
        
# Función para manejar la entrada del usuario
def manejar_entrada(event=None):
    entrada_usuario = entrada_text.get()
    if entrada_usuario.lower() == "2":
        mostrar_mensaje("Tú: " + entrada_usuario)
        nueva_ruta = filedialog.askopenfilename(filetypes=[("Bitmap files", "*.bmp")])
        if nueva_ruta:
            agregar_nueva_huella(nueva_ruta)
    elif entrada_usuario.lower() == "1":
        mostrar_mensaje("Tú: " + entrada_usuario)
        seleccionar_archivo()
    else:
        respuesta_bot = obtener_respuesta(bot, entrada_usuario)
        mostrar_mensaje("Tú: " + entrada_usuario)
        mostrar_mensaje("Bot: " + str(respuesta_bot))
    entrada_text.delete(0, tk.END)
    return "break"

entrada_text = tk.Entry(root, width=50)
entrada_text.grid(row=2, column=0, padx=10, pady=10)
entrada_text.bind("<Return>", manejar_entrada)
entrada_text.focus()

# Función para mostrar mensajes en la conversación
def mostrar_mensaje(mensaje):
    conversation_text.config(state="normal")  # Habilitar la edición temporalmente
    conversation_text.insert(tk.END, mensaje + "\n")  # Insertar el mensaje en el cuadro de texto
    conversation_text.config(state="disabled") 

# Mostrar mensaje de bienvenida en la interfaz
mostrar_mensaje("Bot: ¡Bienvenido al Chatbot del Banco!\nTe presentamos las siguientes opciones\nPara ingresar con identificación de huella, presione 1\nPara registrar una nueva huella, presione 2\nTambién puede realizar consultas\n")

# Función para mostrar la imagen en la interfaz
def mostrar_imagen(image_tk):
    # Actualizar la imagen en el widget de etiqueta en la ventana principal
    imagen_label.configure(image=image_tk)
    imagen_label.image = image_tk
    
    # Colocar la etiqueta en el costado derecho de la ventana principal
    imagen_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Ejecutar la interfaz de usuario
root.mainloop()
