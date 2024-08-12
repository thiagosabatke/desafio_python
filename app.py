def menu():
    menu = """
    ======== Menu ========
    [1]Depositar
    [2]Sacar
    [3]Extrato
    [4]Cadastrar cliente
    [5]Cadastrar conta
    [6]Listar contas
    [7]Sair
    =====================
    """
    return input(menu)

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
    else:
        print("Valor inválido para depósito")
    return saldo, extrato
  
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Saldo insuficiente!")
    elif valor > limite:
        print("Valor do saque excede o limite!")
    elif numero_saques >= limite_saques:
        print("Número máximo de saques excedido!")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print("Saque efetuado com sucesso")
    return saldo, extrato, numero_saques
    
def extrato(saldo, /, *, extrato):
    print("======= Extrato =======")
    if extrato:
        for item in extrato:
            print(item)
    else:
        print("Nenhuma movimentação realizada")
    print(f"Saldo atual: R$ {saldo:.2f}")  
    print("=======================") 

def criar_cliente(clientes):
    cpf = input("Digite o CPF do cliente (apenas números): ")
    if len(cpf) < 11:
        print("Digite um CPF válido!")
        return
    usuario = buscar_usuario(cpf, clientes)

    if usuario:
        print("Já existe um usuário com esse CPF!")
        return

    nome = input("Digite o nome do cliente: ")
    nascimento = input("Digite a data de nascimento do cliente (dd-mm-aaaa): ")
    endereco = input("Digite o endereço do cliente (logradouro, número - bairro - cidade/sigla estado): ")
    
    cliente = {"nome": nome, "nascimento": nascimento, "cpf": cpf, "endereco": endereco}
    clientes.append(cliente)
    
    print("Cliente cadastrado com sucesso!")
    return cliente

def buscar_usuario(cpf, clientes):
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            return cliente
    return None

def criar_conta(agencia, num_conta, clientes):
    cpf = input("Informe o CPF do usuário:")
    cliente = buscar_usuario(cpf, clientes)
    
    if cliente:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": num_conta, "usuario": cliente}
    
    print("Usuário não encontrado, fluxo de criação de conta encerrado!")

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    for conta in contas:
        listar = f"""
        Agência: {conta['agencia']}
        Conta: {conta['numero_conta']}
        Titular da conta: {conta['usuario']['nome']}
        """
        print(listar)

def main():
    saldo = 0
    limite = 500
    extrato_list = []
    numero_saques = 0
    limite_saques = 3
    clientes = []
    contas = []
    AGENCIA = "0001"  

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato_list = depositar(saldo, valor, extrato_list)
        
        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato_list, numero_saques = sacar( 
                saldo=saldo,
                valor=valor,
                extrato=extrato_list,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=limite_saques
            )
        elif opcao == "3":
            extrato(saldo, extrato=extrato_list)
        
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
            print("Opção inválida! Digite uma opção válida.")

main()
