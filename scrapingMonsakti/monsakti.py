import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import logging
from dump import get_data


def get_html_doc(url_requested,filter_type):

  data = get_data(filter_type)
  logging.basicConfig(filename='monsakti.log', level=logging.DEBUG,
                        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

  with requests.Session() as s:
      response = s.get('http://monsakti.kemenkeu.go.id')
      cookies = s.cookies.get_dict()
      p = s.post(url=data['login']['login'], data=data['payload'], cookies=cookies, headers=data['headers'])
      auth = p.headers['Authorization']

      # An authorised request.
      r = s.post(url_requested,files=data['files'],headers={'Authorization': f"Bearer {auth}"})
      return r.text

def get_df_from_dict(data):
    row_marker = 0
    n_rows = len(data)
    n_columns = len(data[0])
    df = pd.DataFrame(columns = range(0,n_columns), index= range(0,n_rows))

    for columns in data :
        column_marker = 0
        for column in columns:
            content = column['value']
            df.iat[row_marker,column_marker] = content
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1

    return df.iloc[:,1:]


url = 'https://monsakti.kemenkeu.go.id/sitp-monsakti-omspan/pembayaran/sppSpmSp2d'

data = json.loads(get_html_doc(url,11))['data']['body']
data2 = json.loads(get_html_doc(url,13))['data']['body']

df1 = get_df_from_dict(data)
df2 = get_df_from_dict(data2)

print(data)

combined = pd.concat([df1,df2])
(combined.to_excel('this.xlsx'))





