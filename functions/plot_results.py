import matplotlib.pyplot as plt
import numpy as np

def plot_results(results, rrs_calculated):
    points = list(rrs_calculated['rrs_median']['estacoes_id'].unique())

    # Calculando as linhas e colunas do gráfico dinamicamente
    num_colunas = int(np.ceil(np.sqrt(len(points))))
    num_linhas = int(np.ceil(len(points) / num_colunas))
    
    # Configuração dos subplots dinâmicos
    fig, axs = plt.subplots(num_linhas, num_colunas, figsize=(8, 6))

    # Flattening da matriz de subplots para facilitar o acesso
    axs = axs.flatten()

    for i, p in enumerate(points):
        rrs_filtered = results['rrs'].loc[results['rrs']['estacoes_id'] == p]
        rrs_median = rrs_calculated['rrs_median'].loc[rrs_calculated['rrs_median']['estacoes_id'] == p]

        axs[i].set_title(points[i])
        axs[i].set_ylabel('Rrs')
        axs[i].set_xlabel('Wavelength')
        axs[i].set_ylim([0, 0.05])

        for w in range(rrs_filtered.shape[0]):
            axs[i].plot(rrs_filtered.columns[8:], rrs_filtered.iloc[w, 8:], label=None, color='red', linewidth=0.5)
        
        axs[i].plot(rrs_median.columns[1:], rrs_median.iloc[0, 1:], label=None, color='black', linewidth=1)

    # Ajustando espaçamento dos gráficos
    plt.tight_layout()

    plt.show(block=False)

    return fig