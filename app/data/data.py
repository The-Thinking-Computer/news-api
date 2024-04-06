import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        Create a new table in the database.

        Args:
            table_name (str): The name of the table to be created.
            columns (list): A list of tuples, where each tuple contains the column name and its data type.

        Returns:
            None
        """
        columns_str = ', '.join([f"{col[0]} {col[1]}" for col in columns])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")

    def insert(self, table_name, values):
        """
        Insert a new record into the specified table.

        Args:
            table_name (str): The name of the table to insert the record into.
            values (dict): A dictionary containing column names and corresponding values for the new record.

        Returns:
            None
        """
        columns = ', '.join(values.keys())
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(values.values()))

    def exists(self, table_name, column, value):
        """
        Check if a record with the specified value in the specified column exists in the table.

        Args:
            table_name (str): The name of the table to search for the record.
            column (str): The name of the column to search for the value.
            value: The value to search for in the specified column.

        Returns:
            bool: True if the record exists, False otherwise.
        """
        query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {column} = ?)"
        self.cursor.execute(query, (value,))
        return self.cursor.fetchone()[0] == 1

    def commit(self):
        """
        Commit changes to the database.

        Args:
            None

        Returns:
            None
        """
        self.conn.commit()

    def close(self):
        """
        Close the database connection.

        Args:
            None

        Returns:
            None
        """
        self.conn.close()