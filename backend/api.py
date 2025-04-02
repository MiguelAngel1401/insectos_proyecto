from fastapi import FastAPI, Request, File, UploadFile
from contextlib import asynccontextmanager
from io import BytesIO
from PIL import Image
import tensorflow as tf
import numpy as np
from fastapi.responses import JSONResponse

def load_insects_model():
    import keras
    model = keras.models.load_model(r"C:\Users\Pc\workspaceDiseño\proyecto_insectos\project-template\models\insects-model\model.keras")
    return model


@asynccontextmanager
async def life_cycle(app: FastAPI):
    app.state.model_garden = {}


    print("the app is starting")
    
    insects_model = load_insects_model()
    
    app.state.model_garden["insects"]=insects_model
    yield
    print("the app is shutting down")
    print(app.state.model_garden["insects"].layers[0].get_weights())


app= FastAPI(lifespan=life_cycle)

@app.post("/insects-predict")
async def predict_flowers(request: Request, image: UploadFile = File(...)):
    image_bytes : bytes = await image.read()
    image_stream = BytesIO(image_bytes)
    pil_image= Image.open(image_stream)
    pil_image = pil_image.resize((224,224 ))
    # Convertir la imagen en un array de numpy
    image_array = np.array(pil_image, dtype=np.float32)
    
    # Aplicar el preprocesamiento de MobileNetV3
    image_array = tf.keras.applications.mobilenet_v3.preprocess_input(image_array)  # Preprocesar la imagen
    
    image_array = np.expand_dims(image_array, axis=0)  # Añadir dimensión de batch (1, 224, 224, 3)

    insects_model= request.app.state.model_garden["insects"]
    activation_scores = insects_model.predict(image_array)
    predictions = tf.nn.softmax(activation_scores).numpy().tolist()
    labels = ['Bees', 'Beetles', 'Butterfly', 'Cicada', 'Dragonfly', 
          'Grasshopper', 'Moth', 'Scorpion', 'Snail', 'Spider']
    # Obtener el índice de la mejor predicción
    best_index = np.argmax(predictions[0])

    # Obtener el label correspondiente a la mejor predicción
    best_label = labels[best_index]
    best_prob = predictions[0][best_index]

    return {"best_prediction": {"label": best_label, "probability": best_prob}}