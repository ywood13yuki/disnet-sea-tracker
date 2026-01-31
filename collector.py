import requests
import pandas as pd
import datetime
import os

def collect():
    try:
        url = "https://disney-api.0505keitan.com/exec?park=tds"
        res = requests.get(url)
        data = res.json()
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timestamp = now.strftime('%Y-%m-%d %H:%M')
        new_records = [{"timestamp": timestamp, "name": i['name'], "wait_time": i.get('standbyTime', 0)} for i in data]
        new_df = pd.DataFrame(new_records)
        file_path = 'wait_times_history.csv'
        if os.path.exists(file_path):
            new_df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            new_df.to_csv(file_path, index=False)
    except:
        pass

if __name__ == "__main__":
    collect()
