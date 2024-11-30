import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Configurações iniciais do Streamlit
st.set_page_config(page_title="Análise Financeira", layout="wide")

# Funções para análise
def crescimento_anual_receita(dados):
    colunas_temporais = pd.to_datetime(dados.columns, format="%b-%Y", errors="coerce")
    dados.columns = colunas_temporais

    receita_bruta = dados.loc["Receita Bruta"]
    receita_anual = receita_bruta.resample("Y").sum()
    crescimento_anual = receita_anual.pct_change() * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(receita_anual.index.year, receita_anual.values, color="skyblue", label="Receita Anual (R$)")
    ax.plot(receita_anual.index.year, receita_anual.values, marker="o", color="blue", label="Receita Bruta")
    ax.set_title("Crescimento Anual da Receita Bruta")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Valores (em R$)")
    ax.grid(True, linestyle="--", alpha=0.6)

    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{receita_anual.values[i]:,.2f}", ha="center", fontsize=10)
        if i > 0 and not np.isnan(crescimento_anual.values[i]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, f"{crescimento_anual.values[i]:.2f}%", ha="center", fontsize=10, color="red")

    ax.legend()
    st.pyplot(fig)

def analisar_tendencia_lucros(dados):
    lucro_bruto = dados.loc["(=) Lucro Bruto"]
    lucro_liquido = dados.loc["(=) Resultado Líquido"]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(lucro_bruto.index, lucro_bruto.values, label="Lucro Bruto", marker="o", color="green")
    ax.plot(lucro_liquido.index, lucro_liquido.values, label="Lucro Líquido", marker="o", color="orange")
    ax.set_title("Tendência do Lucro Bruto e Lucro Líquido")
    ax.set_xlabel("Período")
    ax.set_ylabel("Valores (em R$)")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend()
    st.pyplot(fig)

def analisar_despesas(dados):
    despesas_categorias = [
        "(-) Despesas com Vendas",
        "(-) Despesas Administrativas",
        "(-) Despesas Financeiras"
    ]

    despesas_percentuais = dados.loc[despesas_categorias].div(dados.loc["Receita Bruta"]) * 100

    fig, ax = plt.subplots(figsize=(12, 6))
    for categoria in despesas_categorias:
        ax.plot(despesas_percentuais.columns, despesas_percentuais.loc[categoria], label=categoria, marker="o")
    ax.set_title("Despesas Relativas à Receita Bruta (%)")
    ax.set_xlabel("Período")
    ax.set_ylabel("Percentual (%)")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend()
    st.pyplot(fig)

# Upload do arquivo no Streamlit
st.title("Análise Financeira Interativa")
uploaded_file = st.file_uploader("Faça o upload de um arquivo Excel com os dados financeiros:", type="xlsx")

if uploaded_file:
    dados = pd.read_excel(uploaded_file, index_col=0)
    dados.index.name = "Categoria"
    st.success("Dados carregados com sucesso!")

    # Explorando os dados
    st.header("1. Crescimento Anual da Receita Bruta")
    crescimento_anual_receita(dados)

    st.header("2. Tendência do Lucro Bruto e Lucro Líquido")
    analisar_tendencia_lucros(dados)

    st.header("3. Despesas Relativas à Receita Bruta")
    analisar_despesas(dados)
