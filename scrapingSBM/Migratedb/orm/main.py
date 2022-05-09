from pony import orm
from entities.lokasi import *
from entities.sbm import *
from utilities.migrate_from_csv import *


os.remove('perjadin.db') if os.path.exists('perjadin.db') else None
db = orm.Database()
db.bind(provider='sqlite', filename='perjadin.db', create_db=True)
# if db.exists : db.drop_all_tables(with_all_data=True) #reset


#create entities
provinsi_class = def_provinsi_entitity(db, orm)
lokasi_class = def_lokasi_entitity(db, orm, provinsi_class)
sbm_pesawat_class = def_sbm_pesawat_entitity(db, orm, lokasi_class, provinsi_class)
sbm_taksi_class = def_sbm_taksi_entitity(db, orm, lokasi_class)

db.generate_mapping(create_tables=True)
# orm.sql_debug(True)


#execute utilities
update_provinsi(lokasi_class, provinsi_class)
generate_sbm_pesawat(lokasi_class,sbm_pesawat_class)

with orm.db_session:
    asal = lokasi_class.select(kota="jakarta")
    tujuan = lokasi_class.select(kota="nganjuk")

    res = []
    for x in asal: 
        for y in tujuan:
            # this = sbm_pesawat_class.select(lambda sp: (sp.provinsi_id_asal == x.provinsi_id if (sp.kota_asal == x)<1 else sp.kota_asal == x ) and (sp.provinsi_id_tujuan == y.provinsi_id if (sp.kota_tujuan == y)<1 else sp.kota_tujuan == y ))

            ###defining lambda
            sp = sbm_pesawat_class.select()
            provinsi_id_1 = x.provinsi_id
            provinsi_id_2 = y.provinsi_id

            exp1 = '(sp.provinsi_id_asal == provinsi_id_1 and sp.provinsi_id_tujuan == provinsi_id_2)'
            exp2 = '(sp.provinsi_id_asal == provinsi_id_1 if (sp.kota_asal == x)<1 else sp.kota_asal == x ) and (sp.provinsi_id_tujuan == provinsi_id_2 if (sp.kota_tujuan == y)<1 else sp.kota_tujuan == y)'

            this = sbm_pesawat_class.select(f"lambda sp: {exp1} if ({exp2})<1 else {exp2} ")
            res = res + list(this)
    for x in res:
        print(x.tiket_ekonomi)

# class Provinsi(db.Entity):
#     id = orm.PrimaryKey(int, auto=True)
#     id_provinsi = orm.Set('Daerah')
#     nama_provinsi = orm.Required(str)

# class Daerah(db.Entity):
#     id_provinsi = orm.Set(Provinsi)
#     kota = orm.Required(str)
#     kota_asal = orm.Required('RefundPesawat')
#     kota_tujuan = orm.Required('RefundPesawat')
#     isKota = orm.Required(bool)

# class RefundPesawat(db.Entity):
#     kota_asal = orm.Set(Daerah, reverse=('kota_asal'))
#     kota_tujuan = orm.Set(Daerah, reverse=('kota_tujuan'))
#     tiket_bisnis = orm.Required(int)
#     tiket_ekonomi = orm.Required(int)


# jobs = ['excel_tiket_pesawat', 'provinsi', 'kota']

# for job in jobs :
#     df = pd.read_csv(job+'.csv', sep=',')
#     print(df)