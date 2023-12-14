
def save_files(save_path, results, rrs_calculated, plot, sensores):
    # Salva os DataFrames 'lw', 'lsky', e 'es' em arquivos CSV
    results['lw'].to_csv(save_path + "/lw.csv")
    results['lsky'].to_csv(save_path + "/lsky.csv")
    results['es'].to_csv(save_path + "/es.csv")

    # Salva os DataFrames 'ed', 'eu', e 'lu' em arquivos CSV se houver 6 sensores
    if sensores == 6:
        results['ed'].to_csv(save_path + "/ed.csv")
        results['eu'].to_csv(save_path + "/eu.csv")
        results['lu'].to_csv(save_path + "/lu.csv")

    # Salva os DataFrames 'rrs_filtered', 'rrs_median', e 'rrs_std' em arquivos CSV
    rrs_calculated['rrs_filtered'].to_csv(save_path + "/rrs_completa.csv")
    rrs_calculated['rrs_median'].to_csv(save_path + "/rrs_mediana.csv")
    rrs_calculated['rrs_std'].to_csv(save_path + "/rrs_std.csv")

    # Salva o gráfico em um arquivo de imagem no formato JPG
    plot.savefig(save_path + '/plot.jpg')