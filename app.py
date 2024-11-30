import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
import openai

# Configuração da API da OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Função para verificar estacionaridade
def verificar_estacionaridade(serie):
    resultado = adfuller(serie)
    if resultado[1] > 0.05:
        st.write("A série não é estacionária. Aplicando diferenciação.")
        return np.diff(serie), True
    else:
        st.write("A série é estacionária.")
        return serie, False

# Função para calcular projeções com ARIMA
def calcular_projecao_arima(valores, colunas, categoria, passos=6):
    try:
        modelo_auto = auto_arima(valores, seasonal=False, stepwise=True, suppress_warnings=True)
        previsoes = modelo_auto.predict(n_periods=passos)
        previsoes_indices = [f"Proj {i+1}" for i in range(passos)]

        # Média Móvel
        media_movel = pd.Series(valores).rolling(window=3).mean()

        # Gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(colunas, valores, label=f"Valores Reais ({categoria})", marker="o", color="blue")
        ax.plot(previsoes_indices, previsoes, label=f"Projeção (ARIMA) ({categoria})", marker="x", color="red")
        ax.plot(colunas, media_movel, label=f"Média Móvel ({categoria})", linestyle="--", color="orange")
        ax.set_title(f"Projeção de {categoria}: Próximos {passos} Períodos (ARIMA e Média Móvel)")
        ax.set_xlabel("Períodos")
        ax.set_ylabel("Valores")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao ajustar o modelo ARIMA para {categoria}: {e}")

# Função para gerar relatório com a OpenAI
def gerar_relatorio_ia(dados_analise):
    prompt = f"""
    Com base nos seguintes dados financeiros:

    Crescimento Anual da Receita Bruta: {dados_analise['crescimento_anual_receita']}
    Crescimento do Lucro Bruto: {dados_analise['crescimento_lucro_bruto']:.2f}%
    Crescimento do Lucro Líquido: {dados_analise['crescimento_lucro_liquido']:.2f}%
    Despesas Relativas à Receita Bruta: {dados_analise['despesas_percentuais']}
    Percentual Médio de CPV/CMV: {dados_analise['cpv_percentual']:.2f}%

    Gere um relatório detalhado que inclua:
    - Análise do crescimento da receita.
    - Impacto das despesas no resultado financeiro.
    - Recomendações para melhorar os resultados.
    """
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um analista financeiro especialista."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return resposta["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Erro ao acessar a API da OpenAI: {str(e)}"

# Interface Streamlit
st.title("Análise Financeira com IA e ARIMA")
st.write("Faça upload de um arquivo Excel contendo dados financeiros para análise.")

uploaded_file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])
if uploaded_file:
    try:
        # Ler o conteúdo do arquivo Excel
        dados = pd.read_excel(uploaded_file, index_col=0)
        dados.index.name = "Categoria"

        st.write("Categorias disponíveis no arquivo:")
        st.write(dados.index.tolist())

        # Análise dos dados
        receita_bruta, crescimento_anual = crescimento_anual_receita(dados)
        st.write("Crescimento Anual da Receita Bruta:")
        st.write(crescimento_anual)

        # Gerar relatórios
        dados_analise = {
            "crescimento_anual_receita": crescimento_anual.dropna().to_dict(),
            "crescimento_lucro_bruto": 10.0,  # Exemplo estático para simplificar
            "crescimento_lucro_liquido": 15.0,
            "despesas_percentuais": {"Venda": 30.0, "Administrativa": 20.0},
            "cpv_percentual": 50.0
        }
        relatorio = gerar_relatorio_ia(dados_analise)
        st.subheader("Relatório Gerado pela IA:")
        st.write(relatorio)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
