menu = '''

   DIGITE UMA DAS OPÇÕES ABAIXO

============== MENU ==============
    [1] DEPOSITAR
    [2] SACAR
    [3] EXTRATO
    [4] CADASTRAR CLIENTE
    [5] LISTAR CLIENTES
    [6] CRIAR CONTA PARA CLIENTE
    [7] SAIR
==================================
'''

saldo = 0
limite = 500
usuarios = {}
contas_cadastradas = []
contas_sistema = 0
Extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3


def saque (Saldo, extrato, limite, LIMITE_SAQUES, numero_saques): # sugestão DIO
    global saldo
    global Extrato
    print('Saque')
    valor_sacado = int(input('Informe o valor que deseja sacar: '))
    if Saldo == 0:
        print('Você não tem valor valor em conta, faça um depósito')
    elif valor_sacado > Saldo:
        print('O valor que você deseja sacar é maior do que o que você tem em conta')
    elif limite == 0:
        print('Você excedeu seu limite de saque diário')
    elif valor_sacado > limite:
        print('Esse valor é maior que seu limite permitido para saque')
    elif valor_sacado < 0:
        print('O valor informado é negativo')
    elif numero_saques >= LIMITE_SAQUES:
        print('Sua quantidade de saques diária foi atingida')
    else:
        limite -= valor_sacado
        numero_saques += 1
        Saldo -= valor_sacado
        print(f'O seu saque de {valor_sacado} foi efetuado com sucesso')
        extrato += f"Valor sacado {valor_sacado} \n"
        Extrato = extrato
        saldo = Saldo
    return Saldo, extrato, valor_sacado

def deposito (Saldo, extrato): #sugestão DIO
    global saldo
    global Extrato
    print('Depósito')
    valor_depositado = int(input('Insira o valor do depósito: '))
    if valor_depositado > 0:
        Saldo += valor_depositado
        print(f'Seu depósito de {valor_depositado} foi efetuado com sucesso')
        extrato += f"Valor depositado {valor_depositado} \n"
        saldo = Saldo
        Extrato = extrato
    return Saldo, extrato, valor_depositado

def extrato (saldo, extrato=Extrato): #sugestão DIO
    print("============== EXTRATO ==============")
    print("Não foram realizadas movimentações" if not Extrato else Extrato)
    print(f"\n Seu saldo atual é R${saldo:.2f}")
    print("=====================================")
    return extrato

def criar_usuario ():
    global usuarios
    informacoes_usuario = []

    cpf = input('Insira o CPF do cliente: ')
    informacoes_usuario.append(cpf)

    if cpf in usuarios:
        print('usuario já cadastrado')
#    if any(cpf in dados for dados in usuarios.values()):
#        print('Esse usuário já está cadastrado')

    nome = input('Insira o nome completo do cliente: ')
    informacoes_usuario.append(nome)

    data_nascimento = input('Insira a data de nascimento do cliente no formato dd/mm/aaaa: ')
    informacoes_usuario.append(data_nascimento)

    endereco = input('Insira o endereço do cliente no formato (logradouro, bairro - cidade/sigla estado): ')
    informacoes_usuario.append(endereco)

    usuarios[cpf] = informacoes_usuario

    print(f'Usuário cadastrado com sucesso: {informacoes_usuario}')
    informacoes_usuario.clear
    return usuarios

def criar_conta(agencia="0001"):
    global contas_cadastradas
    global usuarios
    global contas_sistema

    informacoes_conta = []

    Agencia = agencia
    informacoes_conta.append(Agencia)

    usuario = input("Digite o CPF do usuário: ")
    if usuario not in usuarios:
        print("Usuário precisa ser cadastrado no sistema")
        criar_usuario()
    else:
        informacoes_conta.append(usuario)
        contas_sistema += 1
        informacoes_conta.append(contas_sistema)
        print(f"conta criada com sucesso: {informacoes_conta}")
    
    informacoes_conta.clear()

    return contas_cadastradas, contas_sistema


while True:
    opcao = int(input(menu))

    if opcao == 1:
        deposito(saldo, Extrato)
    elif opcao == 2:
        saque(saldo, Extrato, limite, LIMITE_SAQUES, numero_saques)
    elif opcao == 3:
        extrato(saldo)
    elif opcao == 4:
        criar_usuario()
    elif opcao == 5:
        print(usuarios)
    elif opcao == 6:
        criar_conta()
    elif opcao == 7:
        break

    else:
        print('Opção selecionada inválida, escolha uma das opção listadas')