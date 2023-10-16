import unittest
import sys
sys.path.insert(0, '/Users/bradleystevenson/Programs/python-database-wrapper/src/bradleystevenson2015_database')

from database import Database

class TestDatabase(unittest.TestCase):

    def test_initialization(self):
        database = Database("../../databases/python-database-wrapper-test.db", "test-schema.json")
        self.assertEqual(len(database.tables.keys()), 1)

    def test_insert_string_generation(self):
        database = Database("../../databases/python-database-wrapper-test.db", "test-schema.json")
        database.tables['test-table'].append({'column': 'test'})
        self.assertEqual('INSERT INTO test-table (column, id) VALUES ("test", 1)', database.tables['test-table']._generate_insert_string())

    def test_select_string_generation(self):
        database = Database("../../databases/python-database-wrapper-test.db", "test-schema.json")
        self.assertEqual('SELECT column, id FROM test-table', database.tables['test-table']._generate_select_all_string())

    def test_create_tables(self):
        database = Database("../../databases/python-database-wrapper-test.db", "test-schema.json")
        database.create_tables()

if __name__ == '__main__':
    unittest.main()