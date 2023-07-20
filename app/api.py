import requests
import pandas as pd

class API:
    # Spécifiez les informations d'URL, de clé de prédiction et de contenu
    url = 'https://fertiliteclassification-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/09e3abf3-b171-4677-8241-367bad9b37c4/classify/iterations/Iteration1/image'
    prediction_key = 'a3276f0de358412dbf285df671ca86a8'
    content_type = 'application/octet-stream'
    
    def getPredFromImg(self, image_path):
        # Chargez l'image à prédire
        image_data = open(image_path, 'rb').read()
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
    
    