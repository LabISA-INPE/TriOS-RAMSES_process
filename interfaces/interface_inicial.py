from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from tkinter import messagebox
from functions.dados import dados

path_es = ''
path_lw = ''
path_lsky = ''
path_eu = ''
path_ed = ''
path_lu = ''
sensores = 6

def interface_inicial(main_frame, plots_interface):

    def upload_file(file_arq):
        global path_es  # Declara path_arquivo como uma variável global
        global path_lw
        global path_lsky
        global path_eu
        global path_ed
        global path_lu
        
        try:
            if file_arq == "es":
                filename = filedialog.askopenfilename()
                filename_text_es["text"] = filename.split('/')[-1]
                path_es = filename  # Atribui o valor a path_arquivo
                print(path_es)
            elif file_arq == "lw":
                filename = filedialog.askopenfilename()
                filename_text_lw["text"] = filename.split('/')[-1]
                path_lw = filename  # Atribui o valor a path_arquivo
                print(path_lw)
            elif file_arq == "lsky":
                filename = filedialog.askopenfilename()
                filename_text_lsky["text"] = filename.split('/')[-1]
                path_lsky = filename  # Atribui o valor a path_arquivo
                print(path_lsky)
            elif file_arq == "eu":
                filename = filedialog.askopenfilename()
                filename_text_eu["text"] = filename.split('/')[-1]
                path_eu = filename  # Atribui o valor a path_arquivo
                print(path_eu)
            elif file_arq == "ed":
                filename = filedialog.askopenfilename()
                filename_text_ed["text"] = filename.split('/')[-1]
                path_ed = filename  # Atribui o valor a path_arquivo
                print(path_ed)
            else:
                filename = filedialog.askopenfilename()
                filename_text_lu["text"] = filename.split('/')[-1]
                path_lu = filename  # Atribui o valor a path_arquivo
                print(path_lu)
        except FileNotFoundError:
            print("Arquivo não encontrado")

    def mostrar_selecao():
        global sensores
        sensores = int(var.get())

        print(sensores)

    def start_calculate():
        if not path_es or not path_lw or not path_lsky:
            messagebox.showerror(title='Erro', message="Por favor, selecione os arquivos 'es', 'lw' e 'lsky' antes de iniciar a rotina.")
            return
        
        if sensores == 6 :
            if not path_es or not path_lw or not path_lsky or not path_eu or not path_ed or not path_lu:
                messagebox.showerror(title='Erro', message="Por favor, selecione os arquivos 'es', 'lw', 'lsky', 'eu', 'ed' e 'lu' antes de iniciar a rotina.")
                return

        dados(
            path_es=path_es,
            path_lw=path_lw,
            path_lsky=path_lsky,
            path_eu=path_eu,
            path_ed=path_ed,
            path_lu=path_lu,
            sensores=sensores,
        )
        plots_interface.tkraise()

    def atualizar_estado_botoes():
        if var.get() == "3":
            path_arquivo_ed.config(state=DISABLED)
            path_arquivo_eu.config(state=DISABLED)
            path_arquivo_lu.config(state=DISABLED)
        else:
            path_arquivo_ed.config(state=NORMAL)
            path_arquivo_eu.config(state=NORMAL)
            path_arquivo_lu.config(state=NORMAL)

    style = Style()

    style.configure('TButton', font = ('calibri', 20, 'bold'), borderwidth = '4')
    style.configure("TFrame", padding=(12, 12))
    style.configure("TLabel", padding=(20, 0))
    style.configure("TLabe2.TButton", font=('Arial', 11))
    style.configure("TButton.TButton", font=('Arial', 13), width=22)
    style.configure("TLabe3.TButton", font=('Arial', 11), width=22)
    style.configure("TEntry", padding=(5, 0))
    first_container = Frame(main_frame, style="TFrame")
    first_container.pack()

    second_container = Frame(main_frame, style="TFrame")
    second_container.pack()

    third_container = Frame(main_frame, style="TFrame")
    third_container.pack()

    fourth_container = Frame(main_frame, style="TFrame")
    fourth_container.pack()

    fifth_container = Frame(main_frame, style="TFrame")
    fifth_container.pack()

    sixth_container = Frame(main_frame, style="TFrame")
    sixth_container.pack()

    seventh_container = Frame(main_frame, style="TFrame")
    seventh_container.pack()

    eight_container = Frame(main_frame, style="TFrame")
    eight_container.pack()
    
    column_names = Label(first_container, text="Rotina para Análise de RRS KD", font=("Arial", "18"), style=("TLabel"))
    column_names.pack(pady=20)

    column_names = Label(second_container, text="Selecione os arquivos de entrada:", font=("Arial", "13"), style=("TLabel"))
    column_names.pack(pady=20)

   # Botão para selecionar um arquivo para análise
    path_arquivo = Button(third_container, text="Arquivo es", style="TLabe2.TButton", command=lambda: upload_file("es"))
    path_arquivo.grid(row=0, column=0, padx=30)

    # Label para exibir o nome do arquivo selecionado
    filename_text_es = Label(third_container, text='', font=("Arial", "11"))
    filename_text_es.grid(row=1, column=0)

    path_arquivo_ed = Button(third_container, text="Arquivo ed", style="TLabe2.TButton", command=lambda: upload_file("ed"))
    path_arquivo_ed.grid(row=0, column=1, padx=30)

    # Label para exibir o nome do arquivo selecionado
    filename_text_ed = Label(third_container, text='', font=("Arial", "11"))
    filename_text_ed.grid(row=1, column=1)

    # Botão para selecionar um arquivo para análise
    path_arquivo = Button(fourth_container, text="Arquivo lsky", style="TLabe2.TButton", command=lambda: upload_file("lsky"))
    path_arquivo.grid(row=0, column=0, padx=30)

    # Label para exibir o nome do arquivo selecionado
    filename_text_lsky = Label(fourth_container, text='', font=("Arial", "11"))
    filename_text_lsky.grid(row=1, column=0)

    # Botão para selecionar um arquivo para análise
    path_arquivo_eu = Button(fourth_container, text="Arquivo eu", style="TLabe2.TButton", command=lambda: upload_file("eu"))
    path_arquivo_eu.grid(row=0, column=1, padx=30)

    # Label para exibir o nome do arquivo selecionado
    filename_text_eu = Label(fourth_container, text='', font=("Arial", "11"))
    filename_text_eu.grid(row=1, column=1)

    # Botão para selecionar um arquivo para análise
    path_arquivo = Button(fifth_container, text="Arquivo lw", style="TLabe2.TButton", command=lambda: upload_file("lw"))
    path_arquivo.grid(row=0, column=0, padx=30)

    # Label para exibir o nome do arquivo selecionado
    filename_text_lw = Label(fifth_container, text='', font=("Arial", "11"))
    filename_text_lw.grid(row=1, column=0)

    # Botão para selecionar um arquivo para análise
    path_arquivo_lu = Button(fifth_container, text="Arquivo lu", style="TLabe2.TButton", command=lambda: upload_file("lu"))
    path_arquivo_lu.grid(row=0, column=1, padx=30)

    # Label para exibir o nome do arquivo selecionado
    filename_text_lu = Label(fifth_container, text='', font=("Arial", "11"))
    filename_text_lu.grid(row=1, column=1)

    var = StringVar(value="6")

    column_names = Label(sixth_container, text="Selecione o número de sensores:", font=("Arial", "11"), style=("TLabel"))
    column_names.pack(side=LEFT)

    # Criar botões de opção
    opcao1 = Radiobutton(sixth_container, text="03", variable=var, value=3, command=atualizar_estado_botoes)
    opcao2 = Radiobutton(sixth_container, text="06", variable=var, value=6, command=atualizar_estado_botoes)

    # Posicionar os botões lado a lado usando pack
    opcao1.pack(side=LEFT)
    opcao2.pack(side=LEFT)

    # Criar uma label para exibir o resultado da seleção
    label_resultado = Label(sixth_container, text="")
    label_resultado.pack(pady=30)

    # Configurar a função de callback
    var.trace_add("write", lambda *args: mostrar_selecao())

    save_button = Button(eight_container, text="Iniciar rotina", style="TButton.TButton", command=start_calculate)
    save_button.pack(pady=20)