class Transacao:
    """Representa uma transação genérica no sistema bancário."""
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        raise NotImplementedError("Método registrar deve ser implementado pelas subclasses.")


class Deposito(Transacao):
    """Transação de depósito."""
    def registrar(self, conta):
        if self.valor <= 0:
            print("Valor inválido para depósito.")
            return False

        conta._saldo += self.valor
        conta.historico.adicionar_transacao(f"Depósito de R${self.valor:.2f}")
        print(f"Depósito de R${self.valor:.2f} realizado com sucesso.")
        return True


class Saque(Transacao):
    """Transação de saque, respeitando limites da conta corrente."""
    def registrar(self, conta):
        if self.valor <= 0:
            print("Valor inválido para saque.")
            return False
        if conta.numero_saques >= conta.limite_saques:
            print("Número máximo de saques diários atingido.")
            return False
        if self.valor > conta._saldo:
            print("Saldo insuficiente para saque.")
            return False
        if self.valor > conta.limite:
            print("Valor excede o limite disponível para saque.")
            return False

        conta._saldo -= self.valor
        conta.numero_saques += 1
        conta.limite -= self.valor
        conta.historico.adicionar_transacao(f"Saque de R${self.valor:.2f}")
        print(f"Saque de R${self.valor:.2f} realizado com sucesso.")
        return True


class Historico:
    """Mantém o histórico de transações de uma conta."""
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, descricao):
        self.transacoes.append(descricao)

    def imprimir(self):
        print("============== EXTRATO ==============")
        if not self.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for t in self.transacoes:
                print(t)
        print("=====================================")


class Conta:
    """Classe base para contas bancárias."""
    _contador_contas = 1

    def __init__(self, titular, agencia="0001"):
        self.numero = Conta._contador_contas
        Conta._contador_contas += 1
        self.titular = titular  # Instância de Cliente ou PessoaFisica
        self.agencia = agencia
        self._saldo = 0.0
        self.historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def extrato(self):
        self.historico.imprimir()
        print(f"Saldo atual: R${self._saldo:.2f}")


class ContaCorrente(Conta):
    """Conta corrente com limites de saque."""
    def __init__(self, titular, agencia="0001", limite=500.0, limite_saques=3):
        super().__init__(titular, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0


class Cliente:
    """Representa um cliente genérico."""
    def __init__(self, cpf, nome, data_nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        print(f"Conta {conta.numero} adicionada ao cliente {self.nome}.")

    def listar_contas(self):
        if not self.contas:
            print("Este cliente não possui contas.")
            return
        for c in self.contas:
            print(f"[Agência {c.agencia}] Conta {c.numero} - Saldo: R${c.saldo:.2f}")


class PessoaFisica(Cliente):
    """Cliente pessoa física."""
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(cpf, nome, data_nascimento, endereco)


class SistemaBancario:
    """Gerencia usuários e contas, provendo interface de menu."""
    def __init__(self):
        self.usuarios = {}  # mapeia CPF -> Cliente

    def criar_usuario(self):
        cpf = input('Insira o CPF do cliente: ')
        if cpf in self.usuarios:
            print('Usuário já cadastrado.')
            return self.usuarios[cpf]
        nome = input('Insira o nome completo do cliente: ')
        data_nascimento = input('Data de nascimento (dd/mm/aaaa): ')
        endereco = input('Endereço (logradouro, bairro - cidade/UF): ')
        cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
        self.usuarios[cpf] = cliente
        print('Usuário cadastrado com sucesso.')
        return cliente

    def criar_conta_corrente(self):
        cpf = input('Digite o CPF do titular: ')
        cliente = self.usuarios.get(cpf)
        if not cliente:
            print('Cliente não encontrado. Cadastrando novo.')
            cliente = self.criar_usuario()
        conta = ContaCorrente(cliente)
        cliente.adicionar_conta(conta)
        print(f'Conta corrente criada. Número: {conta.numero}, Agência: {conta.agencia}')
        return conta

    def localizar_conta(self):
        cpf = input('CPF do titular: ')
        cliente = self.usuarios.get(cpf)
        if not cliente:
            print('Cliente não cadastrado.')
            return None
        if not cliente.contas:
            print('Cliente não possui contas.')
            return None
        if len(cliente.contas) == 1:
            return cliente.contas[0]
        print('Selecione uma conta:')
        for i, c in enumerate(cliente.contas, 1):
            print(f"[{i}] Conta {c.numero} (Ag {c.agencia})")
        idx = int(input('Opção: ')) - 1
        return cliente.contas[idx]

    def run(self):
        menu = '''

============== MENU ==============
[1] Depositar
[2] Sacar
[3] Extrato
[4] Cadastrar Cliente
[5] Listar Clientes
[6] Criar Conta Corrente
[7] Sair
===================================
'''
        while True:
            print(menu)
            opcao = input('Selecione uma opção: ')
            if opcao == '1':
                conta = self.localizar_conta()
                if conta:
                    valor = float(input('Valor para depósito: '))
                    conta.depositar(valor)
            elif opcao == '2':
                conta = self.localizar_conta()
                if conta:
                    valor = float(input('Valor para saque: '))
                    conta.sacar(valor)
            elif opcao == '3':
                conta = self.localizar_conta()
                if conta:
                    conta.extrato()
            elif opcao == '4':
                self.criar_usuario()
            elif opcao == '5':
                for u in self.usuarios.values():
                    print(f"{u.cpf} - {u.nome}")
            elif opcao == '6':
                self.criar_conta_corrente()
            elif opcao == '7':
                print('Encerrando sistema.')
                break
            else:
                print('Opção inválida, tente novamente.')


if __name__ == '__main__':
    sistema = SistemaBancario()
    sistema.run()