import json
from datetime import date


def get_data(filter_type):

    today = date.today().strftime("%d-%m-%Y")

    data = {
        'payload' : {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'userid': "xxxxxx",
            'password': "xxxxx",
        },

        'cookies' : {
            'PHPSESSID' : '5647ce3711be9b6967a2cda41716819a',
            'dp__v' : '27305865-HFP94ZWG-SP0E9534-4M7ZLH-TFE',
            'cookiesession1' : '678B28FEGHIJKLMNOPRSTUV01234A9C7',
        },

        'login' : {
            'login' : 'https://monsakti.kemenkeu.go.id/sitp-monsakti-omspan/auth/requestJWTToken',
        },

        'files' : {
            'submit_file' : (None,''),
            'tgl_awal' : (None,'01-01-2022'),
            'tgl_akhir' : (None,today),
            'status' : (None,f'SPM_STS_DATA_{filter_type}'),
        },

        'headers' : {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        }
    }

    return data

def dump_data(filter_type):
    data = get_data(filter_type)
    with open("data.json", "w") as write_file:
        json.dump(data, write_file)


if __name__ == "__main__" : dump_data(11)
    

