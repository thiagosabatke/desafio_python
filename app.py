from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_tarefas(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n===== Operação inválida! Saldo insuficiente! =====")
        elif valor > 0:
            self._saldo -= valor
            print("\n----- Saque realizado! -----")
            return True
        else:
            print("\n===== Operação inválida! Valor inválido! =====")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n----- Depósito realizado! -----")
            return True
        else:
            print("\n===== Operação inválida! Valor inválido! =====")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n===== Operação inválida! O valor do saque excede o limite. =====")
        elif excedeu_saques:
            print("\n===== Operação inválida! Número máximo de saques excedido. =====")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\n
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """
    ======== Menu ========
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Cadastrar cliente
    [5] Cadastrar conta
    [6] Listar contas
    [7] Sair
    ======================
    """
    return input(menu)


def criar_cliente(clientes):
    cpf = input("Digite o CPF do cliente (apenas números): ")
    if len(cpf) != 11:
        print("CPF inválido!")
        return
    usuario = buscar_usuario(cpf, clientes)

    if usuario:
        print("Já existe um cliente com esse CPF!")
        return

    nome = input("Digite o nome do cliente: ")
    nascimento = input("Digite a data de nascimento do cliente (dd-mm-aaaa): ")
    endereco = input("Digite o endereço do cliente (logradouro, número - bairro - cidade/estado): ")

    cliente = PessoaFisica(nome, nascimento, cpf, endereco)
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")


def buscar_usuario(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def criar_conta(agencia, num_conta, clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_usuario(cpf, clientes)

    if cliente:
        conta = ContaCorrente(num_conta, cliente)
        cliente.adicionar_conta(conta)
        print("Conta criada com sucesso!")
        return conta
    print("Cliente não encontrado!")


def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    for conta in contas:
        print(conta)


def main():
    clientes = []
    contas = []
    AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao == "1":
            cpf = input("Informe o CPF do cliente: ")
            cliente = buscar_usuario(cpf, clientes)
            if cliente:
                conta = cliente.contas[0]  # Usando a primeira conta cadastrada
                valor = float(input("Informe o valor do depósito: "))
                transacao = Deposito(valor)
                cliente.realizar_tarefas(conta, transacao)
            else:
                print("Cliente não encontrado!")

        elif opcao == "2":
            cpf = input("Informe o CPF do cliente: ")
            cliente = buscar_usuario(cpf, clientes)
            if cliente:
                conta = cliente.contas[0]
                valor = float(input("Informe o valor do saque: "))
                transacao = Saque(valor)
                cliente.realizar_tarefas(conta, transacao)
            else:
                print("Cliente não encontrado!")

        elif opcao == "3":
            cpf = input("Informe o CPF do cliente: ")
            cliente = buscar_usuario(cpf, clientes)
            if cliente:
                conta = cliente.contas[0]
                print("\n===== Extrato =====")
                for transacao in conta.historico.transacoes:
                    print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} em {transacao['data']}")
                print(f"Saldo atual: R$ {conta.saldo:.2f}")
                print("===================")
            else:
                print("Cliente não encontrado!")

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, num_conta, clientes)
            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Escolha uma opção válida.")


if __name__ == "__main__":
    main()
