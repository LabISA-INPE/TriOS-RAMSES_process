
def rrs_calculation(data, quant_sensors, rho):

    rrs = data['es'].copy()
    rrs.iloc[:,8:] = (data['lw'].iloc[:,8:] - data['lsky'].iloc[:,8:] * rho) / data['es'].iloc[:,8:]

    # rrs.to_csv('rrs.txt')

    if quant_sensors == 6:
        resultados = {
            'lw': data['lw'],
            'lsky': data['lsky'],
            'es': data['es'],
            'ed': data['ed'],
            'eu': data['eu'],
            'lu': data['lu'],
            'rrs': rrs
        }
    else:
        resultados = {
            'lw': data['lw'],
            'lsky': data['lw'],
            'es': data['es'],
            'rrs': rrs
        }

    return resultados