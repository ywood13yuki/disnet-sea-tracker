import requests
import pandas as pd
import datetime
import os

def collect():
    url = "https://disney-api.0505keitan.com/exec?park=tds"
    try:
        res = requests.get(url, timeout=15)
        data = res.json()
        
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timestamp = now.strftime('%Y-%m-%d %H:%M')
        
        # 取得できた生データをそのままリスト化
        new_records = []
        for item in data:
            new_records.append({
                "timestamp": timestamp,
                "name": item.get('name', 'Unknown'),
                "wait_time": item.get('standbyTime', 0)
            })
        
        df = pd.DataFrame(new_records)
        file_path = 'wait_times_history.csv'
        
        # 追記モードで保存
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)
        print("CSV update successful")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    collect()
