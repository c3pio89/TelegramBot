import requests
from config import api_key_kurs

class APIException():
    def __init__(self, message):
       self.message = message

    def __repr__(self):
        return self.message

class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        res = base + quote
        kurs = requests.get('https://currate.ru/api/?get=rates&pairs=' + res + '&key=' + api_key_kurs).json()
        if kurs['status'] == '500':
            return False
        else:
           return float(kurs['data'][res]) * amount

    @staticmethod
    def getValut():
        get_kurs = requests.get('https://currate.ru/api/?get=currency_list&key=' + api_key_kurs).json()
        return get_kurs['data']
