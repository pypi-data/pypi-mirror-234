import sqlite3
import os
import json
import logging

class Database(object):

    def __init__(self, database_path, schema_path):
        logging.basicConfig(filename="database.log", level=logging.INFO)
        self.conn = sqlite3.connect(database_path)
        self.database_path = database_path
        self.schema_path = schema_path
        self._create_tables()

    def delete_database(self):
        self.conn.close()
        os.remove(self.database_path)
        self.conn = sqlite3.connect(self.database_path)


    def execute_statement(self, execution_string):
        logging.info(f"[DATABASE STATEMENT] [EXECUTE STATEMENT ] {execution_string}")
        self.conn.execute(execution_string)
        self.conn.commit()


    def execute_select_statement(self, select_statement, columns):
        cursor = self.conn.cursor()
        logging.info(f"[DATABASE STATEMENT] [SELECT STATEMENT] {select_statement}")
        cursor.execute(select_statement)
        return_list = []
        for data in cursor.fetchall():
            return_dict = {}
            inx = 0
            for column in columns:
                return_dict[column] = data[inx]
                inx += 1
            return_list.append(return_dict)
        return return_list

    def _create_tables(self):
        schema_file = open(self.schema_path)
        data = json.load(schema_file)
        schema_file.close()
        self.tables = {}
        for table in data['tables']:
            if table['table_type'] == 'table':
                self.tables[table['table_name']] = Table(self, table['table_name'], table['columns'])
            elif table['table_type'] == 'object_table':
                self.tables[table['table_name']] = ObjectTable(self, table['table_name'], table['columns'])
            else:
                raise Exception("No match for table type")
            
    def insert_into_database(self):
        for table_name in self.tables.keys():
            self.tables[table_name].insert_into_table()

    def create_tables(self):
        for table_name in self.tables.keys():
            self.tables[table_name].create_table()

class Table(object):

    def __init__(self, database, table_name, columns):
        self.database = database
        self.table_name = table_name
        self.columns = columns
        self.data = []


    def generate_from_database(self):
        self.data = self.database.execute_select_statement(self._generate_select_all_string(), self.columns)


    def append(self, insert_dict):
        new_dict = {}
        for column in self.columns:
            new_dict[column] = insert_dict[column]
        self.data.append(new_dict)

    def create_table(self):
        try:
            self.database.execute_statement(self._generate_create_table_string())
        except sqlite3.OperationalError:
            print("Cant create table, already exist")

    def insert_into_table(self):
        self.create_table()
        self.database.execute_statement(self._generate_delete_statement())
        if len(self.data) == 0:
            logging.warn("[DATABASE] [INSERT] Not inserting because we have no data")
        else:
            self.database.execute_statement(self._generate_insert_string())


    def find_first_row_with_match(self, search_dict):
        for row in self.data:
            if self._is_row_match(search_dict, row):
                return row
        raise Exception(f"No match for search_dict {str(search_dict)}")


    def _is_row_match(self, search_dict, row):
        for column in search_dict.keys():
            if search_dict[column] != row[column]:
                return False
        return True
    
    def _generate_delete_statement(self):
        return 'DELETE FROM ' + self.table_name

    def _generate_select_all_string(self):
        return_string = 'SELECT '
        for column in self.columns:
            return_string += column + ', '
        return return_string[:-2] + ' FROM ' + self.table_name

    def _generate_insert_string(self):
        insert_string = 'INSERT INTO ' + self.table_name + ' ('
        for column in self.columns:
            insert_string += column + ', '
        insert_string = insert_string[:-2] + ') VALUES '
        for data_dict in self.data:
            insert_string += '('
            for column in self.columns:
                if isinstance(data_dict[column], int):
                    insert_string += str(data_dict[column]) + ', '
                else:
                    insert_string += '"' + data_dict[column] + '", '
            insert_string = insert_string[:-2] +'), '
        return insert_string[:-2]
    
    def _generate_create_table_string(self):
        return_string = 'CREATE TABLE ' + self.table_name + '('
        for column in self.columns:
            return_string += column + ', '
        return_string = return_string[:-2] + ')'
        return return_string


class ObjectTable(Table):


    def __init__(self, database, table_name, columns):
        new_columns = columns.extend(['id'])
        super().__init__(database, table_name, columns)
        self.max_id = 1


    def generate_from_database(self):
        super().generate_from_database()
        self.max_id = self.database.execute_select_statement('SELECT MAX(id) FROM ' + self.table_name, ['id'])[0]['id']


    def append(self, insert_dict):
        insert_dict['id'] = self.max_id
        return_id = self.max_id
        self.max_id += 1
        super().append(insert_dict)
        return return_id


    def get_primary_key_by_search_dict(self, search_dict):
        return self.find_first_row_with_match(search_dict)['id']