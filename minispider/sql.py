#!/usr/bin/env python
import sqlite3
import time
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
        var_values_str = str(var_values).replace("u", '')

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
    def __init__(self):
        # Self.db_name = 'MiniSpider.db'.
        SQL.__init__(self, db_name='MiniSpider.db')
        self.url_table_name = 'url_list'
        self.resource_table_name = 'resource'
        self.set_table_name = 'setup'

        # Check database file.if not, initialize database.
        if not os.path.isfile(os.getcwd() + os.getcwd()[0] + self.db_name):
            SQL.sql_create_table(self, '%s' % self.url_table_name,
                                 var_dict={'ID': 'INT PRIMARY KEY NOT NULL', 'URL': 'TEXT', 'STATS': 'INT'})
            SQL.sql_create_table(self, '%s' % self.resource_table_name,
                                 var_dict={'ID': 'INT PRIMARY KEY NOT NULL', 'URL': 'TEXT', 'STATS': 'INT'})
            SQL.sql_create_table(self, '%s' % self.set_table_name,
                                 var_dict={'flag': 'INT PRIMARY KEY', 'url_flag': 'INT', 'resource_flag': 'INT'})
            self.initialize_flag()

    def initialize_flag(self):
        SQL.sql_insert(self, self.set_table_name, ['flag', 'url_flag', 'resource_flag'], [0, 0, 0])
        connect = sqlite3.connect(self.db_name)
        connect.execute("UPDATE setup SET url_flag = 0 WHERE flag=0")
        connect.execute("UPDATE setup SET resource_flag = 0 WHERE flag=0")
        connect.commit()
        connect.close()

    def read_set(self):
        return SQL.sql_select(self, self.set_table_name, var_key=['url_flag', 'resource_flag'])

    def insert_url(self, url_list):
        var_key = ['ID', 'URL', 'STATS']

        flag = self._read_url_flag()

        for index, item in enumerate(url_list):
            SQL.sql_insert(self, self.url_table_name, var_key, [flag + index, item, 1])

        # Update URL flag.
        self._update_url_flag(flag + len(url_list))

    def insert_resource(self, resource_list):
        var_key = ['ID', 'URL', 'STATS']

        flag = self._read_resource_flag()

        for index, item in enumerate(resource_list):
            SQL.sql_insert(self, self.resource_table_name, var_key, [flag + index, item, 1])

        # Update URL flag.
        self._update_resource_flag(flag + len(resource_list))

    def _num_available_url(self):
        connect = sqlite3.connect(self.db_name)

        cursor = connect.execute("SELECT COUNT(STATS) FROM %s" % self.url_table_name)
        result = cursor.fetchall()[0][0]

        connect.close()
        return result

    def _num_available_resource(self):
        connect = sqlite3.connect(self.db_name)

        cursor = connect.execute("SELECT COUNT(STATS) FROM %s" % self.resource_table_name)
        result = cursor.fetchall()[0][0]

        connect.close()
        return result

    def _update_url_flag(self, url_flag):
        connect = sqlite3.connect(self.db_name)

        sql_text = "UPDATE setup set url_flag = %s where flag=0" % url_flag
        try:
            connect.execute(sql_text)
        except sqlite3.Error:
            return 0

        connect.commit()
        connect.close()

    def _update_resource_flag(self, resource_flag):
        connect = sqlite3.connect(self.db_name)

        sql_text = "UPDATE setup set resource_flag = %s where flag=0" % resource_flag
        try:
            connect.execute(sql_text)
        except sqlite3.Error:
            return 0

        connect.commit()
        connect.close()

    def _read_resource_flag(self):
        connect = sqlite3.connect(self.db_name)

        sql_text = "SELECT resource_flag from setup WHERE flag = 0"
        cursor = connect.execute(sql_text)
        result = cursor.fetchall()[0][0]

        connect.close()
        return result

    def _read_url_flag(self):
        connect = sqlite3.connect(self.db_name)

        sql_text = "SELECT url_flag from setup WHERE flag = 0"
        cursor = connect.execute(sql_text)
        result = cursor.fetchall()[0][0]

        connect.close()
        return result

    def _plus_resource_flag(self):
        flag = int(self._read_resource_flag())
        flag += 1
        self._update_resource_flag(flag)

    def _plus_url_flag(self):
        flag = int(self._read_url_flag())
        flag += 1
        self._update_url_flag(flag)

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

        sql_text = "SELECT ID,URL from %s WHERE STATS=1" % self.resource_table_name
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


if __name__ == '__main__':
    a = time.time()
    o = MiniSpiderSQL()
    # o.insert_url(['sadsadasd', 'wqewqewqewq'])
    # print(o.pop_resource())
    print(time.time() - a)
