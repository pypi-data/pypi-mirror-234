import logging
import sqlite3
import time


class SimpleDB:
    def __init__(self, db_name):
        self.database_name = db_name
        self.conn = None

        # self.delete_table()
        if not self.check_exists():
            self.create_table()

    def db_connect(self):
        self.conn = sqlite3.connect(self.database_name)

    def db_close(self):
        self.conn.close()

    def check_exists(self):
        """
        Simple method to check the database exists.

        :return: Boolean : True if exists else False
        """

        self.db_connect()

        cur = self.conn.cursor()

        try:
            cur.execute(f"SELECT * FROM {self.database_name}")

            # storing the data in a list
            data_list = cur.fetchall()

            return True

        except sqlite3.OperationalError:
            return False

        finally:
            self.db_close()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS kodiak_db (
                id TEXT PRIMARY KEY,
                username TEXT,
                password TEXT,
                api_key TEXT,
                session TEXT,
                session_time TEXT,
                refresh_token TEXT,
                kodiak_port TEXT,
                lock_key TEXT
            )
        """
        self.db_connect()
        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            self.conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        finally:
            self.db_close()

    # def insert_kodiak_db(self, ipaddress, username, password, key):
    #     query = "INSERT INTO kodiak_db (id, username, password, api_key) VALUES (?, ?, ?, ?)"
    #     self.db_connect()
    #     self.conn.execute(query, (ipaddress, username, password, key))
    #     self.conn.commit()
    #     self.db_close()

    def insert_kodiak_db_standard(self, ipaddress, key):
        query = "INSERT INTO kodiak_db (id, api_key) VALUES (?, ?)"
        self.db_connect()

        cursor = self.conn.cursor()

        try:
            cursor.execute(query, (ipaddress, key))
            self.conn.commit()


            if cursor.rowcount > 0:
                return True
            else:
                return False

            self.db_close()

        except sqlite3.IntegrityError as error:
            self.db_close()
            # the value we`re trying to update is already in the DB
            return self.update_kodiak_db(ipaddress, key)
        # finally:
        #     self.db_close()

    def get_kodiak_db(self, ipaddress):
        """
        Get the row from the DB with the specified Kodiak IP
        ORDER: 0:IP, 1:User, 2:pass, 3:api_key, 4:session_key, 5:session_time, 6:refresh_token, 7:lock_key

        :param ipaddress: IPaddress of the kodiak module

        :return: Return tuple or results if success else None
        """

        query = "SELECT * FROM kodiak_db WHERE id = ?"

        self.db_connect()

        cursor = self.conn.execute(query, (ipaddress,))
        result = cursor.fetchone()

        if not result:
            result = None

        self.db_close()

        return result

    def get_ip_addresses(self):

        """
        Get every IP address currently found that doesn't have an API Key
        ORDER: 0:IP, 1:User, 2:pass, 3:api_key, 4:session_key, 5:session_time, 6:refresh_token, 7:lock_key

        :param ipaddress: IPaddress of the kodiak module

        :return: Return tuple or results if success else None
        """

        query = "SELECT * FROM kodiak_db WHERE id = ?"

        self.db_connect()

        cursor = self.conn.execute(query, (ipaddress,))
        result = cursor.fetchone()

        if not result:
            result = None

        self.db_close()

        return result

    def update_kodiak_db(self, ipaddress, key):
        self.db_connect()

        query = "UPDATE kodiak_db SET api_key = ? WHERE id = ?"
        cursor = self.conn.cursor()

        try:
            cursor.execute(query, (key, ipaddress))
            self.conn.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as err:
            logging.warning(err)
            return False

        finally:
            self.db_close()

    def update_kodiak_db_session_key(self, ipaddress, session_key, refresh_token):
        self.db_connect()

        query = "UPDATE kodiak_db SET session = ? WHERE id = ?"
        self.conn.execute(query, (session_key, ipaddress))
        query = "UPDATE kodiak_db SET session_time = ? WHERE id = ?"
        self.conn.execute(query, (time.time(), ipaddress))
        query = "UPDATE kodiak_db SET refresh_token = ? WHERE id = ?"
        self.conn.execute(query, (refresh_token, ipaddress))
        self.conn.commit()

        self.db_close()

    def update_kodiak_db_lock_key(self, ipaddress, lock_key):
        query = "UPDATE kodiak_db SET lock_key = ? WHERE id = ?"

        self.db_connect()
        cursor = self.conn.cursor()

        try:
            cursor.execute(query, (lock_key, ipaddress))
            self.conn.commit()

            if cursor.rowcount > 0:
                return True
            else:
                logging.warning("Failed to update lock_key to db")
                return False
        finally:
            self.db_close()

    def update_kodiak_db_kodiak_port(self, ipaddress, port):
        query = "UPDATE kodiak_db SET kodiak_port = ? WHERE id = ?"

        self.db_connect()

        cursor = self.conn.cursor()

        try:
            cursor.execute(query, (port, ipaddress))
            self.conn.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False
        finally:
            self.db_close()

    def update_kodiak_db_kodiak_user(self, ipaddress, username):
        query = "UPDATE kodiak_db SET username = ? WHERE id = ?" #password

        self.db_connect()

        cursor = self.conn.cursor()

        try:
            cursor.execute(query, (username, ipaddress))
            self.conn.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False
        finally:
            self.db_close()

    def update_kodiak_db_kodiak_password(self, ipaddress, password):
        query = "UPDATE kodiak_db SET password = ? WHERE id = ?" #password

        self.db_connect()

        cursor = self.conn.cursor()

        try:
            cursor.execute(query, (password, ipaddress))
            self.conn.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False
        finally:
            self.db_close()

    def remove_kodiak_from_db(self, ipaddress):
        query = "DELETE FROM kodiak_db WHERE id = ?"

        self.db_connect()

        self.conn.execute(query, (ipaddress,))
        self.conn.commit()

        self.db_close()

        return True

    def delete_table(self):
        query = "DROP TABLE IF EXISTS kodiak_db"

        self.db_connect()

        cursor = self.conn.cursor()

        cursor.execute(query)
        self.conn.commit()

        try:
            if cursor.rowcount > 0:
                return True
            else:
                return False
        finally:
            self.db_close()


# Example usage
if __name__ == "__main__":
    db = SimpleDB("mykodiak_dbbase.db")
    ipaddress = '127.0.0.1'
    user = "matt"
    password = 'holsey'
    key = 'somekey'

    db.db_connect()

    db.delete_table()

    db.create_table()

    db.insert_kodiak_db_standard(ipaddress, key)

    print(f"Value of '{ipaddress}':", db.get_kodiak_db("127.0.0.1"))

    db.update_kodiak_db(ipaddress, key + "2")

    print(f"Updated value of '{ipaddress}':", db.get_kodiak_db(ipaddress))

    db.remove_kodiak_from_db(ipaddress)

    print(f'Removed value of {ipaddress} from table')

    print(f'Checking it was removed: {db.get_kodiak_db(ipaddress)}')



