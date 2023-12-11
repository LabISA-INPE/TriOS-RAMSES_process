import numpy as np
import matplotlib.pyplot as plt

def rrs_filtering(rrs_filter):
    quantil_25 = np.percentile(rrs_filter[550], 25)
    quantil_75 = np.percentile(rrs_filter[550], 75)

    rrs_filter = rrs_filter.loc[(rrs_filter[550] < 1) & (rrs_filter[900] < 1) & (rrs_filter[400] < 1)]
    rrs_filter = rrs_filter.loc[rrs_filter[550] < quantil_75]
    rrs_filter = rrs_filter.loc[rrs_filter[550] > quantil_25]
    rrs_filter = rrs_filter.reset_index(drop=True)

    return rrs_filter

def plot(rrs_filter):
    figure = plt.figure()

    for w in range(rrs_filter.shape[0]):
        plt.plot(rrs_filter.columns[8:], rrs_filter.iloc[w, 8:], color='black', linestyle='dashed', linewidth=0.5)
        plt.text(rrs_filter.columns[-1], rrs_filter.iloc[w, -1], str(w), fontsize=9, ha='center', va='bottom')

    plt.title(rrs_filter.loc[0,'estacoes_id'])
    plt.xlabel('Wavelength')

    return figure

def rrs_results(rrs, rrs_filtered):
    rrs_median = rrs_filtered.drop(rrs.columns[1:8], axis=1).groupby('estacoes_id').median().reset_index()
    rrs_std = rrs_filtered.drop(rrs.columns[1:8], axis=1).groupby('estacoes_id').std().reset_index()
    
    results = {
        'rrs_filtered': rrs_filtered,
        'rrs_median': rrs_median,
        'rrs_std': rrs_std
    }

    return results