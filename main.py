import pandas as pd
import streamlit as st
import plotly.express as px
from api_covid import extract_data

# Config page
st.set_page_config(page_title="Covid-19 Dashboard", page_icon="🦠", layout="wide")
st.title("🦠 Covid-19 Dashboard")

dataframe = pd.read_csv("covid_data.csv", sep=",")

st.sidebar.title("Mise à jour des données")
start_date = st.sidebar.date_input("Date de début", value=pd.to_datetime(dataframe["date"].min()).date())

if st.sidebar.button("Mettre à jour les données"):
    dataframe = extract_data(start_date)

    with st.spinner("Mise à jour des données...", show_time=True):
        st.rerun()

cases_options = ["confirmed", "deaths", "recovered"]
cases_select_box = st.selectbox(
    "Sélectionnez le type de cas",
    options=cases_options,
    index=0
)

pays_options = dataframe.groupby("name")
pays_selectionnes = st.multiselect(
    "Sélectionnez un ou plusieurs pays",
    options=pays_options,
    default=["France", "Italy", "US"]
)

filtered_df = dataframe[dataframe["name"].isin(pays_selectionnes)]

grouped_data = filtered_df.groupby(["date", "name"]).agg(
    confirmed=('confirmed', 'sum'),
    deaths=('deaths', 'sum'),
    recovered=('recovered', 'sum')
).reset_index()

fig_line = px.line(
    grouped_data,
    x="date",
    y=cases_select_box,
    color="name",
    markers=True,
    title=f"Évolution des {cases_select_box} Covid-19",
    labels={
        "value": cases_select_box,
        "date": "Mois et jour",
        "name": "Pays"
    }
)

st.plotly_chart(fig_line, use_container_width=True)