import pandas as pd

def sub_names(df, orig_name, new_name):
    # Cria um DataFrame com a coluna 'estacoes_id' contendo os valores da coluna 'CommentSub1'
    estacoes = pd.DataFrame({'estacoes_id': df.loc[:, 'CommentSub1']})
    
    # Itera sobre os nomes originais e substitui na coluna 'estacoes_id'
    for i in range(len(orig_name)):
        estacoes['estacoes_id'] = estacoes['estacoes_id'].str.replace(orig_name[i], new_name[i])
    
    # Concatena o DataFrame 'estacoes' com o DataFrame original
    df = pd.concat([estacoes, df], axis=1)
    return df

# Define uma função para renomear pontos para sensores com 6 estações
def rename_points_sensor_6(new_name, lw_, lsky_, es_, ed_, eu_, lu_, quant_sensors):
    # Obtém os nomes originais da coluna 'CommentSub1'
    orig_name = lw_['CommentSub1'].dropna().unique()

    # Aplica a função sub_names para cada DataFrame
    lw_ = sub_names(df=lw_, orig_name=orig_name, new_name=new_name)
    lsky_ = sub_names(df=lsky_, orig_name=orig_name, new_name=new_name)
    es_ = sub_names(df=es_, orig_name=orig_name, new_name=new_name)
    ed_ = sub_names(df=ed_, orig_name=orig_name, new_name=new_name)
    eu_ = sub_names(df=eu_, orig_name=orig_name, new_name=new_name)
    lu_ = sub_names(df=lu_, orig_name=orig_name, new_name=new_name)

    # Organiza os resultados em um dicionário
    resultados = {
        'lw': lw_,
        'lsky': lsky_,
        'es': es_,
        'ed': ed_,
        'eu': eu_,
        'lu': lu_,
    }
    
    return resultados

# Define uma função para renomear pontos para sensores com 3 estações
def rename_points_sensor_3(new_name, lw_, lsky_, es_, quant_sensors):
    # Obtém os nomes originais da coluna 'CommentSub1'
    orig_name = lw_['CommentSub1'].dropna().unique()

    # Aplica a função sub_names para cada DataFrame
    lw_ = sub_names(df=lw_, orig_name=orig_name, new_name=new_name)
    lsky_ = sub_names(df=lsky_, orig_name=orig_name, new_name=new_name)
    es_ = sub_names(df=es_, orig_name=orig_name, new_name=new_name)

    # Organiza os resultados em um dicionário
    resultados = {
        'lw': lw_,
        'lsky': lsky_,
        'es': es_,
    }

    return resultados

# Define uma função para atualizar os nomes dos pontos em DataFrames específicos
def update_name_points(rrs_filter, results, new_name, old_name, sensores):
    # Atualiza a coluna 'estacoes_id' no DataFrame rrs_filter
    rrs_filter['estacoes_id'] = new_name
    
    # Atualiza a coluna 'estacoes_id' nos DataFrames em results
    for sensor in results:
        results[sensor]['estacoes_id'] = results[sensor]['estacoes_id'].str.replace(old_name, new_name)

    # Atualiza a coluna 'estacoes_id' nos DataFrames específicos
    if sensores == 6:
        results['ed']['estacoes_id'] = results['ed']['estacoes_id'].str.replace(old_name, new_name)
        results['eu']['estacoes_id'] = results['eu']['estacoes_id'].str.replace(old_name, new_name)
        results['lu']['estacoes_id'] = results['lu']['estacoes_id'].str.replace(old_name, new_name)
    
    return rrs_filter, results