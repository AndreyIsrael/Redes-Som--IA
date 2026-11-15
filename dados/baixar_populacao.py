
import requests
import pandas as pd
from pathlib import Path

# Caminho da pasta de dados
PASTA = Path(__file__).parent

# API do SIDRA - IBGE
URL = (
    "https://apisidra.ibge.gov.br/values/"
    "t/6579/n6/all/v/9324/p/2026"
)


def baixar_populacao():

    print("Consultando população no IBGE...")

    resposta = requests.get(URL, timeout=120)

    resposta.raise_for_status()

    dados = resposta.json()

    # Transformar os dados recebidos em tabela
    df = pd.DataFrame(dados[1:])

    # Identificar as colunas corretas
    coluna_codigo = "D1C"
    coluna_valor = "V"

    # Verificar se as colunas existem
    if coluna_codigo not in df.columns:
        raise ValueError("Código do município não encontrado.")

    if coluna_valor not in df.columns:
        raise ValueError("Valor da população não encontrado.")

    # Criar nossa tabela organizada
    populacao = pd.DataFrame({

        "id_municipio": (
            df[coluna_codigo]
            .astype(str)
            .str.zfill(7)
        ),

        "populacao": pd.to_numeric(
            df[coluna_valor],
            errors="coerce"
        )

    })

    # Remover valores ausentes
    populacao = populacao.dropna(
        subset=["populacao"]
    )

    # Remover possíveis duplicações
    populacao = populacao.drop_duplicates(
        subset="id_municipio"
    )

    # Salvar CSV
    caminho = PASTA / "populacao.csv"

    populacao.to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nDownload concluído!")

    print(
        "Total de municípios:",
        len(populacao)
    )

    print("\nPrimeiros resultados:")

    print(populacao.head())

    print("\nArquivo salvo em:")
    print(caminho)


if __name__ == "__main__":

    baixar_populacao()
