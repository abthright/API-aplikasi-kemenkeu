from pony import orm
from entities.lokasi import *
from entities.sbm import *
from utilities.migrate_from_csv import *

os.chdir('B:/Development/API-aplikasi-kemenkeu/scrapingSBM/Migratedb/orm')
os.remove('perjadin.db') if os.path.exists('perjadin.db') else None
db = orm.Database()
db.bind(provider='sqlite', filename='perjadin.db', create_db=True)
# if db.exists : db.drop_all_tables(with_all_data=True) #reset


#create entities
provinsi_class = def_provinsi_entitity(db, orm)
lokasi_class = def_lokasi_entitity(db, orm, provinsi_class)
sbm_pesawat_class = def_sbm_pesawat_entitity(db, orm, lokasi_class, provinsi_class)
sbm_taksi_class = def_sbm_taksi_entitity(db, orm, lokasi_class)
sbm_rapat_lk_class = def_sbm_rapat_lk_entitity(db, orm, lokasi_class)
sbm_penginapan_class = def_sbm_penginapan_entitity(db, orm, lokasi_class)
sbm_transport_darat_class = def_sbm_transport_darat_entitity(db, orm, lokasi_class)
sbm_transport_lokal_class = def_sbm_transport_lokal_entitity(db, orm, lokasi_class)
sbm_uang_harian_class = def_sbm_uang_harian_entitity(db, orm, lokasi_class)



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
    
            sp = sbm_pesawat_class.select()
            provinsi_id_1 = x.provinsi_id
            provinsi_id_2 = y.provinsi_id

            #below logic must be used as a string because some python operators arent supported yet, but should work if wrapped as string.
            exp1 = '(sp.provinsi_id_asal == provinsi_id_1 and sp.provinsi_id_tujuan == provinsi_id_2)' #select where this condition met
            exp2 = '(sp.provinsi_id_asal == provinsi_id_1 if (sp.id_kota_asal == x)<1 else sp.id_kota_asal == x ) and (sp.provinsi_id_tujuan == provinsi_id_2 if (sp.id_kota_tujuan == y)<1 else sp.id_kota_tujuan == y)' #check whether this condition returns empty

            this = sbm_pesawat_class.select(f"lambda sp: {exp1} if ({exp2})<1 else {exp2} ")
            res = res + list(this)
    for x in res:
        print(x.tiket_ekonomi)
