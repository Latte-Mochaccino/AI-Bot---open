from keras.models import load_model  # Necesitas tener instalado TensorFlow para que funcione Keras 
# Importamos herramientas para trabajar con imágenes. 
# Image sirve para abrir imágenes y ImageOps nos ayuda a modificarlas (como cambiar su tamaño). 
from PIL import Image, ImageOps  # Instala la librería 'pillow' con pip si no la tienes 

# Importamos NumPy, una biblioteca que nos ayuda a trabajar con números y matrices (listas de listas). 
import numpy as np 

def get_class (ruta_keras, ruta_labels, ruta_imagen):

  # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

  # Load the model
    model = load_model(ruta_keras, compile=False)

  # Load the labels
    class_names = open(ruta_labels, "r").readlines()

  # Create the array of the right shape to feed into the keras model
  # The 'length' or number of images you can put into the array is
  # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  # Replace this with the path to your image
    image = Image.open(ruta_imagen).convert("RGB")

  # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  # turn the image into a numpy array
    image_array = np.asarray(image)

  # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

  # Load the image into the array
    data[0] = normalized_image_array

  # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    porcentaje = confidence_score * 100

    return class_name[2:-1] , round(porcentaje, 2)