import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



df = pd.read_csv(
    "/Users/alessandropavia/Desktop/Stage Reply/Sales Analysis 2/data/processed/MasterTable.csv",
    parse_dates=["Order Date_def", "Ship Date_def"]
)

 #Inizializza la variabile di stato al primo avvio
if "show_details" not in st.session_state:
    st.session_state.show_details = False

# Funzione per cambiare stato
def toggle_view():
    st.session_state.show_details = not st.session_state.show_details

# Pulsante che cambia la visualizzazione
if st.button("🔄 Cambia vista"):
    toggle_view()

if st.session_state.show_details:

    st.title('Dataset Details:')

    # Riga dei grafici
    cols_per_row = len(df.columns)
    chart_cols = st.columns(cols_per_row)

    for i, col in enumerate(df.columns):
        with chart_cols[i]:
            col_data = df[col]
            fig, ax = plt.subplots(figsize=(6,4))
        
            if pd.api.types.is_numeric_dtype(col_data):
                sns.histplot(col_data.dropna(), bins=15, kde=False, ax=ax)
            else:
                sns.countplot(x=col_data, order=col_data.value_counts().index, ax=ax)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=6)
        
            ax.set_title(col, fontsize=8)
            ax.set_ylabel("")
            ax.set_xlabel("")
            ax.tick_params(axis='y', labelsize=6)
            ax.tick_params(axis='x', labelsize=6)
            st.pyplot(fig)


    table_dict = {}

    for col in df.columns:
        col_data = df[col]
        stats = {}
        stats['Storage Type'] = str(col_data.dtype)
        stats['Count'] = col_data.count()
        stats['Missing'] = col_data.isna().sum()
    
        if pd.api.types.is_numeric_dtype(col_data):
            stats['Mean'] = round(col_data.mean(), 4)
            stats['Min'] = col_data.min()
            stats['Max'] = col_data.max()
            stats['StDev'] = round(col_data.std(), 4)
            stats['Unique'] = col_data.nunique()
            stats['Top Frequency'] = '--'
        else:
            stats['Mean'] = '--'
            stats['Min'] = '--'
            stats['Max'] = '--'
            stats['StDev'] = '--'
            stats['Unique'] = col_data.nunique()
            stats['Top Frequency'] = col_data.value_counts().iloc[0]
    
        table_dict[col] = stats

    # Trasponi il dizionario per ottenere le righe come statistiche
    summary_df = pd.DataFrame(table_dict).T  # ora le colonne del dataset sono le colonne della tabella
    summary_df = summary_df.T  # trasponi così ogni colonna è una colonna del dataset e le righe sono le statistiche


    st.dataframe(summary_df) # Mostra tabella unica

    st.header('Dataset visualization')

else:
    st.title("Dataset completo")
    st.dataframe(df)








