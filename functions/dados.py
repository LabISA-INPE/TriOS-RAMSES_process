def dados(path_es, path_lw, path_lsky, path_eu, path_ed, path_lu, sensores):
    with open("input.txt", "w") as arquivo:
        arquivo.write(f"path_es={path_es}\n")
        arquivo.write(f"path_lw={path_lw}\n")
        arquivo.write(f"path_lsky={path_lsky}\n")
        arquivo.write(f"path_eu={path_eu}\n")
        arquivo.write(f"path_ed={path_ed}\n")
        arquivo.write(f"path_lu={path_lu}\n")
        arquivo.write(f"sensores={sensores}\n")
        arquivo.write(f"nome_pontos=\n")

    print("As variáveis foram salvas no arquivo input.txt.")