
import pandas as pd
from pathlib import Path

PASTA = Path(__file__).parent

# Carregar os arquivos
municipios = pd.read_csv(
    PASTA / "municipios.csv",
    dtype={"id_municipio": str}
)

populacao = pd.read_csv(
    PASTA / "populacao.csv",
    dtype={"id_municipio": str}
)

print("Integrando dados dos municípios...")

# Relacionar os arquivos pelo código IBGE
base = pd.merge(
    municipios,
    populacao,
    on="id_municipio",
    how="left",
    validate="one_to_one"
)

# Verificar dados encontrados e ausentes
total = len(base)
com_populacao = base["populacao"].notna().sum()
sem_populacao = base["populacao"].isna().sum()

print("\n===== RESULTADO DA INTEGRAÇÃO =====")

print("Total de municípios:", total)
print("Com população:", com_populacao)
print("Sem população:", sem_populacao)

# Mostrar municípios sem informação
if sem_populacao > 0:
    print("\nMunicípios sem população:")
    print(
        base.loc[
            base["populacao"].isna(),
            ["id_municipio", "nome", "uf"]
        ].head(20)
    )

# Salvar a base integrada
caminho = PASTA / "indicadores.csv"

base[
    ["id_municipio", "populacao"]
].to_csv(
    caminho,
    index=False,
    encoding="utf-8-sig"
)

print("\nBase integrada salva!")
print("Arquivo:", caminho)

print("\nAmostra dos dados:")
print(base.head())
