import psycopg2
import re
import os
from configparser import ConfigParser

class PosgresqlClient:

    def __init__(self):
        #Read db.ini file
        config_object = ConfigParser()
        current_directory = os.path.dirname(__file__)
        config_file = os.path.join(current_directory, 'config.ini')
        config_object.read(config_file)
        postgresql_conn = config_object["POSTGRESQL"]
        postgresql_host = postgresql_conn["host"]
        postgresql_port = postgresql_conn["port"]
        postgresql_usr = postgresql_conn["user"]
        postgresql_psw = postgresql_conn["passwd"]
        postgresql_db = postgresql_conn["db"]

        self.__schema = postgresql_conn["schema"]
        self.__connection = psycopg2.connect(
            host=postgresql_host, 
            port=postgresql_port,
            database=postgresql_db, 
            user=postgresql_usr, 
            password=postgresql_psw
        )

        self.__cur = self.__connection.cursor()

    def _launch_query(self, query):
        print(query)
        self.__cur.execute(query)
        matches = re.search(r"^SELECT", query, re.IGNORECASE)
        if not matches:
            self.__connection.commit()

    def insert(self, table, data):
        values = "'" + "', '".join(data.values()) + "'"
        query = f'INSERT INTO public.{table} ({", ".join(data.keys())}) VALUES ({values}) RETURNING id;'

        self.__cur.execute(query)
        id_of_new_row = self.__cur.fetchone()[0]

        return id_of_new_row

    def update(self, table, id_object, data):

        list_update = []
        for field_name, field_value in data.items():
            list_update.append(f"{field_name}='{field_value}'")
        
        query = f'UPDATE public.{table} SET {", ".join(list_update)} WHERE id = {id_object};'
        self._launch_query(query)

    def delete(self, table, id_object):
        query = f'DELETE FROM public.{table} WHERE id = {id_object};'

        self._launch_query(query)

    def get_by_id(self, table, id_object):
        query = f'SELECT * FROM public.{table} WHERE id = {id_object};'

        table_keys = []
        for schema_key in self.__schema.keys():
            table_keys.append(schema_key)
            
        data = {}
        self._launch_query(query)
        row = self.__cur.fetchone()
        for key, value in enumerate(row):
            data[table_keys[key]] = value

        return data
    
    def get_by_filters(self, table, filters=None):

        list_filters = []

        where = '1=1'
        if filters is not None:
            for field_name, field_value in filters.items():
                list_filters.append(f"{field_name} LIKE '%{field_value}%'")

                where = " AND ".join(list_filters)

        query = f'SELECT * FROM public.{table} WHERE {where};'

        table_keys = []
        for schema_key in self.__schema.keys():
            table_keys.append(schema_key)

        list_data = []
        self._launch_query(query)
        rows = self._cur.fetchall()

        for row in rows:
            data = {}
            for key, value in enumerate(row):
                data[table_keys[key]] = value

            list_data.append(data)

        return list_data
    
    def get_all(self, table):
        return self.get_by_filters(table)