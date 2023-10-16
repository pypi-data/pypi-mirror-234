import datetime
import math
import pandas as pd
import psycopg2


class ConectorPostgreSQL:
    """
    Conector do Banco de Dados.

    Exemplo de seu uso em Context Manager:
        >>> with ConectorPostgreSQL(**{...}) as ConectorSQL:
        >>>     ...
    """

    def __init__(self, database, user, password, host, port):
        config = {
            "database": database,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        self.con = psycopg2.connect(**config)
        self.con.autocommit = True

        cursor = self.con.cursor()
        cursor.execute("SET TIME ZONE 'America/Sao_Paulo'")
        cursor.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def executa_query_select(self, query: str) -> pd.DataFrame:
        """
        Executa um Select Statement e retorna o resultado em uma dataframe
        Em caso de erro, retorna uma dataframe vazia.

        Exemplo:
            >>> df_consulta = SQL.executa_query_select(
            >>>     'SELECT {...} FROM {...};'
            >>> )
            >>> df_consulta
                id      data descricao
            0   1 2000-01-01       ...
            1   2 2000-02-01       ...
        """

        cursor = self.con.cursor()

        try:
            cursor.execute(query)

            dados = cursor.fetchall()
            colunas = [campo[0] for campo in cursor.description]
            cursor.close()

            return pd.DataFrame(dados, columns=colunas)

        except Exception as erro:
            print(erro)
            return pd.DataFrame()

    def executa_query_insert(self, query: str, returning=False) -> int:
        """
        Recebe um Insert Statement que retorna ou não um valor solicitado pelo
        usuário, geralmente o último id adicionado.

        Exemplo:
            >>> id_inserido = SQL.executa_query_insert(
            >>>     'INSERT INTO ... (...) VALUES (...) RETURNING id;',
            >>>     returning=True
            >>> )
            >>> id_inserido
            42
        """

        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            if returning:
                returning_value = cursor.fetchone()[0]
                cursor.close()
                return returning_value
            else:
                cursor.close()
                return True

        except Exception as erro:
            print(erro)
            if returning:
                return 0
            else:
                return False

    def executa_query_update(self, query: str) -> bool:
        """
        Recebe um Update Statement que retorna um bool

        Em caso de erro, retorna 0

        Exemplo:
            >>> update = SQL.executa_query_update(
            >>>     'UPDATE ... SET ... = ...;'
            >>> )
            >>> update
            True
        """

        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            cursor.close()
            return True

        except Exception as erro:
            print(erro)
            return False

    def executa_query_delete(self, query: str) -> bool:
        """
        Recebe um Delete Statement que retorna um bool

        Em caso de erro, retorna 0

        Exemplo:
            >>> delete = SQL.executa_query_update(
            >>>     'DELETE FROM ... WHERE ...;'
            >>> )
            >>> delete
            True
        """

        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            cursor.close()
            return True

        except Exception as erro:
            print(erro)
            return False

    @staticmethod
    def transforma_df_em_insert_statement(
        df: pd.DataFrame, tabela: str
    ) -> str:
        query = f"""
            INSERT INTO {tabela}
            ({",".join(x for x in df.columns)})
            VALUES
            """
        for linha in df.itertuples():
            values = " ("
            for index, coluna in enumerate(df.columns):
                value = getattr(linha, coluna)
                if isinstance(value, str):
                    values += f"'{value}'"
                elif isinstance(value, datetime.date):
                    values += f"'{value.isoformat()}'"
                elif value is None or math.isnan(value):
                    values += "NULL"
                else:
                    values += str(value)

                if index != len(df.columns) - 1:
                    values += ", "

            query += values + "), "

        query = query[:-2]
        return query
