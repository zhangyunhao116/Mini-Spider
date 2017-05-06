import unittest
import os
import sqlite3
from minispider import MiniSpiderSQL


class TestMiniSpiderSQL(unittest.TestCase):
    def setUp(self):
        """Create database and get abspath."""
        self.SQL = MiniSpiderSQL()
        self.db_name = os.path.join(os.getcwd(), 'MiniSpider.db')

    def test_create(self):
        """Test if MiniSpiderSQL can create a database."""
        check = os.path.isfile(self.db_name)
        self.assertEqual(check, True)

    def test_insert_next_url(self):
        """Test insert data into database table next_url."""
        self.SQL.insert_next_url(['URL_1', 'URL_2', 'URL_3', 'URL_4'])
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            cur.execute('SELECT * FROM next_url')
            result = cur.fetchall()
        standard_result = [(1, 'URL_1', 1), (2, 'URL_2', 1), (3, 'URL_3', 1), (4, 'URL_4', 1)]
        self.assertEqual(result, standard_result, 'insert_next_url error: result is incorrect.')

    def test_insert_resource(self):
        """Test insert data into database table resource."""
        self.SQL.insert_resource(['URL_1', 'URL_2', 'URL_3'], 0)
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            cur.execute('SELECT * FROM resource')
            result = cur.fetchall()
        standard_result = [(1, 'URL_1', 1, 0), (2, 'URL_2', 1, 0), (3, 'URL_3', 1, 0)]
        self.assertEqual(result, standard_result, 'insert_resource error: result is incorrect.')

    def test_update_status(self):
        """Test update status."""
        self.SQL.update_status('next_url', 2, 2)  # id[2] status->2
        self.SQL.update_status('next_url', 0, 3)  # id[3] status->0

        self.SQL.update_status('resource', 2, 2)  # id[2] status->2
        self.SQL.update_status('resource', 0, 3)  # id[3] status->0
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            cur.execute('SELECT * FROM next_url')
            result_next_url = cur.fetchall()
            cur.execute('SELECT * FROM resource')
            result_resource = cur.fetchall()

        result_next_url_standard = [(1, 'URL_1', 1), (2, 'URL_2', 2), (3, 'URL_3', 0), (4, 'URL_4', 1)]
        result_resource_standard = [(1, 'URL_1', 1, 0), (2, 'URL_2', 2, 0), (3, 'URL_3', 0, 0)]
        self.assertEqual(result_next_url, result_next_url_standard)
        self.assertEqual(result_resource, result_resource_standard)

    def test_num(self):
        """Test the number of url & available item."""
        self.assertEqual(self.SQL.num_all('next_url'), 4)
        self.assertEqual(self.SQL.num_all('resource'), 3)

        self.assertEqual(self.SQL.num_available('next_url'), 2)
        self.assertEqual(self.SQL.num_available('resource'), 1)

    def test_pop(self):
        """Test pop."""
        self.assertEqual(self.SQL.pop('next_url'), (1, 'URL_1', 1))
        self.assertEqual(self.SQL.pop('next_url'), (4, 'URL_4', 1))
        self.assertEqual(self.SQL.pop('next_url'), (2, 'URL_2', 2))
        self.assertEqual(self.SQL.pop('next_url'), None)

        self.assertEqual(self.SQL.pop('resource'), (1, 'URL_1', 1, 0))
        self.assertEqual(self.SQL.pop('resource'), (2, 'URL_2', 2, 0))
        self.assertEqual(self.SQL.pop('resource'), None)
        self.assertEqual(self.SQL.pop('resource'), None)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # Add test.
    suite.addTest(TestMiniSpiderSQL('test_create'))
    suite.addTest(TestMiniSpiderSQL('test_insert_next_url'))
    suite.addTest(TestMiniSpiderSQL('test_insert_resource'))
    suite.addTest(TestMiniSpiderSQL('test_update_status'))
    suite.addTest(TestMiniSpiderSQL('test_num'))
    suite.addTest(TestMiniSpiderSQL('test_pop'))

    runner = unittest.TextTestRunner()
    runner.run(suite)

    # tearDown.
    os.remove(os.path.join(os.getcwd(), 'MiniSpider.db'))
