
def def_provinsi_entitity(db, orm):

    class Provinsi(db.Entity):
            __table__ = 'provinsi'
            id = orm.PrimaryKey(int, auto=True)
            nama_provinsi = orm.Required(str, unique=True)
            all_kota = orm.Set('Lokasi')
            all_kota_asal_sbm_pesawat = orm.Set('SbmPesawat', reverse='provinsi_id_asal')
            all_kota_tujuan_sbm_pesawat = orm.Set('SbmPesawat', reverse='provinsi_id_tujuan')

    
    return Provinsi

def def_lokasi_entitity(db, orm, Provinsi):

    class Lokasi(db.Entity):
            __table__ = 'lokasi'
            id = orm.PrimaryKey(int, auto=True)
            kota = orm.Required(str, unique=False)
            isKota = orm.Required(bool)
            provinsi_id = orm.Required(Provinsi)
            all_kota_asal = orm.Set('SbmPesawat', reverse='kota_asal')
            all_kota_tujuan = orm.Set('SbmPesawat', reverse='kota_tujuan')
            all_kota_taksi = orm.Set('SbmTaksi')

    return Lokasi


