from converter import converter

# DW bilgieri
DATAWAREHOUSE_HOST = "000.00.0.00"
DATAWAREHOUSE_USER = "admin"
DATAWAREHOUSE_PASSWORD = "password"
port_number = 8080


uri = "mongodb+srv://admin:password!@cluster0.smovknl.mongodb.net/?retryWrites=true&w=majority"
mysql_bilgilerim = {'host': DATAWAREHOUSE_HOST, 'user': DATAWAREHOUSE_USER, 'password': DATAWAREHOUSE_PASSWORD, 'port': port_number, 'database': 'your_db_name'}

my_converter = converter(uri, **mysql_bilgilerim)
my_converter.mysql_to_mongodb('test_table')
my_converter.mongodb_to_mysql('test_collection')


