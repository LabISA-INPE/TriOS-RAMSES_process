import pandas as pd

def sub_names(df, orig_name, new_name):
    estacoes = pd.DataFrame({'estacoes_id': df.loc[:, 'CommentSub1']})
    for i in range(len(orig_name)):
        estacoes['estacoes_id'] = estacoes['estacoes_id'].str.replace(orig_name[i], new_name[i])
    df = pd.concat([estacoes, df], axis=1)
    return df

def rename_points_sensor_6(new_name, lw_, lsky_, es_, ed_, eu_, lu_, quant_sensors):
    orig_name = lw_['CommentSub1'].dropna().unique()

    lw_ = sub_names(df=lw_, orig_name=orig_name, new_name=new_name)
    lsky_ = sub_names(df=lsky_, orig_name=orig_name, new_name=new_name)
    es_ = sub_names(df=es_, orig_name=orig_name, new_name=new_name)
    ed_ = sub_names(df=ed_, orig_name=orig_name, new_name=new_name)
    eu_ = sub_names(df=eu_, orig_name=orig_name, new_name=new_name)
    lu_ = sub_names(df=lu_, orig_name=orig_name, new_name=new_name)

    resultados = {
        'lw': lw_,
        'lsky': lsky_,
        'es': es_,
        'ed': ed_,
        'eu': eu_,
        'lu': lu_,
    }
    
    return resultados

def rename_points_sensor_3(new_name, lw_, lsky_, es_, quant_sensors):
    orig_name = lw_['CommentSub1'].dropna().unique()

    lw_ = sub_names(df=lw_, orig_name=orig_name, new_name=new_name)
    lsky_ = sub_names(df=lsky_, orig_name=orig_name, new_name=new_name)
    es_ = sub_names(df=es_, orig_name=orig_name, new_name=new_name)

    resultados = {
        'lw': lw_,
        'lsky': lsky_,
        'es': es_,
    }

    return resultados

def update_name_points(rrs_filter, results, new_name, old_name, sensores):
    rrs_filter['estacoes_id'] = new_name
    results['rrs']['estacoes_id'] = results['rrs']['estacoes_id'].str.replace(old_name, new_name)
    results['lw']['estacoes_id'] = results['lw']['estacoes_id'].str.replace(old_name, new_name)
    results['lsky']['estacoes_id'] = results['lsky']['estacoes_id'].str.replace(old_name, new_name)
    results['es']['estacoes_id'] = results['es']['estacoes_id'].str.replace(old_name, new_name)

    if sensores == 6:
        results['ed']['estacoes_id'] = results['ed']['estacoes_id'].str.replace(old_name, new_name)
        results['eu']['estacoes_id'] = results['eu']['estacoes_id'].str.replace(old_name, new_name)
        results['lu']['estacoes_id'] = results['lu']['estacoes_id'].str.replace(old_name, new_name)
    
    return rrs_filter, results