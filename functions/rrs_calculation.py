
def rrs_calculation(data, quant_sensors, rho):
    # Cria uma cópia do DataFrame 'es' para armazenar os resultados de Rrs
    rrs = data['es'].copy()
    
    # Calcula Rrs utilizando a fórmula: Rrs = (Lw - Lsky * ρ) / Es
    rrs.iloc[:, 8:] = (data['lw'].iloc[:, 8:] - data['lsky'].iloc[:, 8:] * rho) / data['es'].iloc[:, 8:]

    # salva o DataFrame 'rrs' em um arquivo txt
    # rrs.to_csv('rrs.txt')

    # Organiza os resultados em um dicionário com base na quantidade de sensores
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

    # Retorna o dicionário de resultados
    return resultados
