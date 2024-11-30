6))
        plt.plot(colunas, valores, label=f"Valores Reais ({categoria})", marker="o", color="blue")
        plt.plot(previsoes_indices, previsoes, label=f"Projeção (ARIMA) ({categoria})", marker="x", color="red")
        plt.plot(colunas, media_movel, label=f"Média Móvel ({categoria})", linestyle="--", color="orange")
        plt.title(f"Projeção de {categoria}: Próximos {passos} Períodos (ARIMA e Média Móvel)")
        plt.xlabel("Períodos")
        plt.ylabel("Valores")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Erro ao ajustar o modelo ARIMA para {categoria}: {e}")

# Função para analisar os dados
def explorar_dados(dados):
    print("Explorando os dados fornecidos...")

    for categoria in dados.index:
        valores = dados.loc[categoria].astype(float).values
        colunas = dados.columns
        print(f"\nAnalisando a categoria: {categoria}")
        calcular_projecao_arima(valores, colunas, categoria)

# Gerar relatório com a OpenAI
def gerar_relatorio_ia(dados_analise):
    prompt = f"""
    Com base nos seguintes dados financeiros:

    - Crescimento Anual da Receita Bruta: {dados_analise['crescimento_anual']}
    - Percentuais de Despesas: {dados_analise['despesas_percentuais']}
    - Percentual Médio de CPV/CMV: {dados_analise['cpv_percentual']}

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

# Função para processar o upload do arquivo
def processar_upload(change):
    with output:
        output.clear_output()  # Limpa mensagens anteriores
        try:
            uploaded_file = next(iter(upload.value.values()))
            content = uploaded_file['content']

            # Ler o conteúdo do arquivo Excel
            dados = pd.read_excel(BytesIO(content), index_col=0)
            dados.index.name = "Categoria"

            print("Categorias disponíveis no arquivo:")
            print(dados.index.tolist())

            # Análise dos dados
            explorar_dados(dados)

            # Gerar relatório com OpenAI
            dados_analise = {
                "crescimento_anual": "Exemplo de Crescimento",  # Substituir com cálculo real
                "despesas_percentuais": "Exemplo de Percentuais",  # Substituir com cálculo real
                "cpv_percentual": "Exemplo de CPV/CMV"  # Substituir com cálculo real
            }
            relatorio = gerar_relatorio_ia(dados_analise)
            print("\nRelatório Gerado pela IA:")
            print(relatorio)
        except Exception as e:
            print(f"Erro ao processar o upload: {e}")

# Componente de upload de arquivo
upload = FileUpload(
    accept=".xlsx",  # Aceitar somente arquivos Excel
    multiple=False   # Permitir apenas um arquivo por vez
)
upload.observe(processar_upload, names='value')

# Exibir interface
print("Por favor, faça o upload do arquivo Excel com os dados financeiros:")
display(VBox([upload, output]))
