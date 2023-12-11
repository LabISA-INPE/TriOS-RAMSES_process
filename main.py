# Importações
from tkinter import *
from interfaces.interface_inicial import interface_inicial
from interfaces.interface_nomes import interface_nomes
from interfaces.interface_graficos import interface_graficos

# Função principal para inicializar a interface
def start():

    # Criando a interface com tkinter
    root = Tk()
    
    # Adicionando título da janela
    root.title("Rotina RRS")
    # Definindo o tamanho da janela
    root.geometry("1000x580")

    # Definindo os Frames (telas)
    initial = Frame(root)
    plots = Frame(root)
    names = Frame(root)

    # Percorrendo cada um desses frames. Cada frame é posicionado na mesma localização, mas apenas um frame é visível de cada vez. Isso permite alternar entre diferentes telas ou seções da interface, ocultando e exibindo os frames conforme necessário.
    for frame in (initial, plots, names):
        frame.grid(row=0, column=0, sticky="nsew")

    # Buscando as interfaces
    interface_inicial(initial, names)
    interface_nomes(names, plots)
    interface_graficos(plots, initial)

    # O frame inicialmente visível quando a aplicação é iniciada. Outros frames são ocultados. Isso permite que a aplicação comece na tela inicial.
    initial.tkraise()

    # Iniciar o loop (mantendo a janela aberta) da interface gráfica.
    root.mainloop()

# Inciando a função principal
start()