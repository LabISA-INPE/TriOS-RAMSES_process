# Importa funções necessárias de módulos externos
from functions.read_trios_data import read_trios_data
from functions.normaliza import normaliza
import pandas as pd

def merge_and_get_points(ed, lsky, lw, lu, es, eu, depth_ED, quant_sensors):
    # Chama a função read_trios_data com os argumentos fornecidos
    res = read_trios_data(ed=ed, lsky=lsky, lw=lw, lu=lu, es=es, eu=eu, depth_ED=depth_ED, quant_sensors=quant_sensors)

    # Cria um DataFrame vazio chamado multi_full
    multi_full = pd.DataFrame()

    # Itera sobre os DataFrames resultantes e realiza normalização, mesclando os DataFrames normalizados
    for i in res:
        res[i] = normaliza(data=res[i])
        multi_full = pd.merge(multi_full, res[i], on='DateTime', suffixes=('_' + j, '_' + i)) if not multi_full.empty else res[i]
        j = i

    # Obtém o número de colunas do DataFrame 'lw'
    num_col = res['lw'].shape[1]

    # Divide o DataFrame resultante 'multi_full' em partes correspondentes aos diferentes sensores
    lw_ = multi_full.iloc[:, :num_col]
    lsky_ = multi_full.iloc[:, num_col:num_col*2-1]
    es_ = multi_full.iloc[:, num_col*2-1:num_col*3-2]

    # Se o número de sensores for 6, divide também para 'ed', 'eu' e 'lu'
    if quant_sensors == 6:
        ed_ = multi_full.iloc[:, num_col*3-2:num_col*4-3]
        eu_ = multi_full.iloc[:, num_col*4-3:num_col*5-4]
        lu_ = multi_full.iloc[:, num_col*5-4:num_col*6-5]

    # Concatena partes dos DataFrames 'lsky', 'es', 'ed', 'eu', 'lu'
    lsky_ = pd.concat([lsky_.iloc[:, :4], lw_.loc[:, 'DateTime'], lsky_.iloc[:, 4:]], axis=1)
    es_ = pd.concat([es_.iloc[:, :4], lw_.loc[:, 'DateTime'], es_.iloc[:, 4:]], axis=1)

    # Se o número de sensores for 6, concatena também para 'ed', 'eu' e 'lu'
    if quant_sensors == 6:
        ed_ = pd.concat([ed_.iloc[:, :4], lw_.loc[:, 'DateTime'], ed_.iloc[:, 4:]], axis=1)
        eu_ = pd.concat([eu_.iloc[:, :4], lw_.loc[:, 'DateTime'], eu_.iloc[:, 4:]], axis=1)
        lu_ = pd.concat([lu_.iloc[:, :4], lw_.loc[:, 'DateTime'], lu_.iloc[:, 4:]], axis=1)

    # Atribui nomes às colunas dos DataFrames resultantes
    lw_.columns = res['lw'].columns
    lsky_.columns = res['lsky'].columns
    es_.columns = res['es'].columns

    # Se o número de sensores for 6, atribui nomes também para 'ed', 'eu' e 'lu'
    if quant_sensors == 6:
        ed_.columns = res['ed'].columns
        eu_.columns = res['eu'].columns
        lu_.columns = res['lu'].columns

    # Obtém os nomes das colunas 'Comment', 'CommentSub1', 'CommentSub2', 'CommentSub3' de 'lw_'
    names = lw_['Comment']
    names1 = lw_['CommentSub1']
    names2 = lw_['CommentSub2']
    names3 = lw_['CommentSub3']

    # Cria um dicionário chamado 'results' com os DataFrames resultantes
    if quant_sensors == 6:
        results = {
            'lw': lw_,
            'lsky': lsky_,
            'es': es_,
            'ed': ed_,
            'eu': eu_,
            'lu': lu_
        }
    else:
        results = {
            'lw': lw_,
            'lsky': lsky_,
            'es': es_,
        }

    # Retorna os nomes das colunas e o dicionário de resultados
    return names, names1, names2, names3, results
