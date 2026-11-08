from pathlib import Path

import pandas as pd
import streamlit as st

DOSSIER = Path(__file__).parent / "donnees"

st.set_page_config(page_title="Les résultats d'examens", page_icon="🎓", layout="wide")

st.title("Les résultats d'examens")
st.caption("Projet final, Python pour l'analyse de données, ESIH 2026. Données fictives.")

brut = pd.read_csv(DOSSIER / "resultats_brut.csv")

@st.cache_data
def charger():
    return pd.read_csv(DOSSIER / "resultats_propre.csv")

complet = charger()
complet_filtre = complet.copy()

st.write(f"Le fichier brut compte {len(brut)} lignes.")
st.dataframe(brut.head(10), hide_index=True)

communes = complet["commune"].unique()
ecoles = complet["ecole"].unique()

choix_commune = st.sidebar.multiselect("Commune", communes, default=communes)
choix_ecole = st.sidebar.multiselect("Ecole", ecoles, default=ecoles)
choix_annee = st.sidebar.selectbox("Année", [2024, 2025], index = 1)

if not choix_ecole:
    st.warning("Veuillez choisir au moins une école")
    st.stop()
elif not choix_commune:
    st.warning("Veuillez choisir au moins une commune")
    st.stop()
elif not complet[(complet["commune"].isin(choix_commune)) &(complet["ecole"].isin(choix_ecole))].shape[0]:
    st.warning("Cette(ces) école(s) n'est(ne sont) pas dans cette commune")
    st.stop()


filtre = complet[complet["commune"].isin(choix_commune)]
filtre = filtre[complet["annee"] == choix_annee]
filtre = filtre[complet["ecole"].isin(choix_ecole)]

complet_filtre = complet_filtre[complet_filtre["commune"].isin(choix_commune)]
complet_filtre = complet_filtre[complet_filtre["annee"] == choix_annee]
complet_filtre = complet_filtre[complet_filtre["ecole"].isin(choix_ecole)]

col1, col2, col3 = st.columns(3)

col1.metric("Taux de réussite des filles", f"{((complet_filtre[complet_filtre["sexe"] == "F"]["reussi"].sum() / complet_filtre[complet_filtre["sexe"] == "F"]["reussi"].size)*100).round(2)}%")

col2.metric("Taux de réussite des garçons", f"{((complet_filtre[complet_filtre["sexe"] == "M"]["reussi"].sum() / complet_filtre[complet_filtre["sexe"] == "M"]["reussi"].size)*100).round(2)}%")

col3.metric("Taux de réussite des écoles congréganistes", f"{((complet_filtre[complet_filtre["secteur"] == "Congréganiste"]["reussi"].sum() / complet_filtre[complet_filtre["secteur"] == "Congréganiste"]["reussi"].size)*100).round(2)}%")

tab1, tab2, tab3, tab4 = st.tabs(["Réussite par filière", "Réussite par secteur", "Evolution des communes et départements", "Filles et Garçons"])

with tab1:
    st.title("Taux de réussite par filière")
    taux_filiere = (((complet_filtre.groupby("filiere")["reussi"].sum()) / (complet_filtre.groupby("filiere")["reussi"].size()))*100).round(2).sort_values(ascending=False)
    st.bar_chart(taux_filiere, x_label="Filière", y_label = "Taux de réussite (en %)")
    taux_filiere_df = taux_filiere.reset_index()
    sep1, sep2 = st.columns(2)
    sep1.metric("Filière avec le plus haut taux de réussite", f"{taux_filiere.max()}% ({taux_filiere_df.nlargest(1, "reussi")["filiere"][0]})")
    sep2.metric("Filière avec le plus faible taux de réussite", f"{taux_filiere.min()}% ({taux_filiere_df.nlargest(3, "reussi")["filiere"][2]})")

    st.title("Evolution de la réussite par filière")
    complet_2024 = complet[complet["annee"] == 2024]
    eva_2024 = (((complet_2024.groupby("filiere")["reussi"].sum()) / (complet_2024.groupby("filiere")["reussi"].size()))*100).round(2).sort_values(ascending=False)
    complet_2025 = complet[complet["annee"] == 2025]
    eva_2025 = (((complet_2025.groupby("filiere")["reussi"].sum()) / (complet_2025.groupby("filiere")["reussi"].size()))*100).round(2).sort_values(ascending=False)
    eva_2024_2025 = pd.concat([eva_2024, eva_2025], axis=1)
    eva_2024_2025.columns = ["2024", "2025"]
    st.bar_chart(eva_2024_2025, stack=False, color=["#1368DE", "#FB03C1"])

with tab2:
    st.title("Taux de réussite par secteur")
    eva_secteur = (((complet_filtre.groupby("secteur")["reussi"].sum()) / (complet_filtre.groupby("secteur")["reussi"].size()))*100).round(2).sort_values(ascending=False)
    st.bar_chart(eva_secteur, x_label="Secteur", y_label = "Taux de réussite (en %)")
    eva_secteur_df = eva_secteur.reset_index()
    sep1, sep2 = st.columns(2)
    sep1.metric("Plus haut taux", f"{eva_secteur.max()}% ({eva_secteur_df.iloc[0]["secteur"]})")
    sep2.metric("Plus faible taux", f"{eva_secteur.min()}% ({eva_secteur_df.iloc[-1]["secteur"]})")

