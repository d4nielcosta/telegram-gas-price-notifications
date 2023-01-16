import os
import json

import requests

from datetime import datetime, timedelta
from dotenv import load_dotenv

# LOAD ENV VARS
load_dotenv()

telegram_token = os.getenv("telegram_token")
telegram_chat_ids = json.loads(os.getenv("chat_ids"))

# FOOTBALL API DETAILS
octopus_tracker_api = 'https://octopus.energy/api/v1/tracker/G-1R-SILVER-FLEX-22-11-25-H/daily/current/0/9646/'

# TELEGRAM DETAILS
telegram_url = "https://api.telegram.org/bot" + telegram_token

today = datetime.today().strftime("%Y-%m-%d")
tomorrow = datetime.today() + timedelta(1)
tomorrow = tomorrow.strftime("%Y-%m-%d")

def fetch_results():
    r = requests.request("GET", octopus_tracker_api)
    print('Response status:', r.status_code)
    return r.json()

def parse_data(data):
    return '''
        <b> {date} </b>
        Today's gas price: {todayGasPrice}
        Tomorrow's predicted price: {tomorrowGasPrice}
        Standing charge: {standingCharge}
        '''.format(date=today,
                   todayGasPrice=[entry['unit_rate'] for entry in data['periods'] if entry['date'] == today],
                   tomorrowGasPrice=[entry['unit_rate'] for entry in data['periods'] if entry['date'] == tomorrow],
                   standingCharge=[entry['standing_charge'] for entry in data['periods'] if entry['date'] == today])


def send_notifications(message):
        for chatId in telegram_chat_ids:
            r = requests.post(telegram_url + '/sendMessage', params={"chat_id": chatId}, json={'text': message, 'parse_mode': 'HTML'})
            print('Telegram response status:', r.status_code, "for chat ending in", str(chatId)[-3:])

def main():
    data = fetch_results()
    message = parse_data(data)
    send_notifications(message)

if __name__ == "__main__":  
    print("Starting run...")  
    main()
    print("Finished")
