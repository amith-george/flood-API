from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json
import joblib as jb

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class model_input(BaseModel):
    District : int 
    Rainfall : float
    RiverLevel : float
    SoilMoisture : float




# Load the file to check its contents
flood_model = jb.load('predictor2.joblib')



@app.post('/flood_prediction')
def flood_pred(input_parameters : model_input):

    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    dis = input_dictionary['District']
    rain = input_dictionary['Rainfall']
    river = input_dictionary['RiverLevel']
    soil = input_dictionary['SoilMoisture']



    input_list = [dis, rain, river, soil]

    prediction = flood_model.predict([input_list])


    if prediction[0] == 0:
        return 'The area is not prone to flooding'
    else:
        return 'The area is prone to flooding'