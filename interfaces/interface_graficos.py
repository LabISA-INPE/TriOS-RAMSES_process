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

# Inicialização de variáveis globais
results = {}
pontos = []                 # Lista para armazenar os pontos
plot_widget = {}            # Widget para exibir o gráfico
rrs_filter = pd.DataFrame() # DataFrame para armazenar os resultados do filtro Rrs
rrs_filtered = pd.DataFrame()
rrs_calculated = pd.DataFrame()
cont = 0                    # Contador para pontos
sensores = 0                # Número de sensores
final_plot = {}             # Dicionário para armazenar o gráfico final
percent = False             # Indicador para cálculo de percentil
data = {}                   # Dados obtidos
zoom = False
rho_ = 0.028
delete_var = False

# Função para criar a interface gráfica
def interface_graficos(main_frame, initial_interface):
    def on_close(event):
        global zoom, rho_, delete_var
        zoom = False
        zoom_button['state'] = NORMAL
        if not delete_var:
            calculate_plots(rho_)
        else:
            delete_plots(deletar=False)
        
    # Função interna para exibir o gráfico na interface
    def display_plot(figure):
        global plot_widget, zoom
        if zoom:
            figure.canvas.mpl_connect('close_event', on_close)
            plt.show(block=False)
        else:
            plot_widget = FigureCanvasTkAgg(figure, canvas)
            plot_widget.get_tk_widget().pack()

    def zoom_plot():
        global zoom, rho_, delete_var
        zoom = True
        zoom_button['state'] = DISABLED
        if not delete_var:
            calculate_plots(rho_)
        else:
            delete_plots(deletar=False)

    # Função interna para obter e exibir o gráfico atual
    def get_current_plot():
        global cont, rrs_filter, pontos

        plt.close()

        try:
            # Obtenção dos resultados Rrs
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

    # Função interna para iniciar o processo de obtenção dos plots
    def start_plots(rho):
        global data, sensores, rrs_filter
        

        path = filedialog.askopenfilename(defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl")])

        if path:
            try:
                with open(path, 'rb') as file:
                    data = pickle.load(file)
            except:
                messagebox.showerror(title='Erro', message='Arquivo inválido!')
                return

            # Configuração dos botões e entradas
            start_button['state'] = DISABLED
            aplica_button['state'] = NORMAL
            percentis_button['state'] = NORMAL
            point_name['state'] = NORMAL
            rho_input['state'] = NORMAL
            rho_input.insert(0, '0.028')
            delete_button['state'] = NORMAL
            next_plot_button['state'] = NORMAL
            medidas['state'] = NORMAL
            zoom_button['state'] = NORMAL

            sensores = read_sensores()

            rrs_filter = data

            calculate_plots(rho)

    # Função interna para calcular os plots com base no valor de rho
    def calculate_plots(rho):
        global rrs_filter, pontos, plot_widget, results, sensores, percent, data, rho_, delete_var

        delete_var = False

        # plt.close()

        try:
            rho_ = float(rho)
        except:
            messagebox.showerror(title='Erro', message='Valor inválido. Certifique-se de adicionar um número com decimais separados por ponto e não vírgula.')
            return

        try:
            results = rrs_calculation(data, sensores, rho_)
        except:
            messagebox.showerror(title='Erro', message='Ocorreu um erro ao calcular o rrs! Verifique se o arquivo selecionado no início é realmente válido.')
            return
        if percent:
            get_current_plot_percentil(rho_)
        else:
            get_current_plot()

        delete_button['state'] = NORMAL
        next_plot_button['state'] = NORMAL

    # Função interna para excluir pontos selecionados
    def delete_plots(deletar):
        global rrs_filter, plot_widget, delete_var

        delete_var = True

        points = medidas.get()     
                   
        plt.close()      

        if points and deletar:
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
                messagebox.showerror(title='Erro', message='Não restou nenhuma medida no gráfico.')
                return
            
        if not deletar:
            plot_widget.get_tk_widget().pack_forget()
            try:
                figure = plot(rrs_filter)
                display_plot(figure)
            except:
                plt.close()
                messagebox.showerror(title='Erro', message='Não restou nenhuma medida no gráfico.')
                return
    

    # Função para exibir o gráfico percentil ou os originais
    def get_current_plot_percentil(rho):
        global cont, rrs_filter, pontos, percent

        plt.close()

        rrs = results['rrs']
        pontos = rrs['estacoes_id'].unique()

        if not zoom:
            percent = not percent  # Alternância entre exibição percentil e originais

        if plot_widget:
            plot_widget.get_tk_widget().pack_forget()

        current_point = pontos[cont]
        point_name.delete(0, END)  # Limpa o conteúdo atual do Entry
        point_name.insert(0, current_point)  # Insere o novo valor no Entry
        
        if percent:
            try:
                # Exibição dos dados percentis
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

    # Função para avançar para o próximo gráfico
    def next_plots():
        global cont, rrs_filtered, rrs_filter, pontos, results, rrs_calculated, final_plot, percent, sensores, delete_var
        
        plt.close()

        delete_var = False

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

    # Função para salvar os resultados e voltar à interface inicial
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

    # Criação de containers e elementos da interface
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

    # Rótulo para os gráficos
    column_names = Label(initial_container, text="Gráficos", font=("Arial", "18"), style=("TLabel"))
    column_names.pack(pady=20)

    # Rótulo e botão para iniciar a validação
    label_start = Label(fsecond_container, text="Importe o arquivo anterior:", font=("Arial", "13"))
    label_start.grid()

    start_button = Button(fsecond_container, text="Iniciar validação", style="TButton.TButton", command=lambda:start_plots(0.028))
    start_button.grid()

    # Rótulo e entrada para o nome do ponto
    pontos_name = Label(ssecond_container, text="Nome do ponto:", font=("Arial", "13"), style=("TLabel.TLabel"))
    pontos_name.grid()

    point_name = Entry(ssecond_container, font=("Arial", "11"), width=30, state=DISABLED)
    point_name.insert(0, point_name['text'])
    point_name.grid()

    # Canvas para exibição dos gráficos
    canvas = Canvas(first_container, width=660, height=480, bg='white')
    canvas.pack(anchor=W, expand=True, padx=20)

    zoom_button = Button(first_container, text="Zoom no Gráfico", style="TButton.TButton", command=zoom_plot, state=DISABLED)
    zoom_button.pack()

    # Rótulo, entrada e botão para o valor de rho
    rho_label = Label(fthird_container, text="Valor de rho:", font=("Arial", "13"), style=("TLabel"))
    rho_label.grid()

    rho_input = Entry(fthird_container, font=("Arial", "11"), width=21, state=DISABLED)
    rho_input.grid()

    # Botão para aplicar a análise com o valor de rho inserido
    aplica_button = Button(fthird_container, text="Aplicar", style="TLabe2.TButton", state=DISABLED, command=lambda: calculate_plots(rho_input.get()))
    aplica_button.grid(pady=5)

    # Botão para alternar entre mostrar os gráficos originais e percentis
    percentis_button = Button(sthird_container, text="Mostrar originais", style="TLabe3.TButton", state=DISABLED, command=lambda: get_current_plot_percentil(rho_input.get()))
    percentis_button.grid()

    # Rótulo e entrada para informar os pontos a serem excluídos
    column_names = Label(fourth_container, text="Entre com os pontos para excluir:", font=("Arial", "13"), style=("TLabel.TLabel"))
    column_names.grid()

    # Entrada para o número de amostras de água
    medidas = Entry(fourth_container, font=("Arial", "11"), width=21, state=DISABLED)
    medidas.grid()

    # Botão para excluir os pontos selecionados
    delete_button = Button(fourth_container, text="Excluir", style="TLabe2.TButton", state=DISABLED, command=lambda:delete_plots(deletar=True))
    delete_button.grid(pady=5)

    # Botão para avançar para o próximo gráfico
    next_plot_button = Button(fifth_container, text="Próximo gráfico", style="TLabe2.TButton", state=DISABLED, command=next_plots)
    next_plot_button.grid(pady=10)

    # Rótulo para selecionar o diretório de salvamento
    column_names = Label(sixth_container, text="Selecione onde salvar os arquivos:", font=("Arial", "13"))
    column_names.pack()

    # Botão para salvar os resultados e voltar à interface inicial
    save_button = Button(sixth_container, text="Salvar", style="TLabe2.TButton", state=DISABLED, command=save_and_finish)
    save_button.pack()
