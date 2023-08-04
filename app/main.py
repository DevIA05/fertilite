import streamlit as st
import os, sys
from dotenv import load_dotenv

from components.predWithImg import tab_img
from components.predWithValues import tab_val
from components.charts import tab_charts

load_dotenv()

def main():
    # Titre de la page
    st.title("Human Sperm Head Morphology")

    # Liste des onglets disponibles
    onglets = {
        "À partir d'une image": tab_img,
        "À partir de valeur": tab_val,
        "Graphique": tab_charts
    }

    # Affichage de la liste des onglets dans la barre latérale (sidebar)
    onglet_selectionne = st.sidebar.radio("Navigation", list(onglets.keys()))

    # Exécution de la fonction associée à l'onglet sélectionné
    onglets[onglet_selectionne]()
    

if __name__ == "__main__":
    main()