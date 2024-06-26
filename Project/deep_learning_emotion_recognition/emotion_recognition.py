from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import imutils
import cv2
import time

# Función para detección de emociones
def detectar_emociones():
    # Variables para calcular FPS
    time_actualframe = 0
    time_prevframe = 0

    # Tipos de emociones del detector
    classes = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

    # Cargamos el modelo de detección de rostros
    prototxtPath = r"face_detector\deploy.prototxt"
    weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

    # Carga el detector de clasificación de emociones
    emotionModel = load_model("deep_learning_emotion_recognition/modelFEC.h5")

    # Se crea la captura de video
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def predict_emotion(frame, faceNet, emotionModel):
        # Construye un blob de la imagen
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))

        # Realiza las detecciones de rostros a partir de la imagen
        faceNet.setInput(blob)
        detections = faceNet.forward()

        # Listas para guardar rostros, ubicaciones y predicciones
        faces = []
        locs = []
        preds = []

        # Recorre cada una de las detecciones
        for i in range(0, detections.shape[2]):

            # Fija un umbral para determinar que la detección es confiable
            # Tomando la probabilidad asociada en la deteccion
            if detections[0, 0, i, 2] > 0.4:
                # Toma el bounding box de la detección escalado
                # de acuerdo a las dimensiones de la imagen
                box = detections[0, 0, i, 3:7] * np.array(
                    [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
                )
                (Xi, Yi, Xf, Yf) = box.astype("int")

                # Valida las dimensiones del bounding box
                if Xi < 0:
                    Xi = 0
                if Yi < 0:
                    Yi = 0

                # Se extrae el rostro y se convierte BGR a GRAY
                # Finalmente se escala a 48x48
                face = frame[Yi:Yf, Xi:Xf]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (48, 48))
                face2 = img_to_array(face)
                face2 = np.expand_dims(face2, axis=0)

                # Se agrega los rostros y las localizaciones a las listas
                faces.append(face2)
                locs.append((Xi, Yi, Xf, Yf))

                pred = emotionModel.predict(face2)
                preds.append(pred[0])

        return locs, preds

    val = -1
    estres = ['alto', 'medio', 'bajo']
    lista = [0, 0, 0]
    emocion = ''
    rango = 100

    for i in range(rango):
        # Se toma un frame de la cámara y se redimensiona
        ret, frame = cam.read()
        frame = imutils.resize(frame, width=640)

        (locs, preds) = predict_emotion(frame, faceNet, emotionModel)

        for (box, pred) in zip(locs, preds):
            (Xi, Yi, Xf, Yf) = box
            (angry, disgust, fear, happy, neutral, sad, surprise) = pred

            label = "{}: {:.0f}%".format(
                classes[np.argmax(pred)], max(angry, disgust, fear, happy, neutral, sad, surprise) * 100
            )
            emocion = classes[np.argmax(pred)]
            print(emocion)

            cv2.rectangle(frame, (Xi, Yi - 40), (Xf, Yi), (255, 0, 0), -1)
            cv2.putText(frame, label, (Xi + 5, Yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.rectangle(frame, (Xi, Yi), (Xf, Yf), (255, 0, 0), 3)

        time_actualframe = time.time()

        if time_actualframe > time_prevframe:
            fps = 1 / (time_actualframe - time_prevframe)

        time_prevframe = time_actualframe

        cv2.putText(frame, str(int(fps)) + " FPS", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA)

        if emocion:
            indice = classes.index(emocion)

            if indice == 0 or indice == 2:
                lista[0] += 1  # ALTO
            elif indice == 1 or indice == 5 or indice == 6:
                lista[1] += 1  # MEDIO
            elif indice == 3 or indice == 4:
                lista[2] += 2  # BAJO

        cv2.imshow("Frame", frame)
        
        # Si se presiona la tecla 'q', terminar el loop
        print(i, ' - ', rango)
        if cv2.waitKey(1) & i == rango:
            break

    categoria = lista.index(max(lista))

    if categoria == 0:
        val = 1
    elif categoria == 1:
        val = 2
    elif categoria == 2:
        val = 3
    else:
        val = -1

    # Liberar la cámara y cerrar ventanas después de la iteración
    cam.release()
    cv2.destroyAllWindows()

    return val

if __name__ == "__main__":
    resultado = detectar_emociones()
    print("El valor devuelto es:", resultado)
