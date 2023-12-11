# Rotina RRS e KD em Python

Rotina em Python convertida da rotina em R para pré-processamento e cálculo dos dados de rrs.

## Instalação e execução

Para executar o código é necessário instalar as seguintes tecnologias:

* [Python](https://www.python.org/downloads/)
* [Anaconda](https://www.anaconda.com/download) (Opcional)

Clone o repositório com o comando:

```console
git clone https://github.com/LabISA-INPE/rotina-rrs-kd-python.git
```

Caso esteja utilizando Anaconda:

Abra o Anaconda Prompt e entre na pasta do projeto:

```console
cd path/rotina-rrs-kd-python
```

Crie um ambiente e instale as bibliotecas necessários no arquivo de ambiente:

```console
conda env create --name rrs_kd --file environment.yml
```

Após isso, ative o ambiente:

```console
conda activate rrs_kd
```

Caso opte por instalar pelo pip, é possível instalar as biliotecas com este comando:

```console
pip install -r requirements.txt
```

Execute o código em Python:

```console
python main.py
```

Caso queira testar o código, há um diretório chamado example com o arquivos com dados de entrada (es, lw, lsky, eu, ed, lu) para fazer a sua execução.

## Tela inicial

Inicialmente, temos a tela inicial que possui botões para a entrada dos 6 arquivos de dados indicando seu caminho no diretório. Além disso, possui a opção para 3 ou 6 sensores. Por fim, o código será executado ao clicar no botão "Iniciar rotina".

## Renomeando os nomes dos pontos

Nesta tela, ao clicar em "Buscar nome dos pontos", será buscado os nomes dos pontos nos arquivos de entrada e será exibido os nomes de Comment, CommentSub1, CommentSub2 e CommentSub3 dos arquivos de entrada. Desse modo, é possível renomear os nomes dos pontos a partir de uma dessas opções. Também é possível selecionar mais de uma opção para juntar os nomes desses pontos e será exibido em nomes finais o resultado dessa junção. Após isso, o usuário clicará em "Salvar nomes e continuar" que abrirá uma janela para indicar o caminho que deseja salvar os dados com o nome dos pontos renomeados em um arquivo pickle (.pkl) e também já será salvo os dados mesclados pela data e interpolados.

## Gráficos para avaliação de rrs

Após isso, ao clicar no botão "Iniciar Avaliação", será aberto uma janela para selecionar o arquivo salvo anteriormente. Após isso, será calulado o rrs com o valor padrão de rho (0,028). Assim, será exibido os gráficos de cada ponto com suas medidas, que possibilitará o usuário avaliá-los para manter apenas as medidas relevantes. Para isso, nessa parte do processo, é possivel, caso necessário, alterar o nome do ponto, calcular o rrs novamente com um valor de rho específico, calcular os valores dos quartis ou exibir os valores originais e excluir as medidas inválidas indicando o número no final da linha que deseja excluir. Assim que um ponto estiver tudo corretamente calculado, ao clicar em próximo gráfico será exibido o próximo ponto. Após todos os pontos serem avaliados, será exibido os gráficos de cada ponto com os valores da medida em vermelho e a mediana deles em preto e será habilitado o botão de salvar. O botão de salvar abrirá uma janela na qual o usuário poderá selecionar o diretório que deseja salvar os resultados, incluindo os dados de cada sensor interpolados nos comprimentos de onda de 400 a 900 nm, o arquivo com o valor de rrs e a mediana e o desvio padrão do rrs de cada ponto, além de também salvar o gráfico final.

## Ainda pendente

Em python, a função que faz a interpolação linear dos dados é a função interp1d da biblioteca scipy que está funcionando para os valores que estão dentro do intervalo de 400 a 900 nm. Entretanto, para dados fora deste intervalo, que são preenchidos com o parâmetro fill_value='extrapolate', os dados retornandos em R não são os mesmos. Assim, este ajuste está em pendência por enquanto.

Segue abaixo o código que está fazendo esta interpolação para melhor entendimento:

```console 
    for i in range(df.shape[1]):
        df.iloc[:,i] = pd.to_numeric(df.iloc[:,i], errors='coerce')

        if not pd.isna(df.iloc[0,i]):
            interp_func = interp1d(wavelengths, df.iloc[:,i], kind='linear', fill_value='extrapolate', bounds_error=False)
            normalizado.iloc[:,i+1] = interp_func(range(400,901))

```
