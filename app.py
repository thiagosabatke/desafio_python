menu = """

##### MENU #####

[1] DEPOSITAR
[2] SACAR
[3] EXTRATO
[4] SAIR

################

"""

saldo = 0
limite_diario = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    print(menu)
    opcao = input("Escolha uma opção a seguir: ")

    if opcao == "1":
        print("\n#### Depósito ####")
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0 :
            saldo += valor
            extrato += f"Depósito : R$ {valor:.2f}/n"

        else: 
            print("valor informado é inválido")

    elif opcao == "2":
        print("\n#### Saque ####")
        valor = float(input("Informe o valor do saque: "))
        print(f"Saque efetuado de R$ {valor:.2f}")

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite_diario
        excedeu_saques = numero_saques >= LIMITE_SAQUES  

        if excedeu_saques:
            print("Operação falhou! Você nao tem saldo suficiente")
        
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "3":
        print("\n#### EXTRATO ####")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
    
    elif opcao == "4":
        print("Saindo do sistema...")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada")