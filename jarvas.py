from datetime import datetime
import locale
from database import *

import database 
database.adicionar_coluna_categoria()

locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
agora = datetime.now()

criar_tabelas()

def formatar_dinheiro(valor_texto):
    try:
        return float(str(valor_texto).replace(',', '.'))
    except ValueError:
        print("Valor inválido! Use 0.00")
        return 0.0

print(f'Inicializando JARVAS...\n Olá Senhor!\n\nStatus atual em: {agora.strftime("%d/%m/%Y %H:%M")}')

def menu_principal():
    while True:
        print("MENU PRINCIPAL\n0- Resumo Geral\n1- Imovel\n2- Minhas despesas\n9- Sair\nQual?\n")
        opcao = input("> ")
        if opcao == "0":
            resumo_geral()
        elif opcao == "1":
            menu_imovel()
        elif opcao == "2":
            menu_despesas()
        elif opcao == "9":
            break
    return 
    
def menu_imovel():
    print("1- Visualizar boletos\n2- Adicionar boletos\n3- Alterar status do boleto para pago\n4- Aumento com avanço de obra\n5- lista de desejos")
    opcao = input("> ")
    if opcao == "1":
        ler_sql_boletos_ap()
        total_valor = total_boleto_imovel()
        print(f"Valor total pendente: R${total_valor:.2f}")
    elif opcao == '2':
            recebedor = input('Qual empresa recebe?\n ')
            valor = input('Qual valor? ex: 189,37\n ')
            valor_corrigido = formatar_dinheiro(valor)
            vencimento = input('Qual vencimento do boleto? ex: 03/05/2026\n')
            status = 'Pendente'
            adicionar_sql_boletos_ap(recebedor, valor_corrigido, vencimento, status)
    elif opcao == '3':
            ler_sql_boletos_ap()
            id_pago = input('Qual o ID do boleto que você pagou?\n')
            pagar_boleto_ap(id_pago)
    elif opcao == '4':
            avanco = input('Qual valor do avanço de obra desse mês?\n> ')
            valor_avanco = formatar_dinheiro(avanco)
            adicionar_sql_boletos_ap('Avanço de Obra', valor_avanco, agora.strftime('%d/%m/%Y'), 'Pendente')
            print(f'Avanço de obra de R$ {valor_avanco:.2f} registrado com sucesso!')

    elif opcao == '5':
            ler_sql_lista_desejos()
            retirar_ou_adicionar = input('Gostaria de adicionar, remover algum item? a/r\n(Sair = 9)\n> ').lower()
            if retirar_ou_adicionar == 'a':
                nome_do_item = input('Qual o nome do item?\n')
                valor_do_item = input('Qual valor do item? ex: 299,90\n')
                valor_final = formatar_dinheiro(valor_do_item)
                marca_do_item = input('Qual a marca do item?\n')
                adicionar_sql_lista_desejos(nome_do_item, valor_final, marca_do_item)
            elif retirar_ou_adicionar == 'r':
                ler_sql_lista_desejos()
                id_para_remover = input('Qual ID do item que você quer remover? ')
                retirar_item_lista(id_para_remover)
            elif retirar_ou_adicionar == "9":          
                return
def menu_despesas():
    nome_mes = agora.strftime("%B")
    print(f"Oque gostaria de fazer nas despesas do mes de {nome_mes}?\n")
    opcao = input("1- Adicionar boleto\n2- Visualizar boleto\n3- Marcar boleto como pago\n4- Ver total por categoria\n> ")
    if opcao == '1':
            despesa = input('Qual é a despesa?\n')
            valor = input('Qual o valor? ex:189,37\n')
            valor_final = formatar_dinheiro(valor)
            status = 'Pendente'
            vencimento = input('Qual vencimento do boleto? ex: 03/05/2026\n')
            adicionar_boleto_despesas(despesa, valor_final, status, vencimento)

    elif opcao == '2':
            ler_boleto_despesas()
            total_pago = total_boleto_despesas()
            print(f'Valor total das despesas do mês: R$ {total_pago:.2f}')

    elif opcao == '3':
            ler_boleto_despesas()
            id_boleto = input('Qual o ID do boleto? ')
            pagar_boleto_despesas(id_boleto)
            print('Boleto alterado com sucesso!')

    elif opcao == '4':
            total_por_categoria()
menu_principal()