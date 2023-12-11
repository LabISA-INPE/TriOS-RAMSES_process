from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import pickle
import pandas as pd
from functions.merge_and_get_points import merge_and_get_points
from functions.read_input import read_input
from functions.rename_points import rename_points_sensor_6, rename_points_sensor_3

results = {}
sensores = ''
names = []
names1 = []
names2 = []
names3 = []

def interface_nomes(main_frame, plots_interface):

    def get_points():
        global results, sensores, names, names1, names2, names3

        start_button['state'] = DISABLED

        try:
            path_es, path_lw, path_lsky, path_eu, path_ed, path_lu, sensores, nome_pontos = read_input()
            names, names1, names2, names3, results = merge_and_get_points(es=path_es, lw=path_lw, lsky=path_lsky, eu=path_eu, ed=path_ed, lu=path_lu, depth_ED=True, quant_sensors=sensores)
        except:
            messagebox.showerror(title='Erro', message="Formatação irregular de algum arquivo de entrada")

        if len(names.dropna()) > 0:
            names_comment['state'] = NORMAL
            check_comment['state'] = NORMAL
            for n, i in enumerate(names.fillna('').unique()):
                names_comment.insert(n, i)

        if len(names1.dropna()) > 0:
            names_comment1['state'] = NORMAL
            check_comment1['state'] = NORMAL
            for n, i in enumerate(names1.fillna('').unique()):
                names_comment1.insert(n, i)

        if len(names2.dropna()) > 0:
            names_comment2['state'] = NORMAL
            check_comment2['state'] = NORMAL
            for n, i in enumerate(names2.fillna('').unique()):
                names_comment2.insert(n, i)

        if len(names3.dropna()) > 0:
            names_comment3['state'] = NORMAL
            check_comment3['state'] = NORMAL
            for n, i in enumerate(names3.fillna('').unique()):
                names_comment3.insert(n, i)

        var_comment.set(1)
        var_comment1.set(1)

        update_names()

        save_button['state'] = NORMAL

    def update_names():
        global names, names1, names2, names3

        names_final.delete(0,END)

        names_concat = pd.DataFrame()

        if var_comment.get():
            if names_concat.empty:
                names_concat = names.fillna('')
            else:
                names_concat += '_' + names.fillna('')
        if var_comment1.get():
            if names_concat.empty:
                names_concat = names1.fillna('')
            else:
                names_concat += '_' + names1.fillna('')
        if var_comment2.get():
            if names_concat.empty:
                names_concat = names2.fillna('')
            else:
                names_concat += '_' + names2.fillna('')
        if var_comment3.get():
            if names_concat.empty:
                names_concat = names3.fillna('')
            else:
                names_concat += '_' + names3.fillna('')

        if not names_concat.empty:
            for n, i in enumerate(names_concat.unique()):
                names_final.insert(n, i)
            
    def save_names():
        global results, sensores

        if len(names_final.get(0, END)) > 0:
            try:
                if sensores == 6:
                    renamed_results = rename_points_sensor_6(new_name=names_final.get(0, END), lw_=results['lw'], lsky_=results['lsky'], es_=results['es'], ed_=results['ed'], eu_=results['eu'], lu_=results['lu'], quant_sensors=sensores)
                else:
                    renamed_results = rename_points_sensor_3(new_name=names_final.get(0, END), lw_=results['lw'], lsky_=results['lsky'], es_=results['es'], quant_sensors=sensores)

                file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl")])
            except:
                messagebox.showerror(title='Erro', message="Ocorreu um erro na renomeação dos pontos")


            if file_path:
                with open(file_path, 'wb') as arquivo:
                    pickle.dump(renamed_results, arquivo)
            
                messagebox.showinfo(title="Sucesso", message="Arquivo salvo com sucesso!")

                start_button['state'] = NORMAL
                names_comment.delete(0,END)
                names_comment['state'] = DISABLED
                check_comment['state'] = DISABLED
                var_comment.set(0)
                names_comment1.delete(0,END)
                names_comment1['state'] = DISABLED
                check_comment1['state'] = DISABLED
                var_comment1.set(0)
                names_comment2.delete(0,END)
                check_comment2['state'] = DISABLED
                names_comment2['state'] = DISABLED
                var_comment2.set(0)
                names_comment3.delete(0,END)
                check_comment3['state'] = DISABLED
                names_comment3['state'] = DISABLED
                var_comment3.set(0)
                names_final.delete(0,END)

                plots_interface.tkraise()

        else:
            messagebox.showerror(title="Erro", message="Selecione pelo menos um campo de nomes")

    style = Style()

    style.configure('TButton', font=('Arial', 13), width=22)
    style.configure("Title.TLabel", font=("Arial", 20))
    style.configure("TLabel", font=('Arial', 13))
    style.configure("TCheckbutton", font=('Arial', 11))

    first_container = Frame(main_frame, padding=(10, 10))
    first_container.pack()

    second_container = Frame(main_frame, padding=(0, 10))
    second_container.pack()

    third_container = Frame(main_frame, padding=(0, 10))
    third_container.pack()

    tfirst_container = Frame(third_container, padding=(10, 0))
    tfirst_container.pack(side=LEFT)

    tsecond_container = Frame(third_container, padding=(10, 0))
    tsecond_container.pack(side=LEFT)

    tthird_container = Frame(third_container, padding=(10, 0))
    tthird_container.pack(side=LEFT)

    tfourth_container = Frame(third_container, padding=(15, 0))
    tfourth_container.pack(side=LEFT)

    tfifth_container = Frame(third_container, padding=(10, 0))
    tfifth_container.pack(side=LEFT)

    fourth_container = Frame(main_frame, padding=(0, 20))
    fourth_container.pack()

    title = Label(first_container, text="Nomeação dos pontos", style=("Title.TLabel"))
    title.pack()

    start_button = Button(second_container, text="Buscar nomes dos pontos" , style="TButton", command=get_points)
    start_button.pack(pady=10)

    main_text = Label(second_container, text="Selecione os nomes:", style=("TLabel"))
    main_text.pack(pady=10)

    var_comment = IntVar()
    var_comment.set(0)
    check_comment = Checkbutton(tfirst_container, text = "CommentSub", variable = var_comment, onvalue = 1, offvalue = 0,  state = DISABLED, style=("TCheckbutton"), command=update_names)
    check_comment.pack()

    names_comment = Listbox(tfirst_container, width=18, height=15, font=('Arial', 11))
    names_comment.pack()

    var_comment1 = IntVar()
    var_comment1.set(0)
    check_comment1 = Checkbutton(tsecond_container, text = "CommentSub1", variable = var_comment1, onvalue = 1, offvalue = 0, state = DISABLED, style=("TCheckbutton"), command=update_names)
    check_comment1.pack()

    names_comment1 = Listbox(tsecond_container, width=17, height=15, font=('Arial', 11))
    names_comment1.pack()

    var_comment2 = IntVar()
    var_comment2.set(0)
    check_comment2 = Checkbutton(tthird_container, text = "CommentSub2", variable = var_comment2, onvalue = 1, offvalue = 0, state = DISABLED, style=("TCheckbutton"), command=update_names)
    check_comment2.pack()

    names_comment2 = Listbox(tthird_container, width=17, height=15, font=('Arial', 11))
    names_comment2.pack()

    var_comment3 = IntVar()
    var_comment3.set(0)
    check_comment3 = Checkbutton(tfourth_container, text = "CommentSub3", variable = var_comment3, onvalue = 1, offvalue = 0,  state = DISABLED, style=("TCheckbutton"), command=update_names)
    check_comment3.pack()

    names_comment3 = Listbox(tfourth_container, width=17, height=15, font=('Arial', 11))
    names_comment3.pack()
    
    names_text = Label(tfifth_container, text="Nomes atuais:", style=("TLabel"))
    names_text.pack()

    names_final = Listbox(tfifth_container, width=34, height=15, font=('Arial', 11))
    names_final.pack()

    save_button = Button(fourth_container, text="Salvar nomes e continuar", state=DISABLED, style="TButton", command=save_names)
    save_button.pack()