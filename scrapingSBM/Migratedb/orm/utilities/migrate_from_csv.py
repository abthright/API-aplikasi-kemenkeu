from pony.orm import db_session
import pandas as pd
import os

path = os.chdir('B:/Development/API-aplikasi-kemenkeu/scrapingSBM/Migratedb/data')
df_provinsi = pd.read_csv('provinsi.csv')
df_kota = pd.read_csv('kota_mac.csv', sep=';')
df_sbm_pesawat = pd.read_csv('excel_tiket_pesawat.csv')
df_sbm_taksi = pd.read_csv('excel_taksi.csv')
df_rapat_lk = pd.read_csv('excel_rapat_lk.csv')
df_transport_darat = pd.read_csv('excel_transport_darat.csv')
df_transport_lokal = pd.read_csv('excel_transport_lokal.csv')
df_uang_harian = pd.read_csv('excel_uang_harian.csv')
df_penginapan = pd.read_csv('excel_penginapan.csv')


#how to iterate db in df
#https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas

@db_session()
def update_provinsi(Lokasi, Provinsi):
    for index, row in df_provinsi.iterrows():
        Provinsi(
            id=row['id'],
            nama_provinsi=row['nama_provinsi'],
        )
    generate_kota(Lokasi, Provinsi)

@db_session()
def generate_kota(Lokasi, Provinsi):
    for index, row in df_kota.iterrows():
        sel_provinsi = Provinsi.select(id=row['id_provinsi'])
        for x in sel_provinsi:
            Lokasi(
                kota=row['nama_kota'],
                provinsi_id=x,
                isKota= row['is_kota'],
            )


@db_session()
def generate_sbm_pesawat(Lokasi,SbmPesawat):
    for index, row in df_sbm_pesawat.iterrows():
        sel_kota_asal = Lokasi.select(kota=row['kota_asal'].lower())
        sel_kota_tujuan = Lokasi.select(kota=row['kota_tujuan'].lower())

        for x in sel_kota_asal:
            for y in sel_kota_tujuan:
                SbmPesawat(
                    id_kota_asal = x,
                    id_kota_tujuan = y,
                    provinsi_id_asal = x.provinsi_id,
                    provinsi_id_tujuan = y.provinsi_id,
                    tiket_bisnis = row['satuan biaya tiket pesawat  perjalanan dinas dalam negeri (pp) bisnis'],
                    tiket_ekonomi = row['satuan biaya tiket pesawat  perjalanan dinas dalam negeri (pp) ekonomi'],
                )

#taksi
@db_session()
def generate_sbm_taksi(Lokasi,SbmTaksi):
    for index, row in df_sbm_taksi.iterrows():
        sel_kota = Lokasi.select(kota=row['kota_asal'].lower())

        for x in sel_kota:
            SbmTaksi(
                id_kota = x,
                provinsi_id_asal = x.provinsi_id,
                provinsi_id_tujuan = y.provinsi_id,
                tiket_bisnis = row['satuan biaya tiket pesawat  perjalanan dinas dalam negeri (pp) bisnis'],
                tiket_ekonomi = row['satuan biaya tiket pesawat  perjalanan dinas dalam negeri (pp) ekonomi'],
            )

#penginapan
#rapat lk
#transport darat kabupaten
#transport darat
#transport lokal
#transport uang harian