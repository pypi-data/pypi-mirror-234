# DB Converter - MySQL to MongoDB | MongoDB to MySQL
![db-converter-mysql-to-mongodb-mongodb-to-mysql](dbconverter_main_img.png)

This project is a python library that facilitates data conversion between MongoDB and MySQL databases.

## Installation

You can use the following command to install the project:

```bash
pip install db-converter
```

## Usage

By using this project, you can convert a specific table from a MySQL database to a MongoDB collection. 

You can also convert a specific collection from a MongoDB database to a MySQL table.

```python
from dbconverter.converter import Converter

# DW bilgileri
DATAWAREHOUSE_HOST = "000.00.0.00"
DATAWAREHOUSE_USER = "admin"
DATAWAREHOUSE_PASSWORD = "password"
port_number = 8080

uri = "mongodb+srv://admin:password!@cluster0.smovknl.mongodb.net/?retryWrites=true&w=majority"
mysql_bilgilerim = {'host': DATAWAREHOUSE_HOST, 'user': DATAWAREHOUSE_USER, 'password': DATAWAREHOUSE_PASSWORD,
                    'port': port_number, 'database': 'your_db_name'}

my_converter = Converter(uri, **mysql_bilgilerim)
my_converter.mysql_to_mongodb('test_table')
```

## Used Libraries
- `pandas`: Used for working with data frames.
- `pymongo`: Used for communicating with MongoDB.
- `pymysql`: Used for connecting to the MySQL database.


## Classes and Methods
`Converter`
- `__init__(self, mongo_uri, **kwargs)`: Creates an instance of Converter by taking MongoDB and MySQL connection information.
- `df_to_json(df) -> list` : Converts a DataFrame into JSON objects. 
- `mysql_to_mongodb(self, table_name=None)` : Converts data from a specific MySQL table to a MongoDB collection.

`MongoDb`
- `__init__(self, uri)`: Establishes a connection to MongoDB.
- `connect(self)` : Connects to the MongoDB server.
- `insert_data(self, json_data, collection)` : Inserts JSON data into the specified collection.
- `get_data(self, collection, query=None)` : Retrieves data from the specified collection.

`MySQLConnector`
- `__init__(self, host, user, password, port_number, database)` : Establishes a connection to MySQL.
- `connect(self)` : Connects to the MySQL database.
`disconnect(self)` : Closes the connection.
`fetch_data(self, table) -> pd.DataFrame` : Fetches data from the specified table and converts it into a DataFrame.

## Licence

This project is licensed under the MIT License. See the LICENSE file for more information.
