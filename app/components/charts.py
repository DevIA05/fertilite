import streamlit as st
import pandas as pd
from components.API import API_db
import matplotlib.pyplot as plt

def tab_charts():
    st.subheader("Graphiques")
    fromApiDB = API_db()
    df = fromApiDB.age()
        
    # Création du graphique (courbe) avec Matplotlib
    fig, ax = plt.subplots()
    ax.bar(df['Age'], df['Frequency'])
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution des âges')
    
    # Affichage du graphique avec Streamlit
    st.write("Courbe de distribution des âges :")
    st.pyplot(fig)