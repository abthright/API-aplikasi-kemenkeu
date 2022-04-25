import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def get_html_doc(url_requested,filter_type):
  payload = {
    'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'userid': 418139,
    'password': 65206396,
  }
  cookies = {
      'PHPSESSID' : '5647ce3711be9b6967a2cda41716819a',
      'dp__v' : '27305865-HFP94ZWG-SP0E9534-4M7ZLH-TFE',
      'cookiesession1' : '678B28FEGHIJKLMNOPRSTUV01234A9C7',
  }
  login = {
    'login' : 'https://monsakti.kemenkeu.go.id/sitp-monsakti-omspan/auth/requestJWTToken',
  }

  files = {
      'submit_file' : (None,''),
      'tgl_awal' : (None,'01-01-2022'),
      'tgl_akhir' : (None,'19-04-2022'),
      'status' : (None,f'SPM_STS_DATA_{filter_type}'),
  }

  headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
  }

  with requests.Session() as s:
      response = s.get('http://monsakti.kemenkeu.go.id')
      cookies = s.cookies.get_dict()
      # cookies = cookies
      p = s.post(login['login'], data=payload, cookies=cookies, headers=headers)
      # print the html returned or something more intelligent to see if it's a successful login page.

      auth = p.headers['Authorization']
      # An authorised request.
    #   r = s.get(url_requested,cookies=cookies,headers={'Authorization': f"Bearer {auth}"})
    #   postSpmData = s.post(url_requested, data=data, headers={'Authorization': f"Bearer {auth}"})

      r = s.post(url_requested,files=files,headers={'Authorization': f"Bearer {auth}"})
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

# combined = pd.concat([df1,df2])
# (combined.to_excel('this.xlsx'))





