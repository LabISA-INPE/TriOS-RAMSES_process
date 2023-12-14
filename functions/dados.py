def dados(path_es, path_lw, path_lsky, path_eu, path_ed, path_lu, sensores):
    # Abre o arquivo "input.txt" no modo de escrita ('w')
    with open("input.txt", "w") as arquivo:
        # Escreve cada valor de variável no arquivo, seguido por uma quebra de linha
        arquivo.write(f"path_es={path_es}\n")
        arquivo.write(f"path_lw={path_lw}\n")
        arquivo.write(f"path_lsky={path_lsky}\n")
        arquivo.write(f"path_eu={path_eu}\n")
        arquivo.write(f"path_ed={path_ed}\n")
        arquivo.write(f"path_lu={path_lu}\n")
        arquivo.write(f"sensores={sensores}\n")
        arquivo.write(f"nome_pontos=\n")

    # Imprime uma mensagem indicando que as variáveis foram salvas no arquivo
    print("As variáveis foram salvas no arquivo input.txt.")
