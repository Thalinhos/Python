import os
import psycopg2

try:
    with psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    ) as conn:
        with conn.cursor() as cur:
            # Exemplo de consulta que modifica o banco de dados
            cur.execute("INSERT INTO my_table (column1, column2) VALUES (%s, %s)", (value1, value2))
            
            # Simular uma exceção para demonstrar rollback
            # raise Exception("Erro simulado")

            # Exemplo de consulta apenas leitura
            cur.execute("SELECT * FROM my_table")
            rows = cur.fetchall()
            for row in rows:
                print(row)

        # Commit após o bloco do cursor
        conn.commit()

except Exception as e:
    print(f"Ocorreu um erro: {e}")
    conn.rollback()  # Rollback em caso de erro