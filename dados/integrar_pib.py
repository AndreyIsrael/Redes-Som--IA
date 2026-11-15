
import pandas as pd
from pathlib import Path

PASTA = Path(__file__).parent

# Carregar nossa base atual
indicadores = pd.read_csv(
    PASTA / "indicadores.csv",
    dtype={"id_municipio": str}
)

# Carregar PIB
pib = pd.read_csv(
    PASTA / "pib_per_capita.csv",
    dtype={"id_municipio": str}
)

# Verificar códigos duplicados
if pib["id_municipio"].duplicated().any():
    raise ValueError("Existem códigos duplicados no PIB.")

# Selecionar informações necessárias
pib = pib[
    ["id_municipio", "pib_per_capita"]
]

# Integrar as bases
base = pd.merge(
    indicadores,
    pib,
    on="id_municipio",
    how="left",
    validate="one_to_one"
)

# Verificar resultado
print("===== INTEGRAÇÃO DO PIB =====")

print("Total de municípios:", len(base))

print(
    "Municípios com PIB:",
    base["pib_per_capita"].notna().sum()
)

print(
    "Municípios sem PIB:",
    base["pib_per_capita"].isna().sum()
)

# Salvar
base.to_csv(
    PASTA / "indicadores.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nIntegração concluída!")
print(base.head())
