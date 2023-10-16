from .converter import dataconverter

# DW bilgieri
DATAWAREHOUSE_HOST = "172.16.5.16"
DATAWAREHOUSE_USER = "bi-admin"
DATAWAREHOUSE_PASSWORD = "Dk5Bnqgj3gEsRz2p"
port_number = 3308


uri = "mongodb+srv://mert:Mert123456!@cluster0.smovknl.mongodb.net/?retryWrites=true&w=majority"
mysql_bilgilerim = {'host': DATAWAREHOUSE_HOST, 'user': DATAWAREHOUSE_USER, 'password': DATAWAREHOUSE_PASSWORD, 'port': port_number, 'database': 'weg_hotel'}

my_converter = dataconverter(uri, **mysql_bilgilerim)
my_converter.mysql_to_mongodb('hotels_pro_b2b_test')

"""
my_converter = Converter(
    mongo_uri="mongodb+srv://admin:password!@cluster0.smovknl.mongodb.net/?retryWrites=true&w=majority",
    host="000.00.0.00",
    user="admin",
    password="password",
    port=8080,
    database="your_db_name"
)

# Migrate data from MySQL to MongoDB
my_converter.mysql_to_mongodb(table_name="test_table")

# Migrate data from MongoDB to MySQL
my_converter.mongodb_to_mysql(collection_name="my_collection")

"""