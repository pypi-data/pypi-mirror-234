# DB Converter - MySQL to MongoDB

Bu proje, MongoDB ve MySQL veritabanları arasında veri dönüşümü sağlayan bir araçtır.

## Kullanılan Kütüphaneler

- `pandas`: Veri çerçeveleri ile çalışmak için kullanılır.
- `pymongo`: MongoDB ile iletişim kurmak için kullanılır.
- `pymysql`: MySQL veritabanına bağlanmak için kullanılır.

## Kullanım

Bu projeyi kullanarak, MySQL veritabanındaki belirli bir tabloyu MongoDB koleksiyonuna dönüştürebilirsiniz.

```python
from dbconverter.converter import Converter

# DW bilgileri
DATAWAREHOUSE_HOST = "172.16.5.16"
DATAWAREHOUSE_USER = "bi-admin"
DATAWAREHOUSE_PASSWORD = "Dk5Bnqgj3gEsRz2p"
port_number = 3308

uri = "mongodb+srv://mert:Mert123456!@cluster0.smovknl.mongodb.net/?retryWrites=true&w=majority"
mysql_bilgilerim = {'host': DATAWAREHOUSE_HOST, 'user': DATAWAREHOUSE_USER, 'password': DATAWAREHOUSE_PASSWORD,
                    'port': port_number, 'database': 'weg_hotel'}

my_converter = Converter(uri, **mysql_bilgilerim)
my_converter.mysql_to_mongodb('hotels_pro_b2b')
```
## Sınıflar ve Metodlar
`Converter`
- `__init__(self, mongo_uri, **kwargs)`: MongoDB ve MySQL bağlantı bilgilerini alarak bir Converter örneği oluşturur.
- `df_to_json(df) -> list` : Bir DataFrame'i JSON nesnelerine dönüştürür. 
- `mysql_to_mongodb(self, table_name=None)` : Belirli bir MySQL tablosundaki verileri MongoDB koleksiyonuna dönüştürür.

`MongoDb`
- `__init__(self, uri)`: MongoDB bağlantısı oluşturur.
- `connect(self)` : MongoDB sunucusuna bağlanır.
- `insert_data(self, json_data, collection)` : JSON veriyi belirtilen koleksiyona ekler.
- `get_data(self, collection, query=None)` : Belirtilen koleksiyondaki verileri alır.

`MySQLConnector`
- `__init__(self, host, user, password, port_number, database)` : MySQL bağlantısı oluşturur.
- `connect(self)` : MySQL veritabanına bağlanır.
`disconnect(self)` : Bağlantıyı kapatır.
`fetch_data(self, table) -> pd.DataFrame` : Belirtilen tablodan veri çeker ve bir DataFrame'e dönüştürür.


## Kurulum

Proje kütüphanelerini yüklemek için aşağıdaki komutu kullanabilirsiniz:

```bash
pip install pandas pymongo pymysql
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına göz atın.
