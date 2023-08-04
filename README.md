# fertilite

## Déployer en local

### Créer les images
```
docker build -t fertilite0container.azurecr.io/fertilite-app -f dockerfile .
docker build -t mysql0container.azurecr.io/database-fertilite -f dockerfile_mysql .
```

### Créer les conteneurs
```
docker run --name appfertilite -p 8501:8501 fertilite0container.azurecr.io/fertilite-app
docker run --name dbfertilite -d mysql0container.azurecr.io/database-fertilite 
```

### Transférer le code dans le conteneur
```
docker run -p 8501:8501 -v /app:/app --name appfertilite
# trasnferer plusieurs éléments
docker run -p 8501:8501 -v /app:/app --name appfertilite -v .env:/app/.env
```

## Déployer les images sur les conteneurs de registre Azure

### Application
```
docker build -t fertilite0container.azurecr.io/fertilite-app -f dockerfile .
docker login fertilite0container.azurecr.io
docker push fertilite0container.azurecr.io/fertilite-app
```

### Database
```
docker build -t mysql0container.azurecr.io/database-fertilite -f dockerfile_mysql .
docker login mysql0container.azurecr.io
docker push mysql0container.azurecr.io/database-fertilite
```

## Effectuer des test 
`python -m unittest test.test_api.TestAPIImg`  
`python -m unittest test.test_api.TestAPIVal`

## Package utilisés
Inscrit dans le fichier *requirements.txt* uniquement les packages utilisés dans le fichier séléctionné.  
`pipreqs --print app.py > requirements.txt`
