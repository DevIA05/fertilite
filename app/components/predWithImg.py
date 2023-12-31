from PIL import Image
import streamlit as st
import tempfile

from components.API import API_img  


def tab_img():
    #st.title("Prédiction Fertilité")
    st.subheader("Prédiction à partir d'une image")
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
            fromApiImg = API_img()
            resultat = fromApiImg.getPred(temp_image.name)
            print(resultat)
            df = fromApiImg.extractProb(resultat)
            st.dataframe(df.set_index(df.columns[0]))