menu = '''

   DIGITE UMA DAS OPÇÕES ABAIXO

============== MENU ==============
    [1] DEPOSITAR
    [2] SACAR
    [3] EXTRATO
    [4] SAIR
==================================
'''

saldo = 0
limite = 500
Extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = int(input(menu))

    if opcao == 1:
        print('Depósito')
        valor_depositado = int(input('Insira o valor do depósito: '))
        saldo += valor_depositado
        print(f'Seu depósito de {valor_depositado} foi efetuado com sucesso')

    elif opcao == 2:
        print('Saque')
        valor_sacado = int(input('Informe o valor que deseja sacar: '))
        if saldo == 0:
            print('Você não tem valor valor em conta, faça um depósito')
        elif valor_sacado > saldo:
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
            Extrato.append(valor_sacado)
            print(f'O seu saque de {valor_sacado} foi efetuado com sucesso')
        

    elif opcao == 3:
        print("Extrato")
        for i in Extrato:
            print(f'Valor sacado {i}')

    elif opcao == 4:
        break

    else:
        print('Opção selecionada inválida, escolha uma das opção listadas')