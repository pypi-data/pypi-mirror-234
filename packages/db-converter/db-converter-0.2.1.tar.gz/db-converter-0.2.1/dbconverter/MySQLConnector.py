import pymysql
import datetime
import pandas as pd


class MySQLConnector:
    def __init__(self, host, user, password, port_number, database):
        self.host = host
        self.user = user
        self.password = password
        self.port_number = port_number
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port_number,
            database=self.database
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def get_data(self, table) -> pd.DataFrame:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        # Sütun isimlerini al
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=columns)

        for col in df.columns:
            if df[col].dtype == 'object' and isinstance(df[col].values[0], datetime.date):
                df[col] = df[col].astype(str)

        self.disconnect()
        return df

    def insert_data(self, df, table_name):
        """

        Dataframe istenilen SQL tablosuna insert eder.

        """
        print("SQL Conn kuruluyor...")

        self.connect()
        if '_id' in df.columns:
            df = df.drop('_id', axis=1)
        values = ','.join(['%s'] * len(df.columns))

        sql = f"INSERT INTO {table_name} ({','.join(df.columns)}) VALUES ({values})"
        # Verileri tuple olarak dönüştürme
        data = [tuple(row) for row in df.values]

        # INSERT sorgusunu çalıştırma
        with self.connection.cursor() as cursor:
            cursor.executemany(sql, data)
            self.connection.commit()

        # Close the cursor and connection
        cursor.close()
        self.disconnect()

    def check_table_name(self, table_name):
        self.connect()
        # Bağlantı üzerinden bir cursor oluştur
        cursor = self.connection.cursor()

        # SQL sorgusu ile tablonun var olup olmadığını kontrol et
        query = f"SHOW TABLES LIKE '{table_name}'"
        cursor.execute(query)

        # fetchone metodu ile sonuçları al
        result = cursor.fetchone()

        # Bağlantıyı kapat
        cursor.close()
        self.connection.close()

        # Sonuçları kontrol et
        if result:
            print(f"'{table_name}' tablosu mevcut.")
            return True
        else:
            print(f"'{table_name}' tablosu mevcut değil.")
            return False
        self.disconnect()

    def create_table(self, table_name, df):
        self.connect()

        if '_id' in df.columns:
            df = df.drop('_id', axis=1)

        # Veri tiplerini inceleyin
        data_types = df.dtypes

        # MySQL veri tiplerini belirle
        mysql_data_types = {
            'int64': 'INT',
            'float64': 'FLOAT',
            'object': 'VARCHAR(255)', # Örnek olarak VARCHAR(255) seçildi, ihtiyaca göre değiştirilebilir.
            'datetime64[ns]': 'DATETIME',
        }

        # Bağlantı üzerinden bir cursor oluştur
        cursor = self.connection.cursor()

        # Tablo adı ve sütunlar
        columns = ', '.join([f'{col} {mysql_data_types[str(data_types[col])]}'
                             for col in df.columns])

        # SQL sorgusu ile tabloyu oluştur
        create_table_query = f"CREATE TABLE {table_name} ({columns})"
        cursor.execute(create_table_query)

        cursor.close()
        self.disconnect()
