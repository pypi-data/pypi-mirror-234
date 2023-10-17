import base64
import sqlite3
from typing import Union


class Database:
    """
    This class is used to store the API keys and other sensitive information.
    """
    __instance = None
    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance
    def __init__(self):
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
            #default values loaded
            self.index = {
                0:'openai_api_key',
                1:'powerwritingaid_api_key',
                2:'username',
                3:'password',
                4:'stealthgpt_api_key',
                5:'gptzero_api_key',
                6:'originality'
            }
            self.db = sqlite3.connect('database.db',check_same_thread=False)
            self.cursor = self.db.cursor()
            self.create_tables()
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings(
                id INTEGER PRIMARY KEY,
                key INTEGER,
                value TEXT
            )
        ''')
        self.db.commit()
    def get_settings(self, key: int) -> Union[str, bool]:
        """
            returns auth credintials matching the key value provided or False if no key is found
        """
        #check if user entered the special password for any key
        self.cursor.execute(''' SELECT value FROM user_settings WHERE key = ?''', (key,))
        dbKeys = self.cursor.fetchone()
        if dbKeys != None:
            if dbKeys[0] != '':
                return dbKeys[0]
        
        return False
    def set_settings(self, key: int, value: str) -> bool:
        """
            input: key to be used to get value from self.keys
            output: decrypted text
        """
        #check if user entered the special password for any key
        self.cursor.execute(''' SELECT * FROM user_settings''')
        dbKeys = self.cursor.fetchall()
        if len(dbKeys) > 0:
            for i in dbKeys:
                if i[1] == key:
                    self.cursor.execute('''
                        UPDATE user_settings SET value = ? WHERE key = ?
                    ''', (value, key))
                    self.db.commit()
                    return True
        self.cursor.execute('''
            INSERT INTO user_settings(
                key,
                value
            ) VALUES(?,?)
        ''', (
            key,
            value
        ))
        self.db.commit()
        return True
    def key_lable(self, key: int) -> str:
        name = self.index[key]
        #name to lowercase
        name = name.lower()
        #replace _ with space
        name = name.replace('_', ' ')
        #capitalize first letter
        name = name.capitalize()
        return name
        









#class Authentications:
#    """
#    This class is used to store the API keys and other sensitive information.
#    """
#    def __init__(self):
#        self.keys = [
#            #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
#            "A3W9xoG4xi3RJ8hDJ+Arip8EuIkHsvlckZMD93dbPs6U/Uv+0MJDvc5J5jMriCIbeI3Its/u6DdBcGxA1R4ZyQ==",
#            "Iu1OGO0gEHt23Dh8oNQXid4pLoxqme5JpHoR1pNzqBR14qXkPS2KunU81rICdrsH",
#            "Ts/xipUZZyTlMbiVYDERFQ==",
#            "rmfNufx4wp4guxAlRfRufA==",
#            "A3W9xoG4xi3RJ8hDJ+Arip8EuIkHsvlckZMD93dbPs6U/Uv+0MJDvc5J5jMriCIbeI3Its/u6DdBcGxA1R4ZyQ==",
#            "T4anlhWAE+UgvawRHK6XFs+Gg8QHZhRNUZ2KRaG5Ac6pjP1rKA0xh2o7H3IhJauWDRqiqBhS9GylKqC3dpQ07k68OE402XCwovzZbDizlOk=",
#            "bUPqNhMwY30HAwbEF6A/u8zT9MaizmJhv1cXGEKwNVqLVaL8I5teuLTQt6IyUDM7",
#            "CMEln/z2x/Yi+8DAp6jNIg==",
#            "kL3IcycSdBnnEGI3R4+zFQhTkPK64qu00k7zjC8WRWDnGKnzRaOd6sZfWw94FCu8"
#        ]
#    # Function
#    def decrypt(self,key: int) -> str:
#        """
#            input: key to be used to get value from self.keys
#            output: decrypted text
#        """
#        db = sqlite3.connect('database.db')
#        cursor = db.cursor()
#        feild = [
#            'openai_api_key'
#            'prowritingaid_api_key'
#            'username'
#            'password'
#            'openai_api_key'
#            'stealthgpt_api_key'
#            'gptzero_api_key'
#            'SPECIAL_PASSWORD'
#            'originality'
#        ]
#        if key == 0 or key == 4 or key == 5 or key == 6 or key == 8:
#            
#            cursor.execute('''
#                SELECT ? FROM settings
#            ''', (feild[key],))
#            dbKeys = cursor.fetchone()
#            db.close()
#            #check if any keys are in database
#            if dbKeys != None:
#                if dbKeys[0] != '':
#                    return dbKeys[0]
#        
#
#        ciphertext_base64 =  self.keys[key]
#
#        secret_key = 'ethddwjdozndjwis'
#        iv = 'hskahskelxnebtpd'
#        ciphertext = base64.b64decode(ciphertext_base64)
#        cipher = AES.new(secret_key.encode(), AES.MODE_CBC, iv.encode())
#        decrypted_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
#        return decrypted_bytes.decode('utf-8')
#    #return value of given key 
#
##0'openai_api_key
##1'prowritingaid_api_key
##2'username
##3'password
##4'OPENAI_API_KEY_DEFAULT
##5'STEALTHGPT_API_KEY_DEFAULT
##6'GPTZERO_API_KEY_DEFAULT
##7'SPECIAL_PASSWORD
##8'Orginality