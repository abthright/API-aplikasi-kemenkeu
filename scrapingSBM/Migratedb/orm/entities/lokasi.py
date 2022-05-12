
#relate to provinsi : 
        # penginapan
        # uangharian
        # rapatlk 

#relate to kota : 
        # pesawat pp ~
        # transportdarat pp~
        # taksi~
        # transportlokal~



def def_provinsi_entitity(db, orm):

    class Provinsi(db.Entity):
            __table__ = 'provinsi'
            id = orm.PrimaryKey(int, auto=True)
            nama_provinsi = orm.Required(str, unique=True)
            all_kota = orm.Set('Lokasi')
            all_provinsi_asal_sbm_pesawat = orm.Set('SbmPesawat', reverse='provinsi_id_asal')
            all_provinsi_tujuan_sbm_pesawat = orm.Set('SbmPesawat', reverse='provinsi_id_tujuan')
            
    
    return Provinsi

def def_lokasi_entitity(db, orm, Provinsi):

    class Lokasi(db.Entity):
            __table__ = 'lokasi'
            id = orm.PrimaryKey(int, auto=True)
            kota = orm.Required(str, unique=False)
            isKota = orm.Required(bool)
            provinsi_id = orm.Required(Provinsi)
            all_kota_asal_pesawat = orm.Set('SbmPesawat', reverse='id_kota_asal')
            all_kota_tujuan_pesawat = orm.Set('SbmPesawat', reverse='id_kota_tujuan')
            all_kota_taksi = orm.Set('SbmTaksi')
            all_kota_rapat_lk = orm.Set('SbmRapatLk')
            all_kota_asal_transport_darat = orm.Set('SbmTransportDarat', reverse='id_kota_asal')
            all_kota_tujuan_transport_darat = orm.Set('SbmTransportDarat', reverse='id_kota_tujuan')
            all_kota_penginapan = orm.Set('SbmPenginapan')
            all_kota_transport_lokal_asal = orm.Set('SbmTransportLokal', reverse='id_kota_asal')
            all_kota_transport_lokal_tujuan = orm.Set('SbmTransportLokal', reverse='id_kota_tujuan')
            all_kota_uang_harian = orm.Set('SbmUangHarian')

    return Lokasi


