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
        
        new_records = []
        for item in data:
            new_records.append({
                "timestamp": timestamp,
                "name": item.get('name', 'Unknown'),
                "wait_time": item.get('standbyTime', 0)
            })
        
        new_df = pd.DataFrame(new_records)
        
        # 実行しているディレクトリに確実に保存する
        file_path = os.path.join(os.getcwd(), 'wait_times_history.csv')
        
        if os.path.exists(file_path):
            new_df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            new_df.to_csv(file_path, index=False)
        print(f"Saved to {file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    collect()
