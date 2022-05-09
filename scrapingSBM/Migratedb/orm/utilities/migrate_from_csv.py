from pony.orm import db_session
import pandas as pd
import os

path = "../data/"
df = pd.read_csv('../data/provinsi.csv')
df2 = pd.read_csv('../data/kota_mac.csv', sep=';')
df3 = pd.read_csv('../data/excel_tiket_pesawat.csv')


#how to iterate db in df
#https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas

@db_session()
def update_provinsi(Lokasi, Provinsi):
    for index, row in df.iterrows():
        Provinsi(
            id=row['id'],
            nama_provinsi=row['nama_provinsi'],
        )
    generate_kota(Lokasi, Provinsi)

@db_session()
def generate_kota(Lokasi, Provinsi):
    for index, row in df2.iterrows():
        sel_provinsi = Provinsi.select(id=row['id_provinsi'])
        for x in sel_provinsi:
            Lokasi(
                kota=row['nama_kota'],
                provinsi_id=x,
                isKota= row['is_kota'],
            )


@db_session()
def generate_sbm_pesawat(Lokasi,SbmPesawat):
    for index, row in df3.iterrows():
        sel_kota_asal = Lokasi.select(kota=row['kota_asal'].lower())
        sel_kota_tujuan = Lokasi.select(kota=row['kota_tujuan'].lower())

        for x in sel_kota_asal:
            for y in sel_kota_tujuan:
                SbmPesawat(
                    kota_asal = x,
                    kota_tujuan = y,
                    provinsi_id_asal = x.provinsi_id,
                    provinsi_id_tujuan = y.provinsi_id,
                    tiket_bisnis = row['satuan biaya tiket pesawat  perjalanan dinas dalam negeri (pp) bisnis'],
                    tiket_ekonomi = row['satuan biaya tiket pesawat  perjalanan dinas dalam negeri (pp) ekonomi'],
                )