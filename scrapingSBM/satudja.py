
# docs https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/
# docs https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find

from bs4 import BeautifulSoup
import pandas as pd
import requests
from functools import reduce


#main functions
def parse_html_table(name,table):
    column_names = get_column_name(table)
    table_size = count_column_row_num(table,column_names)
    return create_df(name,table_size,column_names)

#component functions

def get_html_doc(url_requested):
  payload = {
    'iduser': 418139,
    'password': 'Deputitiga',
    'thang': 2022,
  }

  login = {
    'login' : 'https://satudja.kemenkeu.go.id/login?q=faf9b',
  }

  with requests.Session() as s:
      p = s.post(login['login'], data=payload)
      # print the html returned or something more intelligent to see if it's a successful login page.

      # An authorised request.
      r = s.get(url_requested)
      return r.text

def get_html_table_name(table):
  return table.find_all('tr', {'class':'Sub'})[0].find('td').get_text()

def get_column_name(table):
  column_names = []
  for row in table.find_all("thead"):
    # Handle column names if we find them
    th_tags = row.find_all('th') 
    if len(th_tags) > 0 and len(column_names) == 0:
        for th in th_tags:
            column_names.append(th.get_text().strip().lower())
  return(column_names)

def count_column_row_num(table,column_names):
    n_columns = 0
    n_rows=0

    # Find number of rows and columns
    # we also find the column titles if we can
    for row in table.find_all("tr", {'class':'All'}):
        
        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows+=1
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)


    # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    return {'n_columns':n_columns,'n_rows':n_rows}

def create_df(name,table_size,column_names):
    print(name)
    columns = column_names + ['sub_category'] if len(column_names) > 0 else range(0,table_size['n_columns']+1)
    df = pd.DataFrame(columns = columns, index= range(0,table_size['n_rows']))
    sub_category_list = []
    empty_df = pd.DataFrame(columns = columns, index= range(0,table_size['n_rows']))

    row_marker = 0
    counter = 0
    n_loop_size = len(table.find_all('tr'))
    sub_category = ''
    skip_title_counter = 0
    limit_counter = 1

    for row in table.find_all("tr"):
        counter += 1

        is_sub_category = row.find_next('tr')['class'][0] == 'All' if counter!=n_loop_size else False
        is_sub_class = row['class'][0] == 'Sub' if row.has_attr('class') else False
        is_main_category = row.find_next('tr')['class'][0] == 'Sub' if counter!=n_loop_size else False
        is_all_class = row['class'][0] == 'All' if row.has_attr('class') else False

        #detect subclass
        if is_sub_class and is_sub_category:   
          sub_category = row.find_next('b').get_text().strip().lower()
          sub_category_list.append(sub_category)

        #exclude multiple main class
        elif is_sub_class and is_main_category :
          skip_title_counter+=1
          is_anomaly = row.find_next('tr').find_next('tr')['class'][0] == 'Sub' if counter!=n_loop_size-1 else False
          if is_anomaly:limit_counter = 3
          if skip_title_counter>limit_counter: 
            df = df[:row_marker]
            break
        
        #input all subclass item
        if is_all_class: 
          column_marker = 0
          columns = row.find_all('td')
          for column in columns:
              content = int(column.get_text().strip().replace('.','')) if column.get_text().strip().strip('.').replace('.','').isnumeric() else column.get_text().strip()
              df.iat[row_marker,column_marker] = content
              df.sub_category[row_marker] = sub_category
              column_marker += 1
          if len(columns) > 0:
              row_marker += 1

    #mergedf
    method_1 = ['tiket pesawat','transport lokal','uh perjadin','uang rapat rlk','penginapan']
    if name in method_1 : df=merge_sub_pdf(sub_category_list,df)

    #destructuring assignment for pandas split
    #https://datascienceparichay.com/article/pandas-split-column-by-delimiter/
    clean_uraian = ['tiket pesawat','transport lokal','transport darat'] 
    if name in clean_uraian: 
      df.reset_index(inplace=True)
      
      if name in ['tiket pesawat','transport darat'] : df[['kota_asal','kota_tujuan','hapus']] = df.uraian.str.replace(' - ','-').str.split('-',expand=True)
      else : df[['kota_asal','kota_tujuan']] = df.uraian.str.replace(' - ','-').str.split('-',expand=True)
      df.drop('uraian',axis=1,inplace=True)
      # https://stackoverflow.com/questions/13148429/how-to-change-the-order-of-dataframe-columns
      # cols = df.columns.tolist()
      # last two items in the array cols[-2:]
      # everything except the last two items  cols[:-2]
      # cols = cols[-3:] + cols[:-3]
      # df = df[cols]
    
    if name == 'transport lokal' : 
      df[['kota_kabupaten','kota_tujuan']] = df.kota_tujuan.str.replace('Kabupaten ','kabupaten,').str.replace('Kota ','kota,').str.split(',',expand=True)
    if name == 'transport darat' : 
      try:
        df[['kota_kabupaten','kota_tujuan','hapus']] = df.kota_tujuan.str.replace('Kab. ','kabupaten,').str.replace('Kota ','kota,').str.split(',',expand=True)
        #[[[[[[kemarin]]]]]] ini malah program tetep jalan tapi value error, udh di save excel nya
      except ValueError : print(df.kota_tujuan.str.replace('Kab. ','kabupaten,').str.replace('Kota ','kota,').str.split(',',expand=True).head(5))

    print(df.columns)
    
    df.replace({
      'R I A U' : 'RIAU',
      'J A M B I' : 'JAMBI',
      'B A L I' : 'BALI',
      'P A P U A' : 'PAPUA',      
    }, inplace=True)

    df.reset_index(inplace=True)
    return df.drop(['level_0','index','satuan','sub_category','hapus'],axis=1,errors='ignore')

def merge_sub_pdf(sub_category_list,df):
  grouped = df.groupby(df.sub_category)
  dfList= list(map(lambda x: grouped.get_group(x),sub_category_list))
  dfs = [df.set_index('uraian') for df in dfList]
  df = pd.concat(dfs, axis=1).drop(['satuan','sub_category'], axis=1)

  try:
    df.set_axis(sub_category_list, axis=1, inplace=True)
  except ValueError: pass

  return df

login = {
  'uh perjadin' : 'https://satudja.kemenkeu.go.id/referensi?q=0558b&kode=128',
  'taksi' : 'https://satudja.kemenkeu.go.id/referensi?q=0558b&kode=217',
  'tiket pesawat' : 'https://satudja.kemenkeu.go.id/referensi?q=0558b&kode=218',
  'transport darat' : 'https://satudja.kemenkeu.go.id/referensi?q=0558b&kode=201',
  'narasumber' : 'https://satudja.kemenkeu.go.id/referensi?q=0558b&kode=112',
  'penginapan' : 'https://satudja.kemenkeu.go.id/referensi?q=0558b&kode=130',
  'transport lokal' : 'https://satudja.kemenkeu.go.id/referensi?q=0558b&kode=202',
  'lokal dalam kota/kabupaten' : 'https://satudja.kemenkeu.go.id/referensi?q=0558b&kode=203',
  'uang rapat rlk' : 'https://satudja.kemenkeu.go.id/referensi?q=0558b&kode=131',
}

for name,url_requested in login.items():

  soup = BeautifulSoup(get_html_doc(url_requested), 'html.parser')
  table = soup.find_all('table')[0]

  df = parse_html_table(name,table=table)
  df.to_excel(get_html_table_name(table).strip().replace('/',' atau ').replace('\n',' ')+".xlsx")

