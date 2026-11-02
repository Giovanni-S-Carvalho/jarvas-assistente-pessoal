def menu_principal():
    while True:
        print("1- Despesas\n2- Relatórios\n0- Sair")
        opcao = input("> ")
        if opcao =="1":
            menu_despesas()
        elif opcao == "0":
            return
def menu_despesas():
    print("1- Adicionar\n2- Listar\n0- Voltar")
    opcao = input("> ")
    if opcao == "1":
        print("ok")
    elif opcao == "0":
        return

reze = MenuOpcao()

reze.fazer_pergunta()