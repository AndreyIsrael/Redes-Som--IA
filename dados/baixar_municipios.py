
import requests
import pandas as pd
from pathlib import Path

# Caminho da pasta de dados
PASTA_DADOS = Path(__file__).parent

# API oficial do IBGE
URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

def baixar_municipios():

    print("Consultando a API do IBGE...")

    resposta = requests.get(URL, timeout=60)

    resposta.raise_for_status()

    dados = resposta.json()

    municipios = []

    for municipio in dados:

        codigo = str(municipio["id"]).zfill(7)

        nome = municipio["nome"]

        # Identificar a UF na estrutura retornada pela API
        uf = ""

        try:
            uf = municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"]
        except (KeyError, TypeError):
            try:
                uf = municipio["regiao-imediata"][
                    "regiao-intermediaria"
                ]["UF"]["sigla"]
            except (KeyError, TypeError):
                pass

        municipios.append({
            "id_municipio": codigo,
            "nome": nome,
            "uf": uf
        })

    tabela = pd.DataFrame(municipios)

    tabela = tabela.drop_duplicates(
        subset="id_municipio"
    )

    tabela = tabela.sort_values("nome")

    caminho = PASTA_DADOS / "municipios.csv"

    tabela.to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nDownload concluído!")
    print("Total de municípios:", len(tabela))
    print("Arquivo salvo em:", caminho)

    print("\nPrimeiros municípios:")
    print(tabela.head())

    if len(tabela) != 5570:
        print("ATENÇÃO: confira a quantidade de municípios.")

if __name__ == "__main__":
    baixar_municipios()
