
import plotly.graph_objects as go


def criar_mapa_neural(df):

    ocupacao = (
        df.groupby(
            ["neuronio_linha", "neuronio_coluna"]
        )
        .size()
        .reset_index(name="quantidade")
    )

    matriz = [[0 for _ in range(10)] for _ in range(10)]

    for _, registro in ocupacao.iterrows():

        linha = int(registro["neuronio_linha"])
        coluna = int(registro["neuronio_coluna"])

        matriz[linha][coluna] = registro["quantidade"]

    figura = go.Figure(
        data=go.Heatmap(
            z=matriz,
            colorscale="Viridis",
            colorbar=dict(title="Municípios")
        )
    )

    figura.update_layout(
        title="Mapa de ocupação da rede SOM",
        xaxis_title="Colunas dos neurônios",
        yaxis_title="Linhas dos neurônios"
    )

    return figura
