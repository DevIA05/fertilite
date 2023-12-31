import streamlit as st
import pandas as pd
from components.API import API_values   

def tab_val():    
    # Valeurs possibles pour les champs catégoriels
    seasons = ["spring", "fall", "winter", "summer"]
    childish_diseases = ["yes", "no"]
    accident_or_trauma = ["yes", "no"]
    surgical_intervention = ["yes", "no"]
    fevers = ["more than 3 months ago", "less than 3 months ago", "no"]
    alcohol_consumption = ["once a week", "several times a week", "hardly ever or never", "every day"]
    smoking_habit = ["never", "occasional", "daily"]

    # Affichage du formulaire
    st.subheader("Prédiction à partir de valeurs")

    with st.form(key='my_form'):
        left_column, right_column = st.columns(2)
        # Champs catégoriels
        with left_column:
            selected_season = st.selectbox("Saison", seasons)
            selected_childish_diseases = st.selectbox("Maladie infantile", childish_diseases)
            selected_accident_or_trauma = st.selectbox("Accident ou traumatisme sérieux", accident_or_trauma)
            selected_surgical_intervention = st.selectbox("Intervention chirurgicale", surgical_intervention)
            selected_fevers = st.selectbox("Durée de la fièvres l'année dernière", fevers)

        # Champs numériques
        with right_column:
            selected_alcohol_consumption = st.selectbox("Consommation d'alcool", alcohol_consumption)
            selected_smoking_habit = st.selectbox("Type de fumeur", smoking_habit)
            age = st.number_input("Age", min_value=0, max_value=120, value=30)
            hours_sitting = st.number_input("Nombre d'heures assis par jour", min_value=0, max_value=24, value=8)

        st.markdown('<br>', unsafe_allow_html=True)
        _, center_column, _ = st.columns([3, 1, 3])
        with center_column:
            submitted = st.form_submit_button('Submit')
            
    if submitted:
    # Code à exécuter lorsque le bouton est appuyé
        data = {
            "Season": [selected_season],
            "Childish diseases": [selected_childish_diseases],
            "Accident or serious trauma": [selected_accident_or_trauma],
            "Surgical intervention": [selected_surgical_intervention],
            "High fevers in the last year": [selected_fevers],
            "Frequency of alcohol consumption": [selected_alcohol_consumption],
            "Smoking habit": [selected_smoking_habit],
            "Age": [age],
            "Number of hours spent sitting per day": [hours_sitting]
        }
        
        fromApiVal = API_values()
        response = fromApiVal.getPred(data)
        st.write(response)
            
