JARVAS

Assistente pessoal em Python para controlar os boletos do primeiro imóvel, acompanhar despesas do dia a dia e planejar a lista de itens da reforma. Os dados ficam em PostgreSQL, e as despesas são categorizadas automaticamente pela API da Anthropic (Claude).

O que ele faz
Boletos do apartamento: cadastra, lista e marca como pagos, com recebedor, valor, vencimento e status.
Resumo geral: mostra o total já pago, o total pendente, a meta para mobília e desejos, o custo total do projeto e o próximo boleto a vencer.
Despesas pessoais: registra despesas e as classifica sozinho em uma categoria (Moradia, Transporte, Alimentacao, Lazer, Saude, Educacao ou Outros).
Total por categoria: soma os gastos por categoria, do maior para o menor.
Lista de desejos do apartamento: guarda itens, valores e marcas, e permite retirar itens já comprados.
Como a categorização funciona

A função categorizar_despesa envia a descrição da despesa ao modelo claude-haiku-4-5 usando tool use com tool_choice forçado. O esquema da ferramenta restringe o campo categoria a uma lista fixa (enum), então a resposta sempre vem estruturada e dentro das categorias válidas, sem precisar interpretar texto livre. Se a resposta não trouxer a ferramenta, a despesa cai em Outros.

Tecnologias
Python 3.13
PostgreSQL, com psycopg2
API da Anthropic (anthropic)
python-dotenv para variáveis de ambiente
pandas, na análise financeira (analise_jarvas.py)
Estrutura
Arquivo	Conteúdo
database.py	Conexão com o Postgres, criação das tabelas, consultas e categorização com IA
jarvas.py	Interface do assistente
analise_jarvas.py	Análise financeira dos dados
testes.py	Testes
Configuração

Requer Python 3.13 e PostgreSQL local com um banco jarvas_db.

bash
pip install psycopg2-binary anthropic python-dotenv pandas
python -c "import database; database.criar_tabelas()"

Crie um .env na raiz com ANTHROPIC_API_KEY e DB_PASSWORD (senha do usuário postgres). O arquivo está no .gitignore e não deve ser commitado.

Tabelas
boleto_apartamento: id, recebedor, valor, vencimento, status
minhas_despesas: id, categoria, despesa, valor, status, vencimento
lista_desejos_ap: id, item, valor, marca

Todas as consultas usam parâmetros (%s), sem concatenar texto no SQL.

Próximos passos
Trocar REAL por NUMERIC(10,2) nas colunas de valor, para evitar erro de centavos em somas.
Padronizar o formato de data entre as duas tabelas de boletos.
Usar with nas conexões, para que fechem mesmo quando uma consulta falhar.
Autor

Giovanni de Souza Carvalho, estudante de Engenharia de Software (UNICID).