from collections import defaultdict
import textwrap
from datetime import datetime
from pathlib import Path

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ROOT_PATH = Path(__file__).parent
        Log_arquivo_path = ROOT_PATH / "log.txt"

        with open(Log_arquivo_path, "a") as log_file:
            log_file.write(f"[{data_hora}] Funcao '{func.__name__}' executada com argumentos {args} e {kwargs}. Retornou {resultado}\n")
                

        print(f"{data_hora}: {func.__name__.upper()}")
        return resultado
    return envelope


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.titular.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


def listar_contas(clientes):
    for cliente in clientes:
        for conta in ContasIterador(cliente.contas):
            print(str(conta))


class Transacao:
    """Representa uma transação genérica no sistema bancário."""
    transacoes_por_dia = defaultdict(int)

    def __init__(self, valor):
        self.valor = valor

    def registrar(self, funcao):
        raise NotImplementedError("Método registrar deve ser implementado pelas subclasses.")


class Deposito(Transacao):
    """Transação de depósito."""
    @log_transacao
    def registrar(self, conta, hoje=None):
        if hoje is None:
            hoje = datetime.now().date()
        
        if self.valor <= 0:
            print("Valor inválido para depósito.")
            return False
        if conta.numero_transacoes >= conta.limite_transacoes:
            print("Número máximo de saques diários atingido.")
            return False
        if Transacao.transacoes_por_dia[hoje] >= 10:
            return False
        else:
            Transacao.transacoes_por_dia[hoje] += 1
        
        conta._saldo += self.valor
        conta.numero_transacoes += 1
        conta.historico.adicionar_transacao(f"Depósito de R${self.valor:.2f} na data {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Depósito de R${self.valor:.2f} realizado com sucesso.")
        return True


class Saque(Transacao):
    """Transação de saque, respeitando limites da conta corrente."""
    @log_transacao
    def registrar(self, conta, hoje=None):
        if hoje is None:
            hoje = datetime.now().date()

        if self.valor <= 0:
            print("Valor inválido para saque.")
            return False
        if conta.numero_transacoes >= conta.limite_transacoes:
            print("Número máximo de saques diários atingido.")
            return False
        if self.valor > conta._saldo:
            print("Saldo insuficiente para saque.")
            return False
        if self.valor > conta.limite:
            print("Valor excede o limite disponível para saque.")
            return False
        if Transacao.transacoes_por_dia[hoje] >= 10:
            return False
        else:
            Transacao.transacoes_por_dia[hoje] += 1
        
        conta._saldo -= self.valor
        conta.numero_transacoes += 1
        conta.limite -= self.valor
        conta.historico.adicionar_transacao(f"Saque de R${self.valor:.2f} na data {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Saque de R${self.valor:.2f} realizado com sucesso.")
        return True


class Historico:
    """Mantém o histórico de transações de uma conta."""
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, descricao):
        self.transacoes.append(descricao)
    
    @log_transacao
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
    def __init__(self, titular, agencia="0001", limite=500.0, limite_transacoes=10):
        super().__init__(titular, agencia)
        self.limite = limite
        self.limite_transacoes = limite_transacoes
        self.numero_transacoes = 0


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
    
    @log_transacao
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
    
    @log_transacao
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
                listar_contas(self.usuarios.values())
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