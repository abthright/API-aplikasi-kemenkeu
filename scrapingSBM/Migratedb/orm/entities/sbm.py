
def def_sbm_pesawat_entitity(db, orm, Lokasi, Provinsi):

    class SbmPesawat(db.Entity):
        __table__ = 'sbm_pesawat'
        id = orm.PrimaryKey(int, auto=True)
        kota_asal = orm.Required(Lokasi)
        kota_tujuan = orm.Required(Lokasi)
        provinsi_id_asal = orm.Required(Provinsi)
        provinsi_id_tujuan = orm.Required(Provinsi)
        tiket_bisnis = orm.Required(int)
        tiket_ekonomi = orm.Required(int)

    return SbmPesawat
    

def def_sbm_taksi_entitity(db, orm, Lokasi):

    class SbmTaksi(db.Entity):
        __table__ = 'sbm_Taksi'
        id = orm.PrimaryKey(int, auto=True)
        di_kota = orm.Required(Lokasi)
        maks_taksi = orm.Required(int)

    return SbmTaksi
