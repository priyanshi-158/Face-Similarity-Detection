from fastapi import FastAPI, File, UploadFile
from tensorflow.python.keras.models import load_model
from io import BytesIO
import tensorflow as tf
print(tf.__version__)
from PIL import Image
import uvicorn
import h5py
import numpy as np

def check_h5():
    with h5py.File('model/model_weights.h5', 'r') as file:
        # Print the keys at the root level of the HDF5 file
        print("Root keys:", list(file.keys()))
        if 'Siamese_Network_2' in file:
            print("Group keys:", list(file['Siamese_Network_2'].keys()))

# .h5 file
# def load_final_model():
#     try:
#         check_h5()
#         model = load_model('model/model_weights.h5')
#         print("Model loaded")
#         return model
#     except Exception as e:
#         print("Couldn't load model: ", e)



# .pb file 
# Model was trained on tensorflow 2.4.1 and Python 3.8, hence wasn't loading on Python 3.12
# Now model is loaded, but the predict function is not working 
def load_final_model():
    try:
        # saved_model = tf.saved_model.load("model/assets/")
        saved_model = load_model("model/assets/")
        print("Model loaded")
        return saved_model
    except Exception as e:
        print("Couldn't load model: ", e)

def img_preprocess(img):
    # resize to 128x128
    img = img.resize((128, 128))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.keras.applications.resnet.preprocess_input(img)
    img = tf.expand_dims(img, axis=0)  # Add batch dimension
    # TensorSpec(shape=(None, 128, 128, 3), dtype=tf.float32, name='inputs/0')
    img = tf.convert_to_tensor(img, dtype=tf.float32)
    img = img / 255.0
    return img

def predictSimilarImage(anchor: Image.Image, img1: Image.Image, img2: Image.Image):
    anchor = img_preprocess(anchor)
    img1 = img_preprocess(img1)
    img2 = img_preprocess(img2)

    # anchor = tf.identity(anchor, name="input_image")

    classifier = load_final_model()
    print("classifier ", classifier)

    prediction = None
    try:
        prediction = classifier.predict([anchor, img1, img2])
    except Exception as e:
        print("Couldn't predict: ", e)

    print("prediction ", prediction)
    return prediction
 
 # for api
def read_imagefile(file) -> Image.Image:
    img = Image.open(BytesIO(file)) #Pillow object
    return img

def file_check(file):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return False
    return True


app = FastAPI()
 
@app.get('/test')
async def testing():
    t = load_final_model()
    print("model ", t)
    return "Hello World"

@app.post("/predict")
async def predict_api(fileAnchor: UploadFile = File(...), file1: UploadFile = File(...), file2: UploadFile = File(...)):

    # extension check
    if not file_check(fileAnchor):
        return {"Error" : "Image must be jpg or png format!"}
    if not file_check(file1):
        return {"Error" : "Image must be jpg or png format!"}
    if not file_check(file2):
        return {"Error" : "Image must be jpg or png format!"}
        
    anchor = read_imagefile(await fileAnchor.read())
    img1 = read_imagefile(await file1.read())
    img2 = read_imagefile(await file2.read())

    try:
        prediction = predictSimilarImage(anchor, img1, img2)
    except Exception as e:
        return {"Error": str(e)}

    final_prediction = dict()

    # prediction is (array([1.579145], dtype=float32), array([0.], dtype=float32))
    # convert this to a dictionary

    if prediction[0] <= prediction[1]:
        final_prediction.update({"Result" : "Image 1 is more similar to Anchor Image"})
    else:
        final_prediction.update({"Result" : "Image 2 is more similar to Anchor Image"})

    # if prediction:
    #     final_prediction.update({"Result" : "Image 1 is more similar to Anchor Image"})
    # else:
    #     final_prediction.update({"Label" : "Image 2 is more similar to Anchor Image"})

    return final_prediction

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
