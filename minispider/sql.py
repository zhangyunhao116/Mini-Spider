#!/usr/bin/env python
import sqlite3
import os
import os.path


class SQL:
    def __init__(self, db_name):
        self.db_name = db_name

    def sql_create_table(self, table_name, var_dict):
        """
            table_name:database table name,str
            var_dict:variable name,dict
        """
        connect = sqlite3.connect(self.db_name)

        # Create SQL text.
        sql_text_head = 'CREATE TABLE %s \n(' % table_name
        sql_text_end = '\n);'
        sql_text = sql_text_head
        temp = ''
        for key in var_dict.keys():
            temp = key
        for k, v in var_dict.items():
            sql_text_body = '\n%s %s,' % (k, v)
            if k == temp:
                sql_text_body = sql_text_body[0:len(sql_text_body) - 1]
            sql_text = sql_text + sql_text_body
        sql_text = sql_text + sql_text_end

        # Try to create table.
        try:
            connect.execute(sql_text)
        except sqlite3.Error:
            pass
        connect.commit()
        connect.close()

    def sql_insert(self, table_name, var_key, var_values):
        """
            table_name:database table name,str
            var_key:database key name,list
            var_values:database values,list
        """
        connect = sqlite3.connect(self.db_name)

        # Change list
        var_key = tuple(var_key)
        var_key_str = str(var_key).replace("'", '')
        var_values = tuple(var_values)
        var_values_str = str(var_values)

        # Delete ',' if just one item.
        if len(var_key) == 1:
            var_key_str = var_key_str.replace(',', '')
        if len(var_values) == 1:
            var_values_str = var_values_str.replace(',', '')

        # Create SQL text
        sql_text = '''INSERT INTO %s %s VALUES %s''' % (table_name, var_key_str, var_values_str)

        # Try to insert values.
        try:
            connect.execute(sql_text)
        except sqlite3.Error:
            pass
        connect.commit()
        connect.close()

    def sql_select(self, table_name, var_key):
        """
            table_name:database table name,str
            var_key:database key name,list
            :return a list ,contains all tuples in database,list.
        """
        connect = sqlite3.connect(self.db_name)

        # Change list.
        var_key = tuple(var_key)
        var_key = str(var_key).replace("'", '')
        # Delete ()
        var_key = str(var_key)[1:len(str(var_key)) - 1]

        # Create SQL text.
        sql_text = 'SELECT %s from %s' % (var_key, table_name)

        try:
            cursor = connect.execute(sql_text)
        except sqlite3.Error:
            return 0

        result = []
        for i in cursor:
            result.append(i)
        connect.close()

        return result


class MiniSpiderSQL(SQL):
    def __init__(self, force_check=False):
        # Self.db_name = 'MiniSpider.db'.
        SQL.__init__(self, db_name=os.path.join(os.getcwd(), 'MiniSpider.db'))
        self.url_table_name = 'url_list'
        self.resource_table_name = 'resource'
        self.set_table_name = 'setup'
        # Force check.
        if force_check:
            if not os.path.isfile(os.path.join(os.getcwd(), self.db_name)):
                raise RuntimeError('Can not find database!')
        # Check database file.if not, initialize database.
        if not os.path.isfile(os.path.join(os.getcwd(), self.db_name)):
            SQL.sql_create_table(self, '%s' % self.url_table_name,
                                 var_dict={'ID': 'integer PRIMARY KEY AUTOINCREMENT', 'URL': 'TEXT UNIQUE',
                                           'STATS': 'INT'})
            SQL.sql_create_table(self, '%s' % self.resource_table_name,
                                 var_dict={'ID': 'integer PRIMARY KEY AUTOINCREMENT', 'URL': 'TEXT UNIQUE',
                                           'STATS': 'INT', 'SOURCE': 'INT'})

    def insert_url(self, url_list):
        var_key = ['URL', 'STATS']

        for index, item in enumerate(url_list):
            SQL.sql_insert(self, self.url_table_name, var_key, [item, 1])

    def insert_resource(self, resource_list, source=None):
        var_key = ['URL', 'STATS', 'SOURCE']

        for index, item in enumerate(resource_list):
            SQL.sql_insert(self, self.resource_table_name, var_key, [item, 1, source])

    def num_available_url(self):
        connect = sqlite3.connect(self.db_name)

        cursor = connect.execute("SELECT COUNT(STATS) FROM %s WHERE STATS=1" % self.url_table_name)
        result = cursor.fetchall()[0][0]

        connect.close()
        return result

    def num_available_resource(self):
        connect = sqlite3.connect(self.db_name)

        cursor = connect.execute("SELECT COUNT(STATS) FROM %s WHERE STATS=1" % self.resource_table_name)
        result = cursor.fetchall()[0][0]

        connect.close()
        return result

    def pop_url(self):
        connect = sqlite3.connect(self.db_name)

        sql_text = "SELECT ID,URL from %s WHERE STATS=1" % self.url_table_name
        cursor = connect.execute(sql_text)

        result = cursor.fetchone()

        connect.close()
        # If pop success, update this url stats.
        if result:
            self.update_url_stats(result[0], 0)
        return result

    def pop_resource(self):
        connect = sqlite3.connect(self.db_name)

        sql_text = "SELECT ID,URL,SOURCE from %s WHERE STATS=1" % self.resource_table_name
        cursor = connect.execute(sql_text)

        result = cursor.fetchone()

        connect.close()
        # If pop success, update this url stats.
        if result:
            self.update_resource_stats(result[0], 0)
        return result

    def update_url_stats(self, url_id, stats):
        connect = sqlite3.connect(self.db_name)

        sql_text = "UPDATE url_list set STATS = %s where ID = %s" % (stats, url_id)

        connect.execute(sql_text)

        connect.commit()
        connect.close()

    def update_resource_stats(self, url_id, stats):
        connect = sqlite3.connect(self.db_name)

        sql_text = "UPDATE resource set STATS = %s where ID = %s" % (stats, url_id)

        connect.execute(sql_text)

        connect.commit()
        connect.close()

    def num_all_url(self):
        connect = sqlite3.connect(self.db_name)

        cursor = connect.execute("SELECT COUNT(ID) FROM %s" % self.url_table_name)
        result = cursor.fetchall()[0][0]

        connect.close()
        return result

    def num_all_resource(self):
        connect = sqlite3.connect(self.db_name)

        cursor = connect.execute("SELECT COUNT(ID) FROM %s" % self.resource_table_name)
        result = cursor.fetchall()[0][0]

        connect.close()
        return result

    def display_all(self):
        s = 'url: %s/%s||resource: %s/%s' % (
            self.num_available_url(), self.num_all_url(), self.num_available_resource(), self.num_all_resource())
        print(s)


if __name__ == '__main__':
    for i in range(100):
        MiniSpiderSQL().update_resource_stats(i, 1)
