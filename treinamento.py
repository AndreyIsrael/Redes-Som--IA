
import pandas as pd
from pathlib import Path

from modelos.rede_som import RedeSOM
from processamento.normalizacao import normalizar_dados


PASTA = Path(__file__).parent

ARQUIVO = PASTA / "dados" / "indicadores.csv"
RESULTADO = PASTA / "dados" / "resultados_som.csv"

INDICADORES = [
    "populacao",
    "pib_per_capita"
]


def executar_treinamento():

    print("Carregando dados dos municípios...")

    df = pd.read_csv(
        ARQUIVO,
        dtype={"id_municipio": str}
    )

    # Conferir colunas
    for coluna in INDICADORES:
        if coluna not in df.columns:
            raise ValueError(
                f"Coluna não encontrada: {coluna}"
            )

    # Converter indicadores para números
    for coluna in INDICADORES:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    # Remover dados ausentes ou inválidos
    df = df.dropna(
        subset=INDICADORES
    ).copy()

    if len(df) < 2:
        raise ValueError(
            "Precisamos de pelo menos dois municípios."
        )

    if (df[INDICADORES] < 0).any().any():
        raise ValueError(
            "Foram encontrados indicadores negativos."
        )

    print("Municípios disponíveis:", len(df))

    # Normalizar dados
    df_normalizado, parametros = normalizar_dados(
        df,
        INDICADORES
    )

    dados = df_normalizado[
        INDICADORES
    ].values.tolist()

    print("\nInicializando rede SOM...")

    rede = RedeSOM(
        linhas=10,
        colunas=10,
        dimensoes=2,
        taxa_aprendizado=0.5,
        epocas=30,
        semente=42
    )

    print("\nIniciando treinamento...\n")

    rede.treinar(dados)

    # Encontrar neurônio vencedor de cada município
    coordenadas = rede.mapear(dados)

    df["neuronio_linha"] = [
        posicao[0] for posicao in coordenadas
    ]

    df["neuronio_coluna"] = [
        posicao[1] for posicao in coordenadas
    ]

    # Salvar resultados
    df.to_csv(
        RESULTADO,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n===== RESULTADO DO TREINAMENTO =====")

    print("Municípios treinados:", len(df))

    print("Indicadores utilizados:", INDICADORES)

    print("Neurônios:", 100)

    print("Resultado salvo em:", RESULTADO)

    return rede, df


if __name__ == "__main__":
    executar_treinamento()
