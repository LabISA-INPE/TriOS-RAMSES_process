import pandas as pd

def read_trios_data(es, lw, lsky, eu, ed, lu, depth_ED, quant_sensors):
    # Dicionário para armazenar os resultados para cada sensor
    result = {}
    # Nomes dos sensores
    names = ('lw', 'lsky', 'es', 'ed', 'eu', 'lu')

    # Leitura dos dados dos sensores lw, lsky e es
    es = pd.read_csv(es, delimiter="\t", index_col=0, header=1)
    lw = pd.read_csv(lw, delimiter="\t", index_col=0, header=1)
    lsky = pd.read_csv(lsky, delimiter="\t", index_col=0, header=1)

    # Leitura dos dados adicionais para sensores eu, ed e lu se houver 6 sensores
    if quant_sensors == 6:
        eu = pd.read_csv(eu,  delimiter="\t", index_col=0, header=1)
        ed = pd.read_csv(ed, delimiter="\t", index_col=0, header=1)
        lu = pd.read_csv(lu, delimiter="\t", index_col=0, header=1)

    # Verifica a quantidade de sensores e atribui a tupla correspondente
    if quant_sensors == 6:
        sensors = (lw, lsky, es, ed, eu, lu)
    else:
        sensors = (lw, lsky, es)

    # Loop sobre os sensores
    for i, equip in enumerate(sensors):
        # Cria um DataFrame para armazenar informações básicas(nomes dos pontos) do sensor
        df = pd.DataFrame({
            'Comment': equip.loc["Comment",:].values,
            'CommentSub1': equip.loc['CommentSub1',:].values,
            'CommentSub2': equip.loc['CommentSub2',:].values,
            'CommentSub3': equip.loc['CommentSub3',:].values,
            'DateTime': equip.loc['DateTime'],
        })

        # Adiciona informações de pressão ou IDDevice com base no tipo de sensor
        pressure = depth_ED if names[i] == 'ed' else False
        if pressure:
            df['Pressure'] = equip.loc['Pressure',:].values
        else:
            df['IDDevice'] = equip.loc['IDDevice',:].values

        # Seleciona a parte do DataFrame contendo as medidas espectrais
        df_medidas = equip.iloc[equip.index.get_loc('[Data]')+29 : equip.index.get_loc('[END] of [Spectrum]')-75 :]
        df = pd.concat([df, df_medidas.transpose()], axis=1)
        
        # Converte a coluna 'DateTime' para formato datetime
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')

        # Armazena o DataFrame resultante no dicionário de resultados
        result[names[i]] = df
        
        # Salva o DataFrame em um arquivo de teste (comentado por enquanto)
        # df.to_csv(f'teste{i}.txt')

    # Retorna o dicionário de resultados
    return result