with tab3:
    st.title("Evolution de la réussite par commune")
    complet_2024 = complet[complet["annee"] == 2024]
    eva_2024 = (((complet_2024.groupby("commune")["reussi"].sum()) / (complet_2024.groupby("commune")["reussi"].size()))*100).round(2).sort_values(ascending=False)
    complet_2025 = complet[complet["annee"] == 2025]
    eva_2025 = (((complet_2025.groupby("commune")["reussi"].sum()) / (complet_2025.groupby("commune")["reussi"].size()))*100).round(2).sort_values(ascending=False)
    eva_2024_2025_c = pd.concat([eva_2024, eva_2025], axis=1)
    eva_2024_2025_c.columns = ["2024", "2025"]
    st.bar_chart(eva_2024_2025_c, stack=False, color=["#1368DE", "#FB03C1"])

    sep1, sep2 = st.columns(2)
    eva_2024_2025_c_df = eva_2024_2025_c.reset_index()
    eva_2024_2025_c_df["evolution"] = eva_2024_2025_c_df["2025"] - eva_2024_2025_c_df["2024"]
    sep1.metric("Commune avec la plus grande hausse", f"{eva_2024_2025_c_df.max()["evolution"].round(2)}% ({eva_2024_2025_c_df.nlargest(1, "evolution")["commune"].iloc[0]})")
    sep2.metric("Commune avec la plus grande baisse", f"{eva_2024_2025_c_df.min()["evolution"].round(2)}% ({eva_2024_2025_c_df.nlargest(12, "evolution")["commune"].iloc[11]})")
   

    st.title("Evolution de la réussite par département")
    complet_2024 = complet[complet["annee"] == 2024]
    eva_2024 = (((complet_2024.groupby("departement")["reussi"].sum()) / (complet_2024.groupby("departement")["reussi"].size()))*100).round(2).sort_values(ascending=False)
    complet_2025 = complet[complet["annee"] == 2025]
    eva_2025 = (((complet_2025.groupby("departement")["reussi"].sum()) / (complet_2025.groupby("departement")["reussi"].size()))*100).round(2).sort_values(ascending=False)
    eva_2024_2025_d = pd.concat([eva_2024, eva_2025], axis=1)
    eva_2024_2025_d.columns = ["2024", "2025"]
    st.bar_chart(eva_2024_2025_d, stack=False, color=["#1368DE", "#FB03C1"])

    sep3, sep4 = st.columns(2)
    eva_2024_2025_d_df = eva_2024_2025_d.reset_index()
    eva_2024_2025_d_df["evolution"] = eva_2024_2025_d_df["2025"] - eva_2024_2025_d_df["2024"]
    sep3.metric("Département avec la plus grande hausse", f"{eva_2024_2025_d_df.max()["evolution"].round(2)}% ({eva_2024_2025_d_df.nlargest(1, "evolution")["departement"].iloc[0]})")
    sep4.metric("Département avec la plus grande baisse", f"{eva_2024_2025_d_df.min()["evolution"].round(2)}% ({eva_2024_2025_d_df.nlargest(8, "evolution")["departement"].iloc[7]})")

with tab4:
    eva_sexe = pd.concat([complet_filtre.groupby(["filiere", "sexe"]).size(), complet_filtre.groupby(["filiere", "sexe"])["reussi"].sum()], axis=1)
    eva_sexe.columns = ["Total", "Reussi"]
    eva_sexe["Reussite_%"] = ((eva_sexe["Reussi"] / eva_sexe["Total"])*100).round(2)
    del eva_sexe["Total"]
    del eva_sexe["Reussi"]
    eva_sexe = eva_sexe["Reussite_%"].unstack()
    st.bar_chart(eva_sexe, stack=False, color=["#3498DB", "#E74C3C"])

    eva_sexe["parite"] = (eva_sexe["F"] - eva_sexe["M"]).abs()
    st.metric("Filière avec la meilleure parité", f"{eva_sexe.nlargest(4, "parite")["parite"].iloc[3].round(2)} ({eva_sexe.nlargest(4, "parite").iloc[3].name})")
    


st.title("Conclusion")
st.markdown("Les filières réussissant le mieux sont SMP et SVT. Le secteur de l'école peut influer sur le taux de réussite de l'élève (constat que les écoles congréganistes ont un meilleur taux de réussite.) Les communes qui progressent le mieux sont Port-de-Paix, Saint-Marc et Jacmel, les départements qui progressent le mieux sont le Nord-Ouest et l'Artibonite. Les filles ont un taux de réussite légèrement supérieur généralement, mais cette tendance varie selon la filière observée. Toutefois, toutes les observations décrites ici ne sont que des estimations, elles ne permettent pas vraiment d'établir une corrélation entre différents facteurs comme la filière, le secteur etc... et la réussite des étudiants. Pour approfondir cette étude, il serait intéressant de mesurer l'influence de l'assiduité, des conditions d'apprentissage et des ressources pédagogiques, ces informations permettraient de mieux comprendre les facteurs qui influencent les résultats scolaires.")

with st.expander("Données Filtrées"):
    st.dataframe(filtre)