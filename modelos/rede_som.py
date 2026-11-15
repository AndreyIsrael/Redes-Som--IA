
import math
import random


class RedeSOM:

    def __init__(
        self,
        linhas,
        colunas,
        dimensoes,
        taxa_aprendizado=0.5,
        sigma=None,
        epocas=10,
        semente=42
    ):

        self.linhas = linhas
        self.colunas = colunas
        self.dimensoes = dimensoes

        self.taxa_inicial = taxa_aprendizado

        self.sigma_inicial = (
            sigma if sigma is not None
            else max(linhas, colunas) / 2
        )

        self.epocas = epocas

        random.seed(semente)

        # Inicialização dos pesos
        self.pesos = []

        for i in range(linhas):

            linha = []

            for j in range(colunas):

                neuronio = [
                    random.random()
                    for _ in range(dimensoes)
                ]

                linha.append(neuronio)

            self.pesos.append(linha)

    # Distância euclidiana
    def distancia(self, vetor1, vetor2):

        soma = 0

        for i in range(self.dimensoes):

            diferenca = vetor1[i] - vetor2[i]

            soma += diferenca ** 2

        return math.sqrt(soma)

    # Encontrar o neurônio vencedor
    def encontrar_bmu(self, entrada):

        menor_distancia = float("inf")

        melhor_neuronio = (0, 0)

        for i in range(self.linhas):

            for j in range(self.colunas):

                distancia = self.distancia(
                    entrada,
                    self.pesos[i][j]
                )

                if distancia < menor_distancia:

                    menor_distancia = distancia

                    melhor_neuronio = (i, j)

        return melhor_neuronio

    # Função de vizinhança gaussiana
    def vizinhanca(self, distancia_mapa, sigma):

        return math.exp(
            -(distancia_mapa ** 2) /
            (2 * sigma ** 2)
        )

    # Atualizar pesos dos neurônios
    def atualizar_pesos(
        self,
        entrada,
        bmu,
        taxa,
        sigma
    ):

        bmu_linha, bmu_coluna = bmu

        for i in range(self.linhas):

            for j in range(self.colunas):

                distancia_mapa = math.sqrt(
                    (i - bmu_linha) ** 2 +
                    (j - bmu_coluna) ** 2
                )

                influencia = self.vizinhanca(
                    distancia_mapa,
                    sigma
                )

                for k in range(self.dimensoes):

                    peso_atual = self.pesos[i][j][k]

                    diferenca = (
                        entrada[k] - peso_atual
                    )

                    self.pesos[i][j][k] += (
                        taxa * influencia * diferenca
                    )

    # Processo de treinamento
    def treinar(self, dados):

        total = len(dados)

        for epoca in range(self.epocas):

            taxa = (
                self.taxa_inicial *
                math.exp(-epoca / self.epocas)
            )

            sigma = (
                self.sigma_inicial *
                math.exp(-epoca / self.epocas)
            )

            ordem = list(range(total))

            random.shuffle(ordem)

            erro_total = 0

            for indice in ordem:

                entrada = dados[indice]

                bmu = self.encontrar_bmu(entrada)

                erro_total += self.distancia(
                    entrada,
                    self.pesos[bmu[0]][bmu[1]]
                )

                self.atualizar_pesos(
                    entrada,
                    bmu,
                    taxa,
                    sigma
                )

            erro_medio = erro_total / total

            print(
                f"Época {epoca + 1}/{self.epocas} "
                f"| Erro médio: {erro_medio:.6f}"
            )

        print("\nTreinamento concluído!")

    # Mapear cada entrada para seu neurônio vencedor
    def mapear(self, dados):

        resultados = []

        for entrada in dados:

            bmu = self.encontrar_bmu(entrada)

            resultados.append(bmu)

        return resultados
