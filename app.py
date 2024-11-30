import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import openai


# Título do aplicativo
st.title("Análise de Séries Temporais com ARIMA")
st.write("Carregue um arquivo Excel para realizar análises de séries temporais e gerar previsões.")

# Upload do arquivo
uploaded_file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

# Função para análise ARIMA
def analisar_arima(data, categoria, passos=6):
    try:
        # Ajustar o modelo ARIMA
        modelo = ARIMA(data, order=(1, 1, 1)).fit()
        previsoes = modelo.forecast(steps=passos)
        previsoes_indices = [f"Proj {i+1}" for i in range(passos)]
        
        # Gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(data, label="Valores Reais", marker="o", color="blue")
        plt.plot(range(len(data), len(data) + passos), previsoes, label="Projeções (ARIMA)", marker="x", color="red")
        plt.title(f"Projeções para {categoria}")
        plt.xlabel("Períodos")
        plt.ylabel("Valores")
        plt.grid()
        plt.legend()
        st.pyplot(plt)
        
        st.write(f"Projeções para os próximos {passos} períodos:", previsoes)
    except Exception as e:
        st.error(f"Erro ao ajustar o modelo ARIMA: {e}")

# Processamento do arquivo
if uploaded_file:
    try:
        # Carregar dados do Excel
        df = pd.read_excel(uploaded_file, index_col=0)
        st.write("Prévia dos Dados:")
        st.dataframe(df)

        # Selecionar categoria
        categoria = st.selectbox("Selecione a categoria para análise:", df.index)
        passos = st.slider("Número de períodos para projeção:", 1, 12, 6)

        # Realizar análise ARIMA
        if st.button("Analisar"):
            data = df.loc[categoria].dropna().values
            analisar_arima(data, categoria, passos)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
