import requests
import json
import pandas as pd
from dump import get_data
from functools import reduce


#initialize connection and run functions
def get_html_doc(url_requested,filter_type,count=0):

  data = list(map(lambda x : get_data(x), filter_type))

  with requests.Session() as s:
      response = s.get('http://monsakti.kemenkeu.go.id')

      try:
        res = list(map(lambda x : get_data_monsakti(s,x,url_requested),data))
      except KeyError: 
          if (count <2):
            count+=1
            print(f'failure happened, attempts restart {count}')
            res = get_html_doc(url_requested,filter_type,count)
          else: return
    
  return res  


#generate response from given request, output > json response that contains data from given request
def get_data_monsakti(s,data,url_requested):
    p = s.post(url=data['login']['login'], data=data['payload'], cookies=data['cookies'], headers=s.headers)
    print(p)

    auth = p.headers['Authorization']
    # An authorised request.
    r = s.post(url_requested,files=data['files'],headers={'Authorization': f"Bearer {auth}"})
    return r.text
    

#generate a df from given dictionary
def get_df_from_dict(data):
    row_marker = 0
    n_rows = len(data)
    n_columns = len(data[0])
    df = pd.DataFrame(columns = range(0,n_columns), index= range(0,n_rows))

    for columns in data : #get all columns
        column_marker = 0
        for column in columns: #for each column do such [x|y|y|y|y] get x column
            content = column['value']
            df.iat[row_marker,column_marker] = content
            column_marker += 1 #[y|x|y|y|y] proceed to next column
        if len(columns) > 0:
            row_marker += 1 #mark for reading next row

    return df.iloc[:,1:] #get all row, get all column except first column bcs the first column is index.


url = 'https://monsakti.kemenkeu.go.id/sitp-monsakti-omspan/pembayaran/sppSpmSp2d'

#DATA CATEGORY SPM SP2D 
#7 = UPLOAD NTT
#8 = CETAK SPM
#11 = ADK SPM
#13 = UPLOAD SP2D

response = get_html_doc(url,[11,13]) #create a list of respose from each requested category

data = list(map(lambda x : json.loads(x)['data']['body'], response)) #create a list of readable json from response

df = list(map(lambda x : get_df_from_dict(x), data)) #create a list of df from data


combined = reduce(lambda x,y : pd.concat([x,y]),df)
combined.to_excel('this.xlsx')





