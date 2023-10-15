import sqlite3
import uuid

def generate_random_id():
    random_id = str(uuid.uuid4())[:7]
    return random_id



class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE users (
            id varchar(7) NOT NULL,
            full_name varchar(255) NOT NULL,
            telegram_id int NOT NULL UNIQUE,
            username varchar(255) NULL,
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def create_messages_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS messages(
            chat_id int NOT NULL,
            message_id int NOT NULL,
            push_date datetime NOT NULL
        );
        """
        self.execute(sql, commit=True)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, full_name: str, telegram_id: int, username: str = None):
        # SQL_EXAMPLE = "INSERT INTO users(id, name, username) VALUES(1, 'John', 'John@gmail.com')"
        random_id = generate_random_id()
        print(random_id)
        sql = f"""
        INSERT INTO users(id, full_name, telegram_id, username) VALUES('{random_id}', ?, ?, ?)
        """
        self.execute(sql, parameters=(full_name, telegram_id, username), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM users where id=1 AND name='John'"
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)
    
    def add_message(self, chat_id: int, message_id: int, push_date: str):
        sql = """
        INSERT INTO messages(chat_id, message_id, push_date) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(chat_id, message_id, push_date), commit=True)
    

    def get_message_chat_id(self, message_id: int):
        sql = """
        SELECT chat_id FROM messages WHERE message_id = ?
        """
        return self.execute(sql, parameters=(message_id,), fetchone=True)[0]


    # def update_user_username(self, username, id):
    #     # SQL_EXAMPLE = "UPDATE users SET username=mail@gmail.com WHERE id=12345"

    #     sql = f"""
    #     UPDATE users SET username=? WHERE id=?
    #     """
    #     return self.execute(sql, parameters=(username, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
