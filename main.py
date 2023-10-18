import os
import sys
import json

import requests

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv("telegram_token")
telegram_chat_ids = json.loads(os.getenv("chat_ids"))

octopus_tracker_api = 'https://octopus.energy/api/v1/tracker/G-1R-SILVER-FLEX-22-11-25-N/daily/current/0/9646/'
telegram_url = "https://api.telegram.org/bot" + telegram_token

today = datetime.today().strftime("%Y-%m-%d")
tomorrow = datetime.today() + timedelta(1)
tomorrow = tomorrow.strftime("%Y-%m-%d")

def fetch_results():
    r = requests.request("GET", octopus_tracker_api)
    print('Response status:', r.status_code)
    return r.json()

def parse_today_price(data):
    return '''Today's gas price: <b>{todayGasPrice}</b>'''.format(todayGasPrice=[entry['unit_rate'] for entry in data['periods'] if entry['date'] == today][0])

def parse_tomorrow_price(data):
    return '''Tomorrow's gas price: <b>{tomorrowGasPrice}</b>'''.format(tomorrowGasPrice=[entry['unit_rate'] for entry in data['periods'] if entry['date'] == tomorrow][0])

def send_notifications(message):
        for chatId in telegram_chat_ids:
            r = requests.post(telegram_url + '/sendMessage', params={"chat_id": chatId}, json={'text': message, 'parse_mode': 'HTML'})
            print('Telegram response status:', r.status_code, "for chat ending in", str(chatId)[-3:])

def main():
    data = fetch_results()

    if (sys.argv[1].upper() == 'PM'):
        message = parse_tomorrow_price(data)
    else:
        message = parse_today_price(data)

    send_notifications(message)

if __name__ == "__main__":  
    print("Running flow:", sys.argv[1])
    main()
    print("Finished")
