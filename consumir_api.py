import requests
import json
import PySimpleGUI as sg, sys

# Função que faz o request e retorna os valores desejados
def buscar_dados(cidade, unidade): 
    if unidade == 'Celsius': # se a unidade selecionada for "Celsius", adiciona o valor "&units=metric" ao request
        request = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid=3ad92087b8a46499d0838a9985eb368b&units=metric".format(cidade))
    else: # unidade padrão da API é Kelvin
        request = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid=3ad92087b8a46499d0838a9985eb368b".format(cidade))
    print(json.loads(request.content)) # mostrando os valores no terminal
    return(json.loads(request.content))

def gerar_janela(valores, graus): #função que cria a janela com os valores contidos no json
    tamanho = [15,1] # identação dos campos
    tela2 = [
        [sg.T("")],
        [sg.Text("Escolha uma Cidade:"), sg.Input('', size=[15,1], key='_cidade_'),
        sg.Text("", size=[1,1]),
        sg.Text("Graus:"),
        sg.Combo(['Celsius', 'Kelvin'], default_value='Celsius', key='_unidade_'),
        sg.Text("", size=[2,1]),
        sg.Button(button_text='Buscar')],
        [sg.T("")],
        [sg.Text("Resultados da busca por:"), sg.Text(valores['name'], font=('Arial', 10,'bold'))],
        [sg.Text("Temperatura mínima:", size=(tamanho)), sg.Text("{} {}".format(valores['main']['temp_min'], graus)), sg.Text("e máxima:"), sg.Text("{} {}".format(valores['main']['temp_max'], graus))],
        [sg.Text("Sensação térmica:", size=(tamanho)), sg.Text("{} {}".format(valores['main']['feels_like'], graus))],
        [sg.Text("Temperatura atual:", size=(tamanho)), sg.Text("{} {}".format(valores['main']['temp'], graus))],
        [sg.Text("Humidade do ar:", size=(tamanho)), sg.Text("{}%".format(valores['main']['humidity']))],
        [sg.T("")],
    ]
    window2 = sg.Window('Consumindo uma API com Python', icon='a.ico').Layout(tela2)
    return(window2) # função retorna o layout com as informações para ser renderizada

# tema que sera aplicado a todas as janelas
sg.LOOK_AND_FEEL_TABLE['tema'] = {'BACKGROUND': '#dee2e6', 'TEXT': '#343a40', 'INPUT': '#f8f9fa',
                      'SCROLL': '#E7C855', 'TEXT_INPUT': '#343a40', 'BUTTON': ('#f8f9fa', '#495057'),
                      'PROGRESS': "#282923", 'SCROLL': '#282923', 'BORDER': 1,'SLIDER_DEPTH':0, 'PROGRESS_DEPTH':0}

sg.ChangeLookAndFeel('tema')

telaInicial = [
    [sg.T("")],
    [sg.Text("Escolha uma Cidade:"), sg.Input('', size=[15,1], key='_cidade_'),
    sg.Text("", size=[1,1]),
    sg.Text("Graus:"),
    sg.Combo(['Celsius', 'Kelvin'], default_value='Celsius', key='_unidade_'),
    sg.Text("", size=[2,1]),
    sg.Button(button_text='Buscar')],
    [sg.T("")],
]

tela3 = [
    [sg.T("")],
    [sg.Text("Escolha uma Cidade:"), sg.Input('', size=[15,1], key='_cidade_'),
    sg.Text("", size=[1,1]),
    sg.Text("Graus:"),
    sg.Combo(['Celsius', 'Kelvin'], default_value='Celsius', key='_unidade_'),
    sg.Text("", size=[2,1]),
    sg.Button(button_text='Buscar')],
    [sg.T("")],
    [sg.Text("Cidade não encontrada!")],
    [sg.T("")],
]

window1 = sg.Window('Consumindo uma API com Python', icon='a.ico').Layout(telaInicial)
window3 = sg.Window('Consumindo uma API com Python', icon='a.ico').Layout(tela3)

unidade = ''
janela1 = True
janela2 = False
janela3 = False
event, values = window1.Read() # renderizando a primeira janela
while True:
    if event == sg.WIN_CLOSED or event == 'Cancelar': # Se usuário clicar no X ou em cancelar:
        sys.exit()

    if event == 'Buscar': # ao clicar no botão de busca
        valores = buscar_dados(values['_cidade_'], values['_unidade_']) # chamando a função que fará o request
        if values['_unidade_'] == 'Celsius':
            unidade = '°C'
        else:
            unidade = '°K'

        if valores['cod'] == '404': # no caso da cidade digitada não ser encontrada:
            if janela1 == True: 
                janela1 = False
                window1.hide()
            if janela2 == True: 
                janela2 = False
                window2.hide()
            janela3 = True
            event, values = window3.Read() # renderiza janela 3
            
        else: # caso cidade seja encontrada:
            if janela1 == True: 
                janela1 = False
                window1.hide()
            if janela3 == True: 
                janela3 = False
                window3.hide()
            if janela2 == True:
                janela2 = False
                window2.hide()
            janela2 = True
            window2 = gerar_janela(valores, unidade) # função que gera o layout da janela 
            event, values = window2.Read() # renderizando a janela 2