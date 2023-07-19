import streamlit as st
import tempfile
import os
from PIL import Image
from api import API

st.title("Prédiction Fertilité")
st.subheader("Prédiction selon une image")
# Afficher un formulaire de téléversement de fichiers
uploaded_file = st.file_uploader("Choisissez une image", type=["jpg", "jpeg", "png", 'BMP'])
if uploaded_file is not None:
    # Afficher l'image téléversée
    st.image(uploaded_file, caption="Image téléversée", use_column_width=True)
    # Afficher un message de confirmation
    st.success("L'image a été téléversée avec succès!")
    image = Image.open(uploaded_file)
    # Bouton pour effectuer la prédiction
    if st.button("Prédire"):
        # Enregistrer l'image redimensionnée temporairement sur le disque
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
            image.save(temp_image.name)
        api = API()
        pred = api.getPredFromImg(temp_image.name)
        df = api.extractProb(pred)
        st.dataframe(df.set_index(df.columns[0]))