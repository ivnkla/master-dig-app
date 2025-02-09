import pandas as pd
import streamlit as st

# 📌 Chargement des données avec cache
@st.cache_data
def load_data():
    return pd.read_csv("mm.csv", delimiter=";")  

df = load_data()

# 📌 Liste des colonnes
columns_all = df.columns

# 📌 Fonction pour gérer les filtres
def filter():
    filters = {}
    filters_phase = {"Phase principale": None, "Phase complémentaire": None}
    filters_general = {
        "Libellé de l'établissement": None, 
        "Intitulé de la mention": None, 
        "Modalités d'enseignement": None, 
        "Capacité offerte limitée par la formation": None
    }
    selected_columns = list(filters_general.keys())  # Colonnes affichées par défaut

    # ✅ 🎯 Organisation des filtres en colonnes pour une mise en page compacte
    with st.container():
        st.subheader("Filtres généraux 🔍")
        cols = st.columns(len(filters_general))  # Une colonne par filtre pour gagner de la place
        
        for idx, attrib in enumerate(filters_general.keys()):
            print(idx, attrib)
            filters_general[attrib] = cols[idx].selectbox(
                attrib, options=["Tous"] + list(df[attrib].dropna().unique()), key=attrib, label_visibility="visible"
            )

    # ✅ 🎯 Filtres de phase (même logique)
    with st.container():
        st.subheader("Filtres de phase 🏷️")
        col1, col2 = st.columns(2)
        
        for idx, attrib in enumerate(filters_phase.keys()):
            filters_phase[attrib] = [col1, col2][idx].selectbox(
                "", options=["Tous"] + list(df[attrib].dropna().unique()), key=attrib, label_visibility="collapsed"
            )

    # ✅ 🎯 Sélection des colonnes à afficher dans la **barre latérale** pour ne pas surcharger la page principale
    with st.sidebar:
        st.subheader("🔧 Sélectionner les colonnes à afficher")
        for attrib in columns_all:
            if attrib not in filters_general and attrib not in filters_phase:
                selected_value = st.checkbox(attrib, value=False, key=attrib)
                if selected_value:
                    selected_columns.append(attrib)
                filters[attrib] = selected_value  # Sauvegarde du choix utilisateur
    
    return filters, filters_phase, filters_general, selected_columns

# 📌 Récupération des choix utilisateur
filters, filters_phase, filters_general, selected_columns = filter()

# 📌 Application des filtres
filtered_df = df.copy()  # Copie du DataFrame original

# 🎯 Appliquer les filtres généraux
for attrib, selected_value in filters_general.items():
    if selected_value != "Tous":
        filtered_df = filtered_df[filtered_df[attrib] == selected_value]

# 🎯 Appliquer les filtres de phase
for attrib, selected_value in filters_phase.items():
    if selected_value != "Tous":
        filtered_df = filtered_df[filtered_df[attrib] == selected_value]

# 🎯 Sélectionner uniquement les colonnes choisies par l'utilisateur
selected_columns = [col for col in selected_columns if col in filtered_df.columns]  # Évite les erreurs si une colonne filtrée n'existe plus
filtered_df = filtered_df[selected_columns] if not filtered_df.empty else filtered_df  # Garde le DataFrame vide si aucun résultat

# 📌 Affichage des résultats
st.write(f"### Résultats : {len(filtered_df)} masters trouvés 📊")
st.dataframe(filtered_df, height=300)  # Hauteur réduite pour éviter le scroll
