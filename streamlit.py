# Préliminaires

import streamlit as st
import pandas as pd
import numpy as np
from factorize import *
import time

def show_movie(full_title):
    title_row = df_base_show[df_base_show["show_title"] == full_title]
    title_tconst = title_row["tconst"].iloc[0]
    title_directors = title_row["directors"].iloc[0]
    title_firstActor = title_row["firstActor"].iloc[0]
    title_runtime = title_row["runtimeMinutes"].iloc[0]
    
    return st.write(f"""
                   {full_title}\n
                   Un film de {title_directors}, avec {title_firstActor} dans le premier rôle.\n
                   Durée : {title_runtime}mn\n
                   """)

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False


# En-tête de la page

st.title("Projet Creuse's Life")
st.subheader("Une production d'Agnès, Alexis, Bruno, Caro, et Pierrot", anchor=None)
st.header("Système de recommandation de films", anchor=None)


# Selection du film

option = st.selectbox(
    "Quel film vous a plu dernièrement ?",
    tuple([""] + list(df_base_show['show_title'])),
    key=1
    )

if option:
    
    # Display du titre et d'infos sur le film
    
    option_row = df_base_show[df_base_show["show_title"] == option]
    option_tconst = option_row["tconst"].iloc[0]
    
    st.write("#")
    
    st.write("Vous avez aimé :\n")
    show_movie(option)
    st.write("Excellent choix !")
    
    st.write("#")
    
    
    # Display des recommandations
    
    st.write("\nD'autres films similaires qui pourraient vous plaire :\n\n")
    
    voisins = plus_proches_films(option_tconst, 4, X)
    voisins_titres = voisins["show_title"]
    
    for colonne, titre in zip(st.columns(3), voisins_titres[1:]):
        with colonne:
            show_movie(titre)
    
    
    # A usage interne, le display de la table des résultats pour voir les détails
    
    if st.checkbox('Voir les détails'):
        st.table(voisins)


    # Un feedback
    
    feedbacks = import_local("feedbacks.csv")
    appreciations = ["", "Excellente", "Bonne", "Moyenne", "Bof", "Très mauvaise"]
    
    messages = {"Excellente":"Formidable !",
              "Bonne":"Super. N'hésitez pas à laisser un commentaire pour nous aider à nous améliorer.",
              "Moyenne":"Désolé ! Dites-nous ce qui n'allait pas.",
              "Bof":"Oh non ! Qu'est-ce qui n'allait pas ?",
              "Très mauvaise":"Aïe... Voulez-vous laissez un commentaire ?",
              }
    
    appreciation = st.selectbox(
        "Que pensez-vous de cette recommandation ?",
        appreciations,
        key=2)
    
    # A usage interne, le feedback précédent

    if st.checkbox('Voir les évaluations précédentes'):
        st.table(feedbacks)
                    
    # Système de commentaire et upload sur un fichier
    
    if appreciation:
        st.write(messages[appreciation])
        commentaire = st.text_area("Voulez-vous nous aider en laissant un commentaire ?", value="", max_chars=255, disabled=False, label_visibility="visible")
        feedback = [time.time(),
                    option_tconst,
                    list(voisins["tconst"][1:]),
                    facteurs.values(),
                    appreciation,
                    commentaire]
        with st.form(key='my_form'):
            submit_button = st.form_submit_button(label='Soumettre')
            if submit_button:
                feedbacks.loc[len(feedbacks.index)] = feedback             
                feedbacks.to_csv("feedbacks.csv")
                
