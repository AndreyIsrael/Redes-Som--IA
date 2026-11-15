
import plotly.express as px


def grafico_indicador(df, indicador):

    figura = px.scatter(
        df,
        x="neuronio_coluna",
        y="neuronio_linha",
        color=indicador,
        hover_name="nome",
        hover_data=["uf", "id_municipio"],
        color_continuous_scale="Viridis",
        title=f"Distribuição de {indicador} no mapa SOM"
    )

    figura.update_layout(
        xaxis_title="Coluna do neurônio",
        yaxis_title="Linha do neurônio"
    )

    return figura


def media_por_neuronio(df, indicador):

    medias = (
        df.groupby(
            ["neuronio_linha", "neuronio_coluna"]
        )[indicador]
        .mean()
        .reset_index()
    )

    figura = px.bar(
        medias,
        x="neuronio_coluna",
        y=indicador,
        color="neuronio_linha",
        title=f"Média de {indicador} por neurônio"
    )

    return figura
