# fertilite

`docker build -t fertilite-app .`  
`docker run -p 8501:8501 -v /path/to/your/workdir:/app my-streamlit-app`  
`pipreqs --print app.py > requirements.txt`  

`docker run --name test1 -p 8501:8501 fertilite0container.azurecr.io/fertilite-app:latest`
`docker build -t fertilite0container.azurecr.io/fertilite-app:latest .`

```sh
identifiant sur le container azure
docker push fertilite0container.azurecr.io/fertilite-app:latest
docker login fertilite-img
```

`python -m unittest test_api`  
`python -m unittest test.test_api.TestAPIImg`


```py 
image_data = open(image_path, 'rb').read()
ResourceWarning: Enable tracemalloc to get the object allocation traceback

with open(image_path, 'rb') as file:
    image_data = file.read()
```


# Lancer un conteneur en déplaçant le contenu du projet
`docker run -d -p 8501:8501 -v .:/app fertilite0container.azurecr.io/fertilite-app`  