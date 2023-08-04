import requests
import pandas as pd

import urllib.request
import json
import os
import ssl

import mysql.connector

# Effectue une prédiction de la fertilité à partir d'une image et traitre la 
# réponse obtenu 
class API_img:
    
    def __init__(self):
        self._url = os.environ['API_URL_IMG']
        self._prediction_key = os.environ['API_KEY_IMG']
        self.content_type = 'application/octet-stream'
    
    def getPred(self, image_path):
        """
        Envoie une image à partir d'une requête à l'API pour obtenir une 
        prédiction.
        Args:
            image_path (str): Le chemin vers l'image à prédire.
        Returns:
            dict: Un dictionnaire au format json contenant la réponse de l'API.
        """
        # Chargez l'image à prédire
        with open(image_path, 'rb') as file:
            image_data = file.read()
        # Configurez les en-têtes de la requête
        headers = {
            'Prediction-Key': self._prediction_key,
            'Content-Type': self.content_type
        }
        # Effectuez la prédiction en envoyant une requête POST avec les en-têtes 
        # et l'image
        response = requests.post(self._url, headers=headers, data=image_data)
        return response.json()
    
    def extractProb(self, resp_json):
        """
        Extrait les probabilités de prédiction à partir de la réponse JSON de 
        l'API.
        Args:
            resp_json (dict): Un dictionnaire contenant la réponse JSON de l'API.
        Returns:
            pandas.DataFrame: Un DataFrame trié avec les probabilités de 
            prédiction et les noms de catégorie associés.
        """    
        # Extraction de la liste de dictionnaires représentant les prédictions 
        # et leurs probabilités
        predictions = resp_json['predictions']    
        # Création d'un DataFrame à partir des prédictions pour une meilleure 
        # manipulation. Les colonnes 'probability' et 'tagName' sont utilisées 
        # pour stocker les probabilités en fonction des catégories.
        df = pd.DataFrame(predictions, columns=['probability', 'tagName'])
        # Tri du DataFrame en ordre décroissant en fonction des probabilités 
        # pour mettre les prédictions les plus probables en premier.
        df_sorted = df.sort_values(by='probability', ascending=False)
        return df_sorted

# Effectue une prédiction de la fertilité à partir de valeur et traitre la 
# réponse obtenu 
class API_values:
    
    def __init__(self):
        self.allowSelfSignedHttps(True) 
        self._url = os.environ['API_URL_VAL']
        self._api_key = os.environ['API_KEY_VAL']
        self._azureml_model_deployment = os.environ['API_MODEL_VAL']
    
    def allowSelfSignedHttps(self, allowed):
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context
    
    def getPred(self, data):  
        """
        Effectue une prédiction en utilisant les données spécifiées en envoyant 
        une requête à l'API de prédiction.
        Args:
            data (dict): Les données à prédire.
        Returns:
            str: Catégorie prédite.
        """
        
        #self.allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
        # Request data goes here
        # The example below assumes JSON formatting which may be updated
        # depending on the format your endpoint expects.
        # More information can be found here:
        # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
        data_processed = json.loads(self.transform(data).to_json(orient='records'))
        #print(data_processed)
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
                   'Authorization': ('Bearer ' + self._api_key), 
                   'azureml-model-deployment': self._azureml_model_deployment }
        req = urllib.request.Request(self._url, body, headers)
        result = None
        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            result = self.de_transform(result)
        except urllib.error.HTTPError as error:
            #print("The request failed with status code: " + str(error.code))
            result = str(error.code)
            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            #print(error.info())
            #print(error.read().decode("utf8", 'ignore'))
            
        return result

    def transform(self,data):
        """
        Transforme les données catégorielles en valeurs numérique.
        Effectue un encodage par étiquetage (Label Encoding)
        Args:
            data (dict): Les données en format json.
        Returns:
            pandas.DataFrame: Un dataFrame contenant les données transformées.
        """
        data = pd.DataFrame(data)
        
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
    
    def de_transform(self,result):
        """
        Dé-transforme la prédiction du modèle (obtenu en réponse de la requête 
        effectuée) en catégorie.
        Args:
            result (dict): La réponse en format json.
        Returns:
            str: Une chaîne de caractères représentant la catégorie (de la 
            variable dépendante) correspondante.
        """
        reponse_json = json.loads(result)
        valeur_obtenue = reponse_json['Results'][0]
        resultat_transforme = 'Normal' if valeur_obtenue == 0 else 'Altered'
        return resultat_transforme

# Permet d'effectuer des requêtes sur la database 
class API_db:
    def __init__(self):
        self._conn = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PWD'],
            database=os.environ['BD_DB']
        )
           
    def _getData(self, query):
        """
        Exécute une requête SQL sur la base de données et renvoie les données
        récupérées.
        Args:
            query (str): La requête SQL à exécuter.
        Returns:
            list: Une liste de tuples contenant les données.
        """
        cursor = self._conn.cursor()
        cursor.execute(query)
        # Récupérer les données
        data = cursor.fetchall()
        # Fermer la connexion
        self._conn.close()
        return data
    
    def age(self):
        """
        Récupère les données sur l'âge à partir de la base de données et renvoie un DataFrame.
        Returns:
            pandas.DataFrame: Un DataFrame contenant les données d'âge et leur fréquence correspondante.
        """
        query = """
            SELECT Age, COUNT(*) AS Frequency
            FROM fertilite
            GROUP BY Age
            ORDER BY Age;
                """
        res = self._getData(query)
        df = pd.DataFrame(res, columns=['Age', 'Frequency'])
        return df