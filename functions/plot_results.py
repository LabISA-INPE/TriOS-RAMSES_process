import matplotlib.pyplot as plt
import numpy as np

def plot_results(results, rrs_calculated):
    # Obtém os pontos únicos das estações a partir da coluna 'estacoes_id' em rrs_calculated['rrs_median']
    points = list(rrs_calculated['rrs_median']['estacoes_id'].unique())

    # Calcula dinamicamente o número de colunas e linhas do gráfico com base no número de pontos
    num_colunas = int(np.ceil(np.sqrt(len(points))))
    num_linhas = int(np.ceil(len(points) / num_colunas))
    
    # Configuração dos subplots dinâmicos
    fig, axs = plt.subplots(num_linhas, num_colunas, figsize=(8, 6))

    # Flattening da matriz de subplots para facilitar o acesso
    axs = axs.flatten()

    # Itera sobre os pontos e cria subplots individuais
    for i, p in enumerate(points):
        # Filtra os resultados 'rrs' para a estação específica
        rrs_filtered = results['rrs'].loc[results['rrs']['estacoes_id'] == p]
        
        # Obtém os valores medianos de 'rrs' para a estação específica
        rrs_median = rrs_calculated['rrs_median'].loc[rrs_calculated['rrs_median']['estacoes_id'] == p]

        # Configurações do subplot
        axs[i].set_title(points[i])
        axs[i].set_ylabel('Rrs')
        axs[i].set_xlabel('Wavelength')
        axs[i].set_ylim([0, 0.05])

        # Plota os espectros 'rrs' filtrados em vermelho
        for w in range(rrs_filtered.shape[0]):
            axs[i].plot(rrs_filtered.columns[8:], rrs_filtered.iloc[w, 8:], label=None, color='red', linewidth=0.5)
        
        # Plota o espectro mediano em preto
        axs[i].plot(rrs_median.columns[1:], rrs_median.iloc[0, 1:], label=None, color='black', linewidth=1)

    # Ajusta o espaçamento entre os gráficos
    plt.tight_layout()

    # Exibe o gráfico
    plt.show(block=False)

    # Retorna a figura criada
    return fig
