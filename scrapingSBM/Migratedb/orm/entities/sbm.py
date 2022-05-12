
def def_sbm_pesawat_entitity(db, orm, Lokasi, Provinsi):

    class SbmPesawat(db.Entity):
        __table__ = 'sbm_pesawat'
        id = orm.PrimaryKey(int, auto=True)
        id_kota_asal = orm.Required(Lokasi)
        id_kota_tujuan = orm.Required(Lokasi)
        provinsi_id_asal = orm.Required(Provinsi)
        provinsi_id_tujuan = orm.Required(Provinsi)
        tiket_bisnis = orm.Required(int)
        tiket_ekonomi = orm.Required(int)

    return SbmPesawat
    

def def_sbm_taksi_entitity(db, orm, Lokasi):

    class SbmTaksi(db.Entity):
        __table__ = 'sbm_taksi'
        id = orm.PrimaryKey(int, auto=True)
        id_kota = orm.Required(Lokasi)
        maks_taksi = orm.Required(int)

    return SbmTaksi

def def_sbm_rapat_lk_entitity(db, orm, Lokasi):

    class SbmRapatLk(db.Entity):
        __table__ = 'sbm_rapat_lk'
        id = orm.PrimaryKey(int, auto=True)
        id_kota = orm.Required(Lokasi)
        maks_fullboard_dalam_kota = orm.Required(int)
        maks_fullboard_luar_kota = orm.Required(int)    
        maks_sbm_rapat_lk_lain = orm.Required(int)

    return SbmRapatLk

#penginapan
def def_sbm_penginapan_entitity(db, orm, Lokasi):

    class SbmPenginapan(db.Entity):
        __table__ = 'sbm_penginapan'
        id = orm.PrimaryKey(int, auto=True)
        id_kota = orm.Required(Lokasi)
        maks_kelas_a = orm.Required(int)
        maks_kelas_b = orm.Required(int)    
        maks_s_kelas_c = orm.Required(int)
        maks_s_kelas_d = orm.Required(int)

    return SbmPenginapan

#transportdaratkabupaten
def def_sbm_transport_dalam_kota_entitity(db, orm, Lokasi):

    class SbmTransportDalamKota(db.Entity):
        __table__ = 'transport_dalam_kota'
        id = orm.PrimaryKey(int, auto=True)
        maks_transport_dalam_kota_pp = orm.Required(int)

    return SbmTransportDalamKota

#transportdarat
def def_sbm_transport_darat_entitity(db, orm, Lokasi):

    class SbmTransportDarat(db.Entity):
        __table__ = 'transport_darat'
        id = orm.PrimaryKey(int, auto=True)
        id_kota_asal = orm.Required(Lokasi)
        id_kota_tujuan = orm.Required(Lokasi)
        # is_kota = orm.Required(bool) > ga perlu ini, di sesuaikan aja pas insert data
        maks_transport_darat = orm.Required(int)

    return SbmTransportDarat

#transportlokal
def def_sbm_transport_lokal_entitity(db, orm, Lokasi):

    class SbmTransportLokal(db.Entity):
        __table__ = 'transport_lokal'
        id = orm.PrimaryKey(int, auto=True)
        id_kota_asal = orm.Required(Lokasi)
        id_kota_tujuan = orm.Required(Lokasi)
        # is_kota = orm.Required(bool) > ga perlu ini, di sesuaikan aja pas insert data
        maks_transport_lokal = orm.Required(int)

    return SbmTransportLokal

#uangharian
def def_sbm_uang_harian_entitity(db, orm, Lokasi):

    class SbmUangHarian(db.Entity):
        __table__ = 'uang_harian'
        id = orm.PrimaryKey(int, auto=True)
        id_kota = orm.Required(Lokasi)
        maks_luar_kota = orm.Required(int)
        maks_dalam_kota = orm.Required(int)    
        maks_diklat = orm.Required(int)

    return SbmUangHarian