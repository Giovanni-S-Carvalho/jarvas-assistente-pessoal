import psycopg2
import os
from anthropic import Anthropic
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

agora = datetime.now()

DB_PASSWORD = os.environ.get('DB_PASSWORD','')

def get_conexao():
    return psycopg2.connect(host='localhost',database='jarvas_db',user='postgres',password=DB_PASSWORD,port='5432'
)

def adicionar_coluna_categoria():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        ALTER TABLE minhas_despesas 
        ADD COLUMN IF NOT EXISTS categoria TEXT
    """)
    conn.commit()
    conn.close()

def criar_tabelas():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boleto_apartamento(
            id SERIAL PRIMARY KEY,
            recebedor TEXT,
            valor REAL,
            vencimento TEXT,
            status TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS minhas_despesas(
            id SERIAL PRIMARY KEY,
            categoria TEXT,
            despesa TEXT,
            valor REAL,
            status TEXT,
            vencimento TEXT          
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lista_desejos_ap(
            id SERIAL PRIMARY KEY,
            item TEXT,
            valor REAL,
            marca TEXT
        );
    """)
    conn.commit()
    conn.close()

def resumo_geral():
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(valor) FROM boleto_apartamento WHERE status = 'Pago'")
    pago = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT SUM(valor) FROM boleto_apartamento WHERE status = 'Pendente'")
    pendente = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT SUM(valor) FROM lista_desejos_ap')
    desejos = cursor.fetchone()[0] or 0.0

    cursor.execute("""
        SELECT recebedor, valor, vencimento
        FROM boleto_apartamento
        WHERE status = 'Pendente'
        ORDER BY vencimento ASC
        LIMIT 1
    """)
    proximo = cursor.fetchone()

    conn.close()

    nome_mes = agora.strftime("%B")
    print(f'Total investido no seu imovel: R$ {pago:.2f}')
    print(f'Total ainda pendente de pagamento para o mês de {nome_mes}: R$ {pendente:.2f}')
    print(f'Meta para mobilia e desejos: R$ {desejos:.2f}')
    print(f'\nCusto total do projeto: R$ {(pago + pendente + desejos):.2f}')

    if proximo:
        print(f'Proximo boleto a vencer: {proximo[0]} R$ {proximo[1]} em {formatar_data(proximo[2])}')
    else:
        print('Proximo boleto a vencer: Tudo em dia Senhor!')
    return

def pagar_boleto_ap(id_boleto):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE boleto_apartamento SET status = 'Pago' WHERE id = %s", (id_boleto,))
    conn.commit()
    conn.close()
    print(f'JARVAS: Boleto ID: {id_boleto} alterado para PAGO com sucesso!')

def retirar_item_lista(id_item):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lista_desejos_ap WHERE id = %s', (id_item,))
    conn.commit()
    conn.close()
    print(f'Item {id_item} retirado com sucesso!')

def ler_sql_lista_desejos():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lista_desejos_ap')
    resultado = cursor.fetchall()
    conn.close()
    for i in resultado:
        print(f'ID: {i[0]} | Item: {i[1]} | Valor: {i[2]} | Marca: {i[3]}')

def ler_sql_boletos_ap():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boleto_apartamento')
    resultado = cursor.fetchall()
    conn.close()
    if not resultado:
        print('A tabela de boletos esta vazia no momento.')
    else:
        for i in resultado:
            print(f'ID: {i[0]} | Recebedor: {i[1]} | Valor: {i[2]} | Vencimento: {formatar_data(i[3])} | Status: {i[4]}')

def adicionar_sql_boletos_ap(recebedor, valor, vencimento, status):
    resultado = converter_data(vencimento)
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO boleto_apartamento(recebedor, valor, vencimento, status) VALUES(%s,%s,%s,%s)",
        (recebedor, valor, resultado, status)
    )
    conn.commit()
    conn.close()
    print(f'Boleto de {recebedor} adicionado com sucesso!')

def adicionar_sql_lista_desejos(item, valor, marca):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO lista_desejos_ap(item, valor, marca) VALUES(%s,%s,%s)',
        (item, valor, marca)
    )
    conn.commit()
    conn.close()

def adicionar_boleto_despesas(despesa, valor, status, vencimento):
    categoria = categorizar_despesa(despesa)
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO minhas_despesas(despesa, valor, status, vencimento, categoria) VALUES(%s,%s,%s,%s,%s)',
        (despesa, valor, status, vencimento, categoria)
    )
    conn.commit()
    conn.close()
    print(f'Boleto adicionado com sucesso! Categoria detectada: {categoria}')

def ler_boleto_despesas():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM minhas_despesas')
    resultado = cursor.fetchall()
    conn.close()
    for i in resultado:
        print(f'ID: {i[0]} | Categoria: {i[1]} | Despesa: {i[2]} | Valor: {i[3]} | Status: {i[4]} | Vencimento: {i[5]}')

def pagar_boleto_despesas(id_boleto):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE minhas_despesas SET status = 'Pago' WHERE id = %s", (id_boleto,))
    conn.commit()
    conn.close()

def total_boleto_despesas():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT COALESCE(SUM(valor), 0) FROM minhas_despesas')
    total = cursor.fetchone()[0] or 0.0
    conn.close()
    return total

def total_boleto_imovel():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM boleto_apartamento WHERE status = 'Pendente'")
    total = cursor.fetchone()[0] or 0.0
    conn.close()
    return total
# def formatar_data(data):
#     data = datetime.strptime(data,'%Y-%m-%d')# entrada
#     resultado = data.strftime('%d/%m/%Y')#saida
#     return resultado
def converter_data(data):
    data = datetime.strptime(data, '%d/%m/%Y')#entrada
    resultado = data.strftime('%Y-%m-%d')#saida    
    return resultado
    

client = Anthropic()
model = "claude-haiku-4-5"  # rapido e barato, bom pra tarefa simples de categorizacao

CATEGORIAS_VALIDAS = ["Moradia", "Transporte", "Alimentacao", "Lazer", "Saude", "Educacao", "Outros"]

categorizar_despesa_schema = {
    "name": "categorizar_despesa",
    "description": "Categoriza uma despesa pessoal em uma das categorias predefinidas.",
    "input_schema": {
        "type": "object",
        "properties": {
            "categoria": {
                "type": "string",
                "enum": CATEGORIAS_VALIDAS,
                "description": "A categoria que melhor representa essa despesa"
            }
        },
        "required": ["categoria"]
    }
}

def categorizar_despesa(descricao):
    response = client.messages.create(
        model=model,
        max_tokens=200,
        tools=[categorizar_despesa_schema],
        tool_choice={"type": "tool", "name": "categorizar_despesa"},
        messages=[{
            "role": "user",
            "content": f"Categorize esta despesa: '{descricao}'"
        }]
    )
    for block in response.content:
        if block.type == "tool_use":
            return block.input["categoria"]
    return "Outros"

def total_por_categoria():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT categoria, SUM(valor) 
        FROM minhas_despesas 
        GROUP BY categoria 
        ORDER BY SUM(valor) DESC
    """)
    resultado = cursor.fetchall()
    conn.close()
    for categoria, total in resultado:
        print(f'{categoria}: R$ {total:.2f}')