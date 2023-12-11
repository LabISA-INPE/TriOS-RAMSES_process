import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def normaliza(data):

    radiometric = data.iloc[:, 7:]
    wavelengths = pd.to_numeric(data.columns[7:])
    
    df = radiometric.transpose()
    normalizado = pd.DataFrame({'Wave': range(400, 901)})

    df_base = pd.DataFrame(data=np.zeros((501, df.shape[1])))
    normalizado = pd.concat([normalizado, df_base], axis=1)
    
    for i in range(df.shape[1]):
        df.iloc[:,i] = pd.to_numeric(df.iloc[:,i], errors='coerce')

        if not pd.isna(df.iloc[0,i]):
            interp_func = interp1d(wavelengths, df.iloc[:,i], kind='linear', fill_value='extrapolate', bounds_error=False)
            normalizado.iloc[:,i+1] = interp_func(range(400,901))

    df_normalized = normalizado.iloc[:,1:].transpose().dropna()
    df_normalized.index = data.index
    data_normalized = pd.concat([data.iloc[:,:7], df_normalized], axis=1, ignore_index=True)
    data_normalized.columns = list(data.columns[:7]) + [i for i in range(400,901)]

    # data_normalized.to_csv(f'normalizado.txt')
    
    return data_normalized