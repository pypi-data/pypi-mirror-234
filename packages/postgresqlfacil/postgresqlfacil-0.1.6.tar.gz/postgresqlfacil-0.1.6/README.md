# PostgreSQLFacil
O pacote PostgreSQLFacil oferece uma interface simplificada para interagir com o banco de dados PostgreSQL, abstraindo as operações comuns de SELECT, INSERT, UPDATE e DELETE em métodos convenientes e com integrações em DataFrames do pandas.

# Instalação
Para utilizar o pacote CalendarioFinanceiro, você precisa instalá-lo primeiro. Isso pode ser feito utilizando o gerenciador de pacotes pip. Execute o seguinte comando no terminal:

```shell
pip install PostgreSQLFacil
```

# Uso Básico
Aqui está um exemplo de como você pode usar o PostgreSQLFacil para realizar operações com o banco de dados PostgreSQL:

```py
from PostgreSQLFacil import ConectorPostgreSQL
import pandas as pd


# Configuração das informações de conexão
config = {
    "database": "seu_banco_de_dados",
    "user": "seu_usuario",
    "password": "sua_senha",
    "host": "seu_host",
    "port": "sua_porta",
}

# Inicialização do ConectorPostgreSQL
with ConectorPostgreSQL(**config) as SQL:
    # Executa uma consulta SELECT e obtém o resultado como um DataFrame
    df_consulta = SQL.executa_query_select('SELECT * FROM sua_tabela;')

    # Executa uma inserção de dados
    query_insert = 'INSERT INTO sua_tabela (coluna1, coluna2) VALUES (valor1, valor2);'
    SQL.executa_query_insert(query_insert)

    # Executa um update
    query_update = 'UPDATE sua_tabela SET coluna1 = novo_valor WHERE coluna2 = valor_alvo;'
    SQL.executa_query_update(query_update)

    # Executa um delete
    query_delete = 'DELETE FROM sua_tabela WHERE coluna = valor_alvo;'
    SQL.executa_query_delete(query_delete)
```

# Métodos Disponíveis
### executa_query_select(query: str) -> pd.DataFrame
Executa um SELECT statement e retorna o resultado como um DataFrame. Em caso de erro, retorna um DataFrame vazio.

### executa_query_insert(query: str, returning=False) -> int
Executa um INSERT statement e retorna o valor solicitado (geralmente o último ID inserido) se especificado. Retorna True em caso de sucesso.

### executa_query_update(query: str) -> bool
Executa um UPDATE statement e retorna True em caso de sucesso.

### executa_query_delete(query: str) -> bool
Executa um DELETE statement e retorna True em caso de sucesso.

### transforma_df_em_insert_statement(df: pd.DataFrame, tabela: str) -> str
Transforma um DataFrame em um INSERT statement para a tabela especificada.
