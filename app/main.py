import streamlit as st

st.title("Téléversement d'images")
# Afficher un formulaire de téléversement de fichiers
uploaded_file = st.file_uploader("Choisissez une image", type=["jpg", "jpeg", "png", 'BMP'])
if uploaded_file is not None:
    # Afficher l'image téléversée
    st.image(uploaded_file, caption="Image téléversée", use_column_width=True)
    # Traiter l'image téléversée (vous pouvez ajouter votre propre logique ici)
    # Par exemple, vous pouvez utiliser une bibliothèque comme PIL pour manipuler l'image :
    # from PIL import Image
    # image = Image.open(uploaded_file)
    # Faites quelque chose avec l'image...
    # Afficher un message de confirmation
    st.success("L'image a été téléversée avec succès!")