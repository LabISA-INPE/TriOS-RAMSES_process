
def read_input():
    with open('input.txt', 'r') as file:
        rows = file.readlines()

    for r in rows:
        key, value = r.strip().split('=')
        if key == 'path_es': path_es = value
        if key == 'path_lw': path_lw = value
        if key == 'path_lsky': path_lsky = value
        if key == 'path_eu': path_eu = value
        if key == 'path_ed': path_ed = value
        if key == 'path_lu': path_lu = value
        if key == 'sensores': sensores = value
        if key == 'nome_pontos': nome_pontos = value

    return path_es, path_lw, path_lsky, path_eu, path_ed, path_lu, int(sensores), nome_pontos

def read_sensores():
        with open('input.txt', 'r') as file:
            rows = file.readlines()

        for r in rows:
            key, value = r.strip().split('=')
            if key == 'sensores': sensores = value

        return int(sensores)
