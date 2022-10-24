import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(60) NOT NULL,
        last_name VARCHAR(80),
        email VARCHAR(100) UNIQUE
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        number VARCHAR(12),
        client_id INTEGER REFERENCES client(id)
        );
        ''')
        return conn.commit()

def add_client(conn, first_name, last_name, email, number=None):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO client(first_name, last_name, email)  VALUES(%s, %s, %s);
        ''', (first_name, last_name, email))
        return conn.commit()
        
def add_phone(conn, number, client_id):
    with conn.cursor() as cur:
       cur.execute('''
       INSERT INTO phone(number, client_id) VALUES(%s, %s)
       ''', (number, client_id))
       return conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
       cur.execute('''
       UPDATE client
       SET first_name = %s, last_name = %s, email = %s
       WHERE id = %s;
       ''', (client_id, first_name, last_name, email))
       return conn.commit()

def delete_phone(conn, client_id, number):
    with conn.cursor() as cur:
       cur.execute('''
       DELETE FROM phone
       WHERE client_id = %s
       ''', (client_id))
       return conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
       cur.execute('''
       DELETE FROM client
       WHERE id = %s
       ''', (client_id))
       return conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
       cur.execute('''
       SELECT % FROM client
       WHERE  first_name = %s OR last_name = %s OR email = %s or number = %s;
       ''', (first_name, last_name, email, number))
       return print(cur.fetchall())


with psycopg2.connect(database="netology_hw5", user="postgres", password="Z25instr") as conn:
    create_db(conn)
    add_client(conn, 'Cool', 'Guy', 'c@gmail.com')
    add_client(conn, 'Pop', 'Bob', 'p@mail.ru')
    add_phone(conn, '890330332211', 1)
    add_phone(conn, '1425808993', 2)
    change_client(conn, 1, 'Vasya', 'Petrov', 'petrov@gmail.com')
    find_client(conn, last_name='Petrov')

conn.close()