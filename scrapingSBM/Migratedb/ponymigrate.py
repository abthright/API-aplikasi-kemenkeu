from pony.orm import *
import pandas as pd

db = Database()

class Provinsi(db.Entity):
    id = PrimaryKey(int, auto=True)
    id_provinsi = Set('Daerah')
    nama_provinsi = Required(str)

class Daerah(db.Entity):
    id_provinsi = Set(Provinsi)
    kota = Required(str)
    kota_asal = Required('RefundPesawat')
    kota_tujuan = Required('RefundPesawat')
    isKota = Required(bool)

class RefundPesawat(db.Entity):
    kota_asal = Set(Daerah, reverse=('kota_asal'))
    kota_tujuan = Set(Daerah, reverse=('kota_tujuan'))
    tiket_bisnis = Required(int)
    tiket_ekonomi = Required(int)

db.bind('sqlite', 'db.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
sql_debug(True)

jobs = ['excel_tiket_pesawat', 'provinsi', 'kota']

for job in jobs :
    df = pd.read_csv(job+'.csv', sep=',')
    print(df)