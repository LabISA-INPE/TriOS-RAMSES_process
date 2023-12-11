import pandas as pd

def read_trios_data(es, lw, lsky, eu, ed, lu, depth_ED, quant_sensors):

    result = {}
    names = ('lw', 'lsky', 'es', 'ed', 'eu', 'lu')

    es = pd.read_csv(es, delimiter="\t", index_col=0, header=1)
    lw = pd.read_csv(lw, delimiter="\t", index_col=0, header=1)
    lsky = pd.read_csv(lsky, delimiter="\t", index_col=0, header=1)

    if quant_sensors == 6:
        eu = pd.read_csv(eu,  delimiter="\t", index_col=0, header=1)
        ed = pd.read_csv(ed, delimiter="\t", index_col=0, header=1)
        lu = pd.read_csv(lu, delimiter="\t", index_col=0, header=1)

    if quant_sensors == 6:
        sensors = (lw, lsky, es, ed, eu, lu)
    else:
        sensors = (lw, lsky, es)

    for i, equip in enumerate(sensors):

        df = pd.DataFrame({
            'Comment': equip.loc["Comment",:].values,
            'CommentSub1': equip.loc['CommentSub1',:].values,
            'CommentSub2': equip.loc['CommentSub2',:].values,
            'CommentSub3': equip.loc['CommentSub3',:].values,
            'DateTime': equip.loc['DateTime'],
        })

        pressure = depth_ED if names[i] == 'ed' else False

        if pressure:
            df['Pressure'] = equip.loc['Pressure',:].values
        else:
            df['IDDevice'] = equip.loc['IDDevice',:].values

        df_medidas = equip.iloc[equip.index.get_loc('[Data]')+29 : equip.index.get_loc('[END] of [Spectrum]')-75 :]
        df = pd.concat([df, df_medidas.transpose()], axis=1)
        
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')

        result[names[i]] = df
        
        # df.to_csv(f'teste{i}.txt')

    return result
