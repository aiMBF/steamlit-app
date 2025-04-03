import streamlit as st  
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.set_page_config(page_title="Analyse des transactions", layout="wide")
st.title("Analyse des Transactions de Vente")

data_file = st.file_uploader("Importer le fichier de donnees", type=["csv"])

if data_file:
    df = pd.read_csv(data_file, parse_dates=["Date"])
    
    st.subheader("Apercu des donnees")
    st.write(df.head())
    
    min_date, max_date  =  df["Date"].min(), df["Date"].max()
    date_range = st.slider("Selectionner une periode pour l'analyse", min_value=min_date.to_pydatetime(), max_value=max_date.to_pydatetime(), value=(min_date.to_pydatetime(), max_date.to_pydatetime()))
    df_filtered = df[(df["Date"] >= date_range[0]) & (df["Date"] <= date_range[1])]

    st.subheader("Statistiques Générales")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", f"{df_filtered.shape[0]:,}")
    col2.metric("Revenu Total (€)", f"{df_filtered['Total Amount'].sum():,.2f}")
    col3.metric("Quantité Totale de produits vendus", f"{df_filtered['Quantity'].sum():,}")
    
    
    st.subheader("Evolution du Chiffre d'Affaires")
    sales_over_time = df_filtered.groupby("Date")["Total Amount"].sum().reset_index()
    fig = px.line(sales_over_time, x="Date", y="Total Amount", title="Évolution des Ventes")
    st.plotly_chart(fig)
    
    
    st.subheader("Répartition des Ventes par Catégorie")
    category_sales = df_filtered.groupby("Product Category")["Total Amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=category_sales.index, y=category_sales.values, ax=ax, palette="viridis")
    ax.set_ylabel("Revenu Total (€)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
    
    st.subheader("Analyse des Clients")
    gender_sales = df_filtered.groupby("Gender")["Total Amount"].sum()
    fig, ax = plt.subplots(figsize=(5, 5))
    gender_sales.plot(kind="pie", autopct="%.1f%%", colors=["lightblue", "pink"], ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)
    
    st.subheader("Top 10 Clients")
    top_clients = df_filtered.groupby("Customer ID").agg(
    Total_Achat=("Total Amount", "sum"),
    Total_Produits=("Quantity", "sum"),
    Product_Categories=("Product Category", lambda x: ", ".join(x.unique()))).sort_values(by="Total_Achat", ascending=False).head(10)    
    st.write(top_clients)
    
else:
    st.info("Veuillez importer un fichier CSV pour commencer l'analyse.")