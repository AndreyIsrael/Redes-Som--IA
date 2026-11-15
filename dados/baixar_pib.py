
import requests
import pandas as pd
from pathlib import Path

PASTA = Path(__file__).parent

ANO = 2022

# PIB total dos municípios
URL_PIB = (
    "https://apisidra.ibge.gov.br/values/"
    f"t/5938/n6/all/v/37/p/{ANO}"
)

# População do Censo 2022
URL_POPULACAO = (
    "https://apisidra.ibge.gov.br/values/"
    f"t/4714/n6/all/v/93/p/{ANO}"
)


def consultar_sidra(url):

    resposta = requests.get(url, timeout=120)
    resposta.raise_for_status()

    dados = resposta.json()

    if not dados:
        raise ValueError("A API não retornou dados.")

    return pd.DataFrame(dados[1:])


def baixar_pib():

    print("Consultando PIB municipal no IBGE...")

    pib = consultar_sidra(URL_PIB)

    print("Consultando população do Censo 2022...")

    populacao = consultar_sidra(URL_POPULACAO)

    # Organizar PIB
    pib = pd.DataFrame({
        "id_municipio": (
            pib["D1C"].astype(str).str.zfill(7)
        ),
        "pib_mil_reais": pd.to_numeric(
            pib["V"], errors="coerce"
        )
    })

    # Organizar população
    populacao = pd.DataFrame({
        "id_municipio": (
            populacao["D1C"].astype(str).str.zfill(7)
        ),
        "populacao_2022": pd.to_numeric(
            populacao["V"], errors="coerce"
        )
    })

    # Juntar os dados pelo código IBGE
    base = pd.merge(
        pib,
        populacao,
        on="id_municipio",
        how="outer",
        validate="one_to_one"
    )

    # O PIB está em mil reais.
    # Multiplicamos por 1000 para obter reais.
    base["pib_per_capita"] = (
        base["pib_mil_reais"] * 1000
    ) / base["populacao_2022"]

    # Salvar resultado
    caminho = PASTA / "pib_per_capita.csv"

    base.to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n===== RESULTADO DO PIB =====")

    print("Ano de referência:", ANO)
    print("Municípios com PIB:", base["pib_mil_reais"].notna().sum())
    print(
        "Municípios com PIB per capita:",
        base["pib_per_capita"].notna().sum()
    )

    print("\nPrimeiros resultados:")

    print(base.head())

    print("\nArquivo salvo em:")
    print(caminho)


if __name__ == "__main__":
    baixar_pib()
