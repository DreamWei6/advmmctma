'''
Created on 2021年1月10日

@author: kankuni
'''
import requests
import json

payload = {
    'mode': '1',
    'input0': '1',
    'input1': '2',
    'input2': '3',
    'input3': '4'
}

r = requests.get('http://localhost:3000/', data = json.dumps(payload))

print(r.text)