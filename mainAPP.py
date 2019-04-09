'''
Autor: Rômulo Gabriel Sousa Sá

1- Descriçao do projeto :
    - Cria e armazena cadastros de emprestimos para um usuario a fim.

4 -Modulos que compoe o software:
    - modules.py: Esse modulo fornece todas funções para salvar e ler (os dados da aplicação em arquivo,
     usando a biblioteca Pickle), cadastrar, listar cadastros, buscar por nome, ano e mes + ano(usando dicionario
     e modulo datetime).
    - PySimpleGUI: framework para a parte gráfica do projeto.
    - Telas.telas: módulo contendo as demais telas do programa.
'''

#aqui começa o software ...
from telas import tela_busca, tela_cadastro, tela_atualizacao, tela_escolha_busca, tela_excluir
from modules import get_informacoes, editar_emprestimo, buscar_nome, cadastrar, exlcuir_emprestimo
from PySimpleGUI import Text, InputText, Button, Column, Frame, Listbox, Window, Popup, PopupNoButtons

NOMES = get_informacoes()
coluna_detalhes = [[Text('', key='nome', size=(30, 1), pad=(1,5))],
                   [Text('', key='telefone', size=(30, 1), pad=(1,8))],
                   [Text('', key='celular', size=(30, 1), pad=(1,8))],
                   [Text('', key='email', size=(30, 1), pad=(1,8))],
                   [Text('', key='vivencia', size=(30, 1), pad=(1,8))],
                   [Text('', key='data', size=(30, 1), pad=(1,8))],
                   [Text('', key='item', size=(30, 1), pad=(1,8))]
                   ]
coluna_btt = [[Button('Editar', key='Editar',pad=(10,0,5), size=(8,1), button_color=('white', 'springgreen4')),
               Button('Apagar', key='Apagar', size=(8,1), button_color=('white', 'firebrick3'))]]
coluna_bt1 = [[Button("Cadastrar",button_color=('white', 'springgreen4'), size=(8,1)),
               Button("Sair", button_color=('white', 'firebrick3'), size=(8,1), pad=(10,0))]]
coluna_nomes = [[Button('Buscar', size=(8,1), pad=(25,1), button_color=('white', 'springgreen4')),
                 Button("", key='botao_busca', visible=False, size=(12,1),  button_color=('white', 'firebrick3'))],
                [Text("", size=(30,2), justification=('center'), key='buscas')],
                [Listbox(values= NOMES, key='lista', change_submits=True, size=(130, 100))]]
tela_principal = [[Frame("Loans-Management", coluna_detalhes), Column(coluna_nomes, size=(130,100))],
                  [Column(coluna_bt1, key='Apag', visible=True)],
                  [Column(coluna_btt, key='Edit', visible=False)]
                  ]
