from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from tkinter import messagebox
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions.read_input import read_sensores
from functions.rrs_calculation import rrs_calculation
from functions.rrs_filtering import rrs_filtering, plot, rrs_results
from functions.plot_results import plot_results
from functions.save_files import save_files
from functions.rename_points import update_name_points

results = {}
pontos = []
plot_widget = {}
rrs_filter = pd.DataFrame()
rrs_filtered = pd.DataFrame()
rrs_calculated = pd.DataFrame()
cont = 0
sensores = 0
final_plot = {}
percent = False
data = {}

def interface_graficos(main_frame, initial_interface):
    def display_plot(figure):
        global plot_widget

        plot_widget = FigureCanvasTkAgg(figure, canvas)
        plot_widget.get_tk_widget().pack()
        plt.close()

    def get_current_plot():
        global cont, rrs_filter, pontos

        try:
            rrs = results['rrs']
            pontos = rrs['estacoes_id'].unique()
            rrs_filter = rrs_filtering(rrs.loc[rrs['estacoes_id'] == pontos[cont]])
        except:
            messagebox.showerror(title='Erro', message='Houve um erro ao calcular o percentil.')
            return

        if plot_widget:
            plot_widget.get_tk_widget().pack_forget()

        current_point = pontos[cont]
        point_name.delete(0, END)  # Limpa o conteúdo atual do Entry
        point_name.insert(0, current_point)  # Insere o novo valor no Entry

        if not rrs_filter.empty:
            try:
                figure = plot(rrs_filter)
                display_plot(figure)
            except:
                messagebox.showerror(title='Erro', message='Ocorreu um erro ao plotar o gráfico')
                return
        else:
            messagebox.showerror(title='Sem medidas possíveis', message='Nenhum dado foi obtido no ponto "' + pontos[cont] + '"')
            next_plots()

    def start_plots(rho):
        global data, sensores

        path = filedialog.askopenfilename(defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl")])

        if path:
            try:
                with open(path, 'rb') as file:
                    data = pickle.load(file)
            except:
                messagebox.showerror(title='Erro', message='Arquivo inválido!')
                return

            start_button['state'] = DISABLED
            aplica_button['state'] = NORMAL
            percentis_button['state'] = NORMAL
            point_name['state'] = NORMAL
            rho_input['state'] = NORMAL
            rho_input.insert(0, '0.028')
            delete_button['state'] = NORMAL
            next_plot_button['state'] = NORMAL

            medidas['state'] = NORMAL

            sensores = read_sensores()

            calculate_plots(rho)

    def calculate_plots(rho):
        global rrs_filter, pontos, plot_widget, results, sensores, percent, data

        try:
            rho = float(rho)
        except:
            messagebox.showerror(title='Erro', message='Valor inválido. Cerifique-se de adicionar um número com decimais separados por ponto e não vírgula.')
            return

        try:
            results = rrs_calculation(data, sensores, rho)
        except:
            messagebox.showerror(title='Erro', message='Ocorreu um erro ao calcular o rrs! Verifique se o arquivo selecionado no início é realmente válido.')
            return

        if percent:
            get_current_plot_percentil(rho)
        else:
            get_current_plot()

        delete_button['state'] = NORMAL
        next_plot_button['state'] = NORMAL

    def delete_plots():
        global rrs_filter, plot_widget

        points = medidas.get()           

        if points:
            delete = [int(x) for x in points.split(',')]
            try:
                rrs_filter = rrs_filter.drop(rrs_filter.index[delete], axis=0)
                rrs_filter = rrs_filter.reset_index(drop=True)
            except:
                messagebox.showerror(title='Erro', message='Algum ponto indicado é inválido.')
                return

            plot_widget.get_tk_widget().pack_forget()

            try:
                figure = plot(rrs_filter)
                display_plot(figure)
            except:
                plt.close()
                messagebox.showerror(title='Erro', message='Não restou nenhuma medida no gráfico.')
                return

    def get_current_plot_percentil(rho):
        global cont, rrs_filter, pontos, percent

        rrs = results['rrs']
        pontos = rrs['estacoes_id'].unique()

        percent = not percent

        if plot_widget:
            plot_widget.get_tk_widget().pack_forget()

        current_point = pontos[cont]
        point_name.delete(0, END)  # Limpa o conteúdo atual do Entry
        point_name.insert(0, current_point)  # Insere o novo valor no Entry
        
        if percent:
            try:
                rrs_filter = rrs.loc[rrs['estacoes_id'] == pontos[cont]]
                rrs_filter = rrs_filter.reset_index(drop=True)
                figure = plot(rrs_filter)
                display_plot(figure)
            except:
                messagebox.showerror(title='Erro', message='Houve um erro ao retornar os valores originais ou ao plotar o gráfico.')
                return

            percentis_button['text'] = 'Calcular percentis'
        else:
            percentis_button['text'] = 'Mostrar originais'
            calculate_plots(rho)

    def next_plots():
        global cont, rrs_filtered, rrs_filter, pontos, results, rrs_calculated, final_plot, percent, sensores

        try:
            rrs_filter, results = update_name_points(rrs_filter=rrs_filter, results=results, new_name=point_name.get(), old_name=pontos[cont], sensores=sensores)
        except:
            messagebox.showerror(title='Erro', message='Ocorreu um erro ao tentar substituir o nome do ponto!')
            return

        if rrs_filtered.empty:
            rrs_filtered = rrs_filter
        else:
            rrs_filtered = pd.concat([rrs_filtered, rrs_filter])
   
        cont += 1

        if (cont >= len(pontos)):
            try:
                rrs_calculated = rrs_results(results['rrs'], rrs_filtered)
            except:
                messagebox.showerror(title='Erro', message='Ocorreu um erro ao calcular os resultados finais.')
                return

            plot_widget.get_tk_widget().pack_forget()

            medidas.delete(0, END)
            point_name.delete(0, END)
            rho_input.delete(0, END)
            delete_button['state'] = DISABLED
            next_plot_button['state'] = DISABLED
            percentis_button['state'] = DISABLED
            point_name['state'] = DISABLED
            rho_input['state'] = DISABLED
            medidas['state'] = DISABLED
            aplica_button['state'] = DISABLED

            save_button['state'] = NORMAL
            try:
                final_plot = plot_results(results, rrs_calculated)
            except:
                messagebox.showerror(title='Erro', message='Ocorreu um erro ao gerar o gráfico com os resultados.')
                return

        else:
            if percent:
                percent = not percent
                get_current_plot_percentil(rho_input.get())
            else:
                get_current_plot()

    def save_and_finish():
        global results, rrs_calculated, final_plot, sensores, cont, rrs_filtered

        save_path = filedialog.askdirectory()

        if save_path:
            try:
                save_files(save_path, results, rrs_calculated, final_plot, sensores)
            except:
                messagebox.showerror(title='Erro', message='Ocorreu um erro ao salvar os arquivos.')
                return

            messagebox.showinfo(title='Salvo com sucesso', message='Os dados e o gráfico resultante foram salvos com sucesso!')

            initial_interface.tkraise()

            start_button['state'] = NORMAL
            save_button['state'] = DISABLED
            cont = 0
            rrs_filtered = pd.DataFrame()

    initial_container = Frame(main_frame, style="TFrame")
    initial_container.pack()

    first_container = Frame(main_frame, style="TFrame")
    first_container.pack(side=LEFT)

    fsecond_container = Frame(main_frame, style="TFrame")
    fsecond_container.pack(pady=10)

    ssecond_container = Frame(main_frame, style="TFrame")
    ssecond_container.pack(pady=10)

    fthird_container = Frame(main_frame, style="TFrame")
    fthird_container.pack(pady=10)
    
    sthird_container = Frame(main_frame, style="TFrame")
    sthird_container.pack(pady=10)

    fourth_container = Frame(main_frame, style="TFrame")
    fourth_container.pack(pady=10)

    fifth_container = Frame(main_frame, style="TFrame")
    fifth_container.pack()

    sixth_container = Frame(main_frame, style="TFrame")
    sixth_container.pack()

    column_names = Label(initial_container, text="Gráficos", font=("Arial", "18"), style=("TLabel"))
    column_names.pack(pady=20)

    label_start = Label(fsecond_container, text="Importe o arquivo anterior:", font=("Arial", "13"))
    label_start.grid()

    start_button = Button(fsecond_container, text="Iniciar validação", style="TButton.TButton", command=lambda:start_plots(0.028))
    start_button.grid()

    pontos_name = Label(ssecond_container, text="Nome do ponto:", font=("Arial", "13"), style=("TLabel.TLabel"))
    pontos_name.grid()

    point_name = Entry(ssecond_container, font=("Arial", "11"), width=30, state=DISABLED)
    point_name.insert(0, point_name['text'])
    point_name.grid()

    # Quadrado em branco aonde será exibido os gráficos
    canvas = Canvas(first_container, width=660, height=480, bg='white')
    canvas.pack(anchor=W, expand=True, padx=20)

    rho_label = Label(fthird_container, text="Valor de rho:", font=("Arial", "13"), style=("TLabel"))
    rho_label.grid()

    rho_input = Entry(fthird_container, font=("Arial", "11"), width=21, state=DISABLED)
    rho_input.grid()

    aplica_button = Button(fthird_container, text="Aplicar", style="TLabe2.TButton", state=DISABLED, command=lambda:calculate_plots(rho_input.get()))
    aplica_button.grid(pady=5)

    percentis_button = Button(sthird_container, text="Mostrar originais", style="TLabe3.TButton", state=DISABLED, command=lambda: get_current_plot_percentil(rho_input.get()))
    percentis_button.grid()

    column_names = Label(fourth_container, text="Entre com os pontos para excluir:", font=("Arial", "13"), style=("TLabel.TLabel"))
    column_names.grid()

    # Entrada para o número amostras de água
    medidas = Entry(fourth_container, font=("Arial", "11"), width=21, state=DISABLED)
    medidas.grid()

    # Botão para selecionar um arquivo para análise
    delete_button = Button(fourth_container, text="Excluir", style="TLabe2.TButton", state=DISABLED, command=delete_plots)
    delete_button.grid(pady=5)

    # Botão para selecionar um arquivo para análises
    next_plot_button = Button(fifth_container, text="Próximo gráfico", style="TLabe2.TButton", state=DISABLED, command=next_plots)
    next_plot_button.grid(pady=10)

    column_names = Label(sixth_container, text="Selecione onde salvar os arquivos:", font=("Arial", "13"))
    column_names.pack()

    save_button = Button(sixth_container, text="Salvar", style="TLabe2.TButton", state=DISABLED, command=save_and_finish)
    save_button.pack()