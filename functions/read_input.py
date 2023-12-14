
def read_input():
    # Abre o arquivo "input.txt" em modo de leitura e lê todas as linhas
    with open('input.txt', 'r') as file:
        rows = file.readlines()

    # Inicializa variáveis
    path_es = path_lw = path_lsky = path_eu = path_ed = path_lu = sensores = nome_pontos = None

    # Itera sobre as linhas do arquivo
    for r in rows:
        # Divide a linha em chave e valor usando '=' como delimitador
        key, value = r.strip().split('=')

        # Atribui os valores correspondentes às variáveis com base na chave
        if key == 'path_es': path_es = value
        if key == 'path_lw': path_lw = value
        if key == 'path_lsky': path_lsky = value
        if key == 'path_eu': path_eu = value
        if key == 'path_ed': path_ed = value
        if key == 'path_lu': path_lu = value
        if key == 'sensores': sensores = value
        if key == 'nome_pontos': nome_pontos = value

    # Converte sensores para um inteiro e retorna as variáveis correspondentes
    return path_es, path_lw, path_lsky, path_eu, path_ed, path_lu, int(sensores), nome_pontos


def read_sensores():
    # Abre o arquivo "input.txt" em modo de leitura e lê todas as linhas
    with open('input.txt', 'r') as file:
        rows = file.readlines()

    # Inicializa a variável sensores
    sensores = None

    # Itera sobre as linhas do arquivo
    for r in rows:
        # Divide a linha em chave e valor usando '=' como delimitador
        key, value = r.strip().split('=')

        # Atribui o valor correspondente à variável sensores com base na chave
        if key == 'sensores': sensores = value

    # Converte sensores para um inteiro e retorna o resultado
    return int(sensores)