janela = Window("Loans-Management", size=(600, 350), icon=('C:\\Loans-management\\Icon\\icon-logo.ico'), text_justification=('center')).Layout(tela_principal)
while True:
    evento, valores = janela.Read()
    if evento == 'lista':
        try:
            nome = valores['lista'][0]
            emprestimo = buscar_nome(nome)
            nome = "Nome: " + emprestimo['nome']
            telefone = "Telefone: " + emprestimo['telefone']
            celular = "Celular: " + emprestimo['celular']
            email = "E-mail: " + emprestimo['email']
            vivencia = "Vivencia: " + emprestimo['vivencia']
            data = "Data: " + emprestimo['data'].strftime("%d/%m/%Y")
            item = "Item: " + emprestimo['item']
            janela.FindElement('nome').Update(nome)
            janela.FindElement('telefone').Update(telefone)
            janela.FindElement('celular').Update(celular)
            janela.FindElement('data').Update(data)
            janela.FindElement('item').Update(item)
            janela.FindElement('email').Update(email)
            janela.FindElement('vivencia').Update(vivencia)
            janela.FindElement('Edit').Update(visible=True)
            janela.FindElement('Apag').Update(visible=True)
        except IndexError:
            pass
    elif evento == 'Buscar':
        janela.FindElement('nome').Update('')
        janela.FindElement('telefone').Update('')
        janela.FindElement('celular').Update('')
        janela.FindElement('data').Update('')
        janela.FindElement('item').Update('')
        janela.FindElement('email').Update('')
        janela.FindElement('vivencia').Update('')
        janela.FindElement('Edit').Update(visible=False)
        botao_busca = tela_escolha_busca()
        try:
            if botao_busca == "Nome":
                nome_busca = tela_busca(botao_busca)
                if len(nome_busca) != 0:
                    NOMES = get_informacoes(nome=nome_busca)
                    if len(NOMES) != 0:
                        txt_busca = "Buscando por " + nome_busca
                        janela.FindElement('buscas').Update(txt_busca)
                        janela.FindElement('botao_busca').Update(text='Cancelar busca', visible=True)
                        janela.FindElement('lista').Update(NOMES)
                    else:
                        Popup("Nome não encontrado!", button_color=('white', 'springgreen4'))
            elif botao_busca == 'Item':
                item_busca = tela_busca(botao_busca)
                if len(item_busca) != 0:
                    NOMES = get_informacoes(item=item_busca)
                    if len(NOMES) != 0:
                        txt_busca = "Buscando pelo item " + item_busca
                        janela.FindElement('buscas').Update(txt_busca)
                        janela.FindElement('botao_busca').Update(text='Cancelar busca', visible=True)
                        janela.FindElement('lista').Update(NOMES)
                    else:
                        Popup("Item não encontrado!", button_color=('white', 'springgreen4'))
            elif botao_busca == 'Ano':
                ano_busca = tela_busca(botao_busca)
                if type(ano_busca) != str:
                    NOMES = get_informacoes(ano=ano_busca)
                    if len(NOMES) != 0:
                        txt_busca = "Buscando pelo ano " + str(ano_busca)
                        janela.FindElement('buscas').Update(txt_busca)
                        janela.FindElement('botao_busca').Update(text='Cancelar busca', visible=True)
                        janela.FindElement('lista').Update(NOMES)
                    else:
                        Popup("Ano não encontrado!", button_color=('white', 'springgreen4'))
            elif botao_busca == 'Mes + Ano':
                ano_mes_busca = tela_busca(botao_busca)
                if type(ano_mes_busca) != str:
                    mes = ano_mes_busca.month
                    ano = ano_mes_busca.year
                    NOMES = get_informacoes(ano = ano, mes= mes)
                    if len(NOMES) != 0:
                        txt_busca = "Buscando pelo mes " + str(mes) + " e ano " + str(ano)
                        janela.FindElement('buscas').Update(txt_busca)
                        janela.FindElement('botao_busca').Update(text='Cancelar busca', visible=True)
                        janela.FindElement('lista').Update(NOMES)
                    else:
                        Popup("Mes + Ano não encontrado!", button_color=('white', 'springgreen4'))
        except TypeError:
            janela.FindElement('buscas').Update('')
            janela.FindElement('botao_busca').Update(visible=False)
            pass
    elif evento == 'botao_busca':
        NOMES = get_informacoes()
        janela.FindElement('buscas').Update('')
        janela.FindElement('botao_busca').Update(visible=False)
        janela.FindElement('lista').Update(NOMES)
        janela.FindElement('nome').Update('')
        janela.FindElement('telefone').Update('')
        janela.FindElement('celular').Update('')
        janela.FindElement('data').Update('')
        janela.FindElement('item').Update('')
        janela.FindElement('email').Update('')
        janela.FindElement('vivencia').Update('')
        janela.FindElement('Edit').Update(visible=False)

    elif evento == 'Cadastrar':
        cadastro = tela_cadastro()
        if type(cadastro) == list:
            cadastrar(cadastro)
            NOMES = get_informacoes()
            janela.FindElement('lista').Update(NOMES)

    elif evento == 'Editar':
        try:
            emprestimo = buscar_nome(valores['lista'][0])
            novos_dados = tela_atualizacao(emprestimo)
            atualizacao = editar_emprestimo(valores['lista'][0], novos_dados)
            NOMES = get_informacoes()
            janela.FindElement('lista').Update(NOMES)
        except IndexError:
            pass
    elif evento == 'Apagar':
        try:
            confirmar = tela_excluir()
            if confirmar:
                exlcuir_emprestimo(valores['lista'][0])
                NOMES = get_informacoes()
                janela.FindElement('Edit').Update(visible=False)
                janela.FindElement('lista').Update(NOMES)
                janela.FindElement('nome').Update('')
                janela.FindElement('telefone').Update('')
                janela.FindElement('celular').Update('')
                janela.FindElement('data').Update('')
                janela.FindElement('item').Update('')
                janela.FindElement('email').Update('')
                janela.FindElement('vivencia').Update('')
        except IndexError:
            pass

    elif evento is None or evento == 'Sair':
        janela.Close()
        break
PopupNoButtons("Obrigado por usar nosso sistemas!!!", auto_close=True, auto_close_duration=1)