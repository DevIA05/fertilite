import unittest
from unittest.mock import Mock, patch
from api import API

class TestAPI(unittest.TestCase):
        
    # tests go here
    def test_api_call(self):
        
        image_path = r'C:\Users\IKmai\Documents\Workspace\afpar-simplon\fertilite\data\Human Sperm Head Morphology dataset (HuSHeM)\02_Tapered\image_004.BMP'
        
        # Création d'un objet simulacre pour la réponse de la méthode post
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': '36923662-dbe8-47bc-848b-29063646a961',
            'project': '09e3abf3-b171-4677-8241-367bad9b37c4',
            'iteration': '2356ccbe-64a1-44b2-a3b9-799bbf8613e4',
            'created': '2023-07-20T16:20:31.595Z',
            'predictions': [
                {'probability': 0.99285686, 'tagId': 'be49ac9d-c8fd-44b9-b956-87d078a03cdf', 'tagName': 'pyriform'},
                {'probability': 0.0059690806, 'tagId': '8fcc4570-d7ed-4a31-8961-265242a53e04', 'tagName': 'tapered'},
                {'probability': 0.0009966472, 'tagId': '921f503b-04ca-4039-a443-9aa175648d02', 'tagName': 'amorphous'},
                {'probability': 0.00017731161, 'tagId': '3c271665-50b4-43f8-af4e-1f0021c2730b', 'tagName': 'normal'}
            ]
        }

        api = API()
        # Utilisation du décorateur patch pour remplacer temporairement la méthode post avec l'objet simulacre
        with patch('requests.post', return_value=mock_response):
            # Appel de la méthode à tester
            response = api.getPredFromImg(image_path)
        
        # Assert that the value of 'predictions' is a list with a length of 4
        self.assertIsInstance(response['predictions'], list, "Value of 'predictions' is a list")
        self.assertEqual(len(response['predictions']), 4, "Length of 'predictions' list is 4")

 
if __name__ == "__main__":
    unittest.main()   
    