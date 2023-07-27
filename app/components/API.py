import requests
import pandas as pd

import urllib.request
import json
import os
import ssl

class API_img:
    # Spécifiez les informations d'URL, de clé de prédiction et de contenu
    url = 'https://fertiliteclassification-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/09e3abf3-b171-4677-8241-367bad9b37c4/classify/iterations/Iteration1/image'
    prediction_key = 'a3276f0de358412dbf285df671ca86a8'
    content_type = 'application/octet-stream'
    
    def getPred(self, image_path):
        # Chargez l'image à prédire
        with open(image_path, 'rb') as file:
            image_data = file.read()
        # Configurez les en-têtes de la requête
        headers = {
            'Prediction-Key': self.prediction_key,
            'Content-Type': self.content_type
        }
        # Effectuez la prédiction en envoyant une requête POST avec les en-têtes et les données de l'image
        response = requests.post(self.url, headers=headers, data=image_data)
        
        return response.json()
    
    def extractProb(self, resp_json):
        # Création d'une liste de dictionnaires pour les prédictions
        predictions = resp_json['predictions']
        df = pd.DataFrame(predictions, columns=['probability', 'tagName'])
        df_sorted = df.sort_values(by='probability', ascending=False)
        return df_sorted


class API_values:
    
    def __init__(self):
        self.allowSelfSignedHttps(True) 
    
    url = 'https://workspace-fertilite-jxvfk.southafricanorth.inference.ml.azure.com/score'
    api_key = "wGiKQhKXs5YazqwkcpkBtpoGfX3JMOZE"
    azureml_model_deployment = 'automl4f78aa81750-1'
    
    def allowSelfSignedHttps(self, allowed):
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context
    
    def getPred(self, data):
        #self.allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
        # Request data goes here
        # The example below assumes JSON formatting which may be updated
        # depending on the format your endpoint expects.
        # More information can be found here:
        # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
        data_processed = json.loads(self.transform(data).to_json(orient='records'))
        print(data_processed)
        content =  {
          "Inputs": {
            "data": data_processed 
          },
          "GlobalParameters": {
            "method": "predict"
          }
        }

        body = str.encode(json.dumps(content))
        headers = {'Content-Type':'application/json', 
                   'Authorization': ('Bearer ' + self.api_key), 
                   'azureml-model-deployment': self.azureml_model_deployment }
        req = urllib.request.Request(self.url, body, headers)
        result = None
        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            print(result)
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))
            result = str(error.code)
            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))
        return result

    def transform(self,data):
        data['Childish diseases'] = data['Childish diseases'].map({'yes': 1, 'no': 0})
        data['Accident or serious trauma'] = data['Accident or serious trauma'].map({'yes': 1, 'no': 0})
        data['Surgical intervention'] = data['Surgical intervention'].map({'yes': 1, 'no': 0})
        data['High fevers in the last year'] = data['High fevers in the last year'].map({
            'more than 3 months ago': 2,
            'less than 3 months ago': 1,
            'no': 0
        })
        #data['Diagnosis'] = data['Diagnosis'].map({'Normal': 0, 'Altered': 1})
        data['Frequency of alcohol consumption'] = data['Frequency of alcohol consumption'].map({
            'once a week': 1,
            'several times a week': 2,
            'hardly ever or never': 0,
            'every day': 3
        })
        data['Season'] = data['Season'].map({
            'spring': 0,
            'fall': 1,
            'winter': 2,
            'summer': 3
        })
        data['Smoking habit'] = data['Smoking habit'].map({
            'occasional': 0,
            'daily': 1,
            'never': 2,
        })
        return data
    
    def de_transform(self,pred):
        pass