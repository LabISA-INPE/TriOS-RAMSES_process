from functions.read_trios_data import read_trios_data
from functions.normaliza import normaliza
import pandas as pd

def merge_and_get_points(ed, lsky, lw, lu, es, eu, depth_ED, quant_sensors):
    res = read_trios_data(ed = ed, lsky = lsky, lw = lw, lu = lu, es = es, eu = eu, depth_ED=depth_ED, quant_sensors=quant_sensors)
    
    # print(res['lw'].shape)
    # print(res['lsky'].shape)
    # print(res['es'].shape)
    # print(res['ed'].shape)
    # print(res['eu'].shape)
    # print(res['lu'].shape)

    multi_full = pd.DataFrame()
    for i in res:
        res[i] = normaliza(data=res[i])
        multi_full = pd.merge(multi_full, res[i], on='DateTime', suffixes=('_' + j, '_' + i)) if not multi_full.empty else res[i]
        j = i

    num_col = res['lw'].shape[1]
    lw_ = multi_full.iloc[:,:num_col]
    lsky_ = multi_full.iloc[:,num_col:num_col*2-1]
    es_ = multi_full.iloc[:,num_col*2-1:num_col*3-2]

    if quant_sensors == 6:
        ed_ = multi_full.iloc[:,num_col*3-2:num_col*4-3]
        eu_ = multi_full.iloc[:,num_col*4-3:num_col*5-4]
        lu_ = multi_full.iloc[:,num_col*5-4:num_col*6-5]

    # print(lw_.shape)
    # print(lsky_.shape)
    # print(es_.shape)
    # print(ed_.shape)
    # print(eu_.shape)
    # print(lu_.shape)

    lsky_ = pd.concat([lsky_.iloc[:,:4], lw_.loc[:,'DateTime'], lsky_.iloc[:,4:]], axis=1)
    es_ = pd.concat([es_.iloc[:,:4], lw_.loc[:,'DateTime'], es_.iloc[:,4:]], axis=1)

    if quant_sensors == 6:
        ed_ = pd.concat([ed_.iloc[:,:4], lw_.loc[:,'DateTime'], ed_.iloc[:,4:]], axis=1)
        eu_ = pd.concat([eu_.iloc[:,:4], lw_.loc[:,'DateTime'], eu_.iloc[:,4:]], axis=1)
        lu_ = pd.concat([lu_.iloc[:,:4], lw_.loc[:,'DateTime'], lu_.iloc[:,4:]], axis=1)

    # print(lw_.shape)
    # print(lsky_.shape)
    # print(es_.shape)
    # print(ed_.shape)
    # print(eu_.shape)
    # print(lu_.shape)

    lw_.columns = res['lw'].columns
    lsky_.columns = res['lsky'].columns
    es_.columns = res['es'].columns

    if quant_sensors == 6:
        ed_.columns = res['ed'].columns
        eu_.columns = res['eu'].columns
        lu_.columns = res['lu'].columns
    
    names = lw_['Comment']
    names1 = lw_['CommentSub1']
    names2 = lw_['CommentSub2']
    names3 = lw_['CommentSub3']
    # print(orig_name)

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

    return names, names1, names2, names3, results