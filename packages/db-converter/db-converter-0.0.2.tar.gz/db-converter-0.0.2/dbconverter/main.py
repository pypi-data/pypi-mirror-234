from converter import Converter

# DW bilgieri
DATAWAREHOUSE_HOST = "172.16.5.16"
DATAWAREHOUSE_USER = "bi-admin"
DATAWAREHOUSE_PASSWORD = "Dk5Bnqgj3gEsRz2p"
port_number = 3308


uri = "mongodb+srv://mert:Mert123456!@cluster0.smovknl.mongodb.net/?retryWrites=true&w=majority"
mysql_bilgilerim = {'host': DATAWAREHOUSE_HOST, 'user': DATAWAREHOUSE_USER, 'password': DATAWAREHOUSE_PASSWORD, 'port': port_number, 'database': 'weg_hotel'}

my_converter = Converter(uri, **mysql_bilgilerim)
my_converter.mysql_to_mongodb('hotels_pro_b2b_test')
#my_converter.mongodb_to_mysql('hotels_pro_b2b_test')


