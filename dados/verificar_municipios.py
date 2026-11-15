
import pandas as pd
from pathlib import Path

arquivo = Path(__file__).parent / "municipios.csv"

df = pd.read_csv(arquivo, dtype={"id_municipio": str})

print("===== VALIDAÇÃO DOS MUNICÍPIOS =====")

print("Total de registros:", len(df))

print(
    "Códigos duplicados:",
    df["id_municipio"].duplicated().sum()
)

print(
    "Nomes ausentes:",
    df["nome"].isna().sum()
)

print(
    "UFs ausentes:",
    df["uf"].isna().sum()
)

print(
    "Quantidade de UFs:",
    df["uf"].nunique()
)

print("\nNovo município:")

print(
    df[df["nome"] == "Boa Esperança do Norte"]
)

print("\nPrimeiros registros:")
print(df.head())
