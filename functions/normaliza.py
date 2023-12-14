import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def normaliza(data):
    # Extrai os dados radiométricos do DataFrame a partir da coluna 7 em diante
    radiometric = data.iloc[:, 7:]
    
    # Obtém os comprimentos de onda como números a partir dos nomes das colunas
    wavelengths = pd.to_numeric(data.columns[7:])
    
    # Transpõe os dados radiométricos e cria um DataFrame 'normalizado' com coluna 'Wave' de 400 a 900
    df = radiometric.transpose()
    normalizado = pd.DataFrame({'Wave': range(400, 901)})

    # Cria um DataFrame base com zeros para armazenar os dados normalizados
    df_base = pd.DataFrame(data=np.zeros((501, df.shape[1])))
    normalizado = pd.concat([normalizado, df_base], axis=1)
    
    # Itera sobre as colunas dos dados radiométricos e realiza interpolação linear
    for i in range(df.shape[1]):
        # Converte os valores para números, tratando erros como NaN
        df.iloc[:,i] = pd.to_numeric(df.iloc[:,i], errors='coerce')

        # Se o primeiro valor não for NaN, realiza a interpolação linear
        if not pd.isna(df.iloc[0,i]):
            interp_func = interp1d(wavelengths, df.iloc[:,i], kind='linear', fill_value='extrapolate', bounds_error=False)
            normalizado.iloc[:,i+1] = interp_func(range(400,901))

    # Transpõe novamente os dados normalizados, elimina NaNs e define o índice
    df_normalized = normalizado.iloc[:,1:].transpose().dropna()
    df_normalized.index = data.index

    # Concatena os dados normalizados com as primeiras 7 colunas do DataFrame original
    data_normalized = pd.concat([data.iloc[:,:7], df_normalized], axis=1, ignore_index=True)
    
    # Renomeia as colunas para terem números de 400 a 900
    data_normalized.columns = list(data.columns[:7]) + [i for i in range(400,901)]

    # Salva os dados normalizados em um arquivo "normalizado.txt" (comentado por enquanto)
    # data_normalized.to_csv(f'normalizado.txt')
    
    # Retorna os dados normalizados
    return data_normalized
