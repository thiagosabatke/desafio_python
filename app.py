menu = """

##### MENU #####

[0] DEPOSITAR
[1] SACAR
[2] EXTRATO
[3] SAIR

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

    if opcao == "0":
        print("#### Depósito ####")
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0 :
            saldo += valor
            extrato += f"Depósito : R$ {valor:.2f}/n"
        else: 
            print("valor informado é inválido")

    elif opcao == "1":
        print("Saque")
    
    elif opcao == "2":
        print("Extrato")
    
    elif opcao == "3":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada")