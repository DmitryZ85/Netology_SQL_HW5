import psycopg2

def create_db(cur):
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


def add_client(cur, first_name, last_name, email):
    cur.execute('''
    INSERT INTO client(first_name, last_name, email)  VALUES(%s, %s, %s);
    ''', (first_name, last_name, email))

        
def add_phone(cur, number, client_id):
    cur.execute('''
    INSERT INTO phone(number, client_id) VALUES(%s, %s)
    ''', (number, client_id))


def change_client():
    print("Для изменения информации о клиенте, пожалуйста, введите нужную Вам команду.\n "
          "1 - изменить имя; 2 - изменить фамилию; 3 - изменить email; 4 - изменить номер телефона")

    while True:
        command = int(input())

        if command == 1:
            input_id = input('Введите ID клиента для изменения его данных: ')
            input_new_name = input('Введите новое имя: ')
            cur.execute('''
            UPDATE client
            SET first_name = %s
            WHERE id = %s;
            ''', (input_new_name, input_id))
            break
        elif command == 2:
            input_id = input('Введите ID клиента для изменения его данных: ')
            input_new_lastname = input('Введите новую фамилию: ')
            cur.execute('''
            UPDATE client
            SET last_name = %s
            WHERE id = %s;
            ''', (input_new_lastname, input_id))
            break
        elif command == 3:
            input_id = input('Введите ID клиента для изменения его данных: ')
            input_new_email = input('Введите новый email: ')
            cur.execute('''
                UPDATE client
                SET email = %s
                WHERE id = %s;
                ''', (input_new_email, input_id))
            break
        elif command == 4:
            input_phone = input('Введите номер телефона, который нужно изменить: ')
            input_new_phone = input('Введите новый номер телефона: ')
            cur.execute('''
                UPDATE phone
                SET number = %s
                WHERE number = %s;
                ''', (input_new_phone, input_phone))
            break
        else:
            print("Вы ввели неправильную команду, пожалуйста, повторите ввод")


def delete_phone(cur, client_id,):
   cur.execute('''
   DELETE FROM phone
   WHERE client_id = %s
   ''', (client_id))


def delete_client(cur, id):
   cur.execute('''
   DELETE FROM client
   WHERE id = %s
   ''', (id))


def find_client():
    print("Для поиска информации о клиенте, пожалуйста, введите одну из команд:\n "
          "1 - Поиск по имени; 2 - Поиск по фамилии; 3 - Поиск по e-mail; 4 - Поиск по номеру телефона")

    while True:
        command = int(input('Введите команду для поиска информации о клиенте: '))
        if command == 1:
            input_name = input("Введите имя для поиска: ")
            cur.execute("""
            SELECT c.id, first_name, last_name, email, number
            FROM client AS c
            LEFT JOIN phone AS p ON p.client_id = c.id
            WHERE first_name=%s
            """, (input_name,))
            print(cur.fetchall())
            break
        elif command == 2:
            input_lastname= input("Введите фамилию для поиска: ")
            cur.execute("""
            SELECT c.id, first_name, last_name, email, number
            FROM client AS c
            LEFT JOIN phone AS p ON p.client_id = c.id
            WHERE last_name=%s
            """, (input_lastname,))
            print(cur.fetchall())
            break
        elif command == 3:
            input_email = input("Введите email для поиска: ")
            cur.execute("""
            SELECT c.id, first_name, last_name, email, number
            FROM client AS c
            LEFT JOIN phone AS p ON p.client_id = c.id
            WHERE email=%s
            """, (input_email,))
            print(cur.fetchall())
            break
        elif command == 4:
            input_phonenumber = input("Введите номер телефона для поиска: ")
            cur.execute("""
            SELECT c.id, first_name, last_name, email, number
            FROM client AS c
            LEFT JOIN phone AS p ON p.client_id = c.id
            WHERE number=%s
            """, (input_phonenumber,))
            print(cur.fetchall())
            break
        else:
            print("Вы ввели неправильную команду, пожалуйста, повторите ввод")


if __name__ == "__main__":
    with psycopg2.connect(database="netology_hw5", user="postgres", password="Z25instr") as conn:
        with conn.cursor() as cur:
            create_db(cur)
            add_client(cur, 'Cool', 'Guy', 'c@gmail.com')
            add_client(cur, 'Pop', 'Bob', 'p@mail.ru')
            add_phone(cur, '890330332211', 1)
            add_phone(cur, '1425808993', 2)
            change_client()
            find_client()

    conn.close()