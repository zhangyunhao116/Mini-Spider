#!/usr/bin/env python
import sqlite3
import os
import os.path


class MiniSpiderSQL:
    """Allows you accessing the Mini-Spider database using a one-line command."""

    def __init__(self):
        # Database filename is 'MiniSpider.db'.
        self.db_name = os.path.join(os.getcwd(), 'MiniSpider.db')
        self.url_table_name = 'next_url'
        self.resource_table_name = 'resource'

        # Check database file.if it doesn't exist, initialize database.
        if not os.path.isfile(self.db_name):
            with sqlite3.connect(self.db_name) as c:
                cur = c.cursor()
                cur.executescript("""
                            CREATE TABLE next_url(
                            id      INTEGER PRIMARY KEY AUTOINCREMENT,
                            url     TEXT UNIQUE,
                            status  INT
                            );

                            CREATE TABLE resource(
                            id      INTEGER PRIMARY KEY AUTOINCREMENT,
                            url     TEXT UNIQUE,
                            status  INT,
                            source  INT
                            );""")

    def insert_next_url(self, url_list):
        """Insert a list of URL into database table next_url."""
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            for i in url_list:
                try:
                    cur.execute("""INSERT INTO next_url (url,status) VALUES (?,?)""", (i, 1))
                except sqlite3.IntegrityError:
                    # This error raised by repetition.
                    pass

    def insert_resource(self, resource_list, source):
        """Insert a list of URL into database table resource."""
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            for i in resource_list:
                try:
                    cur.execute("""INSERT INTO resource (url,status,source) VALUES (?,?,?)""", (i, 1, source))
                except sqlite3.IntegrityError:
                    # This error raised by repetition.
                    pass

    def num_available(self, table_name):
        """Return the number of available URL in table_name"""
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            if table_name == 'next_url':
                cur.execute("""SELECT COUNT(STATUS) FROM next_url WHERE status >= 1""")
            elif table_name == 'resource':
                cur.execute("""SELECT COUNT(STATUS) FROM resource WHERE status >= 1""")
            num = cur.fetchone()[0]
        return num

    def num_all(self, table_name):
        """Return the number of all data item in table_name"""
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            if table_name == 'next_url':
                cur.execute("""SELECT COUNT(id) FROM next_url""")
            elif table_name == 'resource':
                cur.execute("""SELECT COUNT(id) FROM resource""")
            num = cur.fetchone()[0]
        return num

    def pop(self, table_name):
        """pop a row from table_name."""
        result = None
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            if table_name == 'next_url':
                cur.execute("""SELECT * FROM next_url WHERE status != 0 ORDER BY status ASC """)
                result = cur.fetchone()
                # Update this data status because it has been used.
                if result:
                    cur.execute("""UPDATE next_url SET status = ? WHERE id = ?""", (0, result[0]))
            elif table_name == 'resource':
                cur.execute("""SELECT * FROM resource WHERE status != 0 ORDER BY status ASC """)
                result = cur.fetchone()
                # Update this data status because it has been used.
                if result:
                    cur.execute("""UPDATE resource SET status = ? WHERE id = ?""", (0, result[0]))

        return result

    def update_status(self, table_name, status, id):
        """Update the status of data."""
        info = (status, id)
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            if table_name == 'next_url':
                cur.execute("""UPDATE next_url SET status = ? WHERE id = ?""", info)
            elif table_name == 'resource':
                cur.execute("""UPDATE resource SET status = ? WHERE id = ?""", info)
            else:
                raise Exception('MiniSpiderSQL error:update_status table_name error.')

    def print_all(self):
        """Print the number of available URL and all URL from the entire database."""
        text = 'url: %s/%s||resource: %s/%s' % (
            self.num_available('next_url'), self.num_all('next_url'), self.num_available('resource'),
            self.num_all('resource'))
        print(text)

    def list_url(self, table_name, num):
        """Print all the URL form table_name."""
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            if table_name == 'next_url':
                cur.execute("""SELECT url,status FROM next_url ORDER BY id""")
            elif table_name == 'resource':
                cur.execute("""SELECT url,status FROM resource ORDER BY id""")
            result = cur.fetchall()

        temp = ''
        for index, item in enumerate(result, 1):
            if index < num:
                if item[1] == 0:
                    temp = 'Used'
                elif item[1] == 1:
                    temp = 'New'
                elif item[1] >= 2:
                    temp = 'Exception'
                print('[%s:%s]%s' % (index, temp, item[0]))

    def export_txt(self, table_name, file_name):
        """Export all the URL from table_name to a txt file."""
        with sqlite3.connect(self.db_name) as c:
            cur = c.cursor()
            if table_name == 'next_url':
                cur.execute("""SELECT url FROM next_url ORDER BY id""")
            elif table_name == 'resource':
                cur.execute("""SELECT url FROM resource ORDER BY id""")
            result = cur.fetchall()

        # Add '\n'.
        result = list(map(lambda x: x[0] + '\n', result))

        # Export txt file.
        with open(os.path.join(os.getcwd(), file_name), mode='w') as f:
            f.writelines(result)

    def import_txt(self, table_name, file_name):
        """Import a tuple of URL from txt file."""
        with open(os.path.join(os.getcwd(), file_name), mode='r') as f:
            result = f.readlines()

        # May have problem here.MARK
        result = tuple(map(lambda x: x[:-1], result))

        if table_name == 'next_url':
            self.insert_next_url(result)
        elif table_name == 'resource':
            self.insert_resource(result, 'user')

    def reset(self, table_name):
        """Reset all the data that reside in table_name status to 1 ."""
        if table_name == 'u':
            for i in range(1, self.num_all('next_url') + 1):
                self.update_status('next_url', 1, i)
        elif table_name == 'u':
            for i in range(1, self.num_all('resource') + 1):
                self.update_status('resource', 1, i)


if __name__ == '__main__':
    pass
