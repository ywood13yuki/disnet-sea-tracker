import requests
import pandas as pd
import datetime
import os

def collect():
    # 1. データを取ってくる
    url = "https://disney-api.0505keitan.com/exec?park=tds"
    res = requests.get(url)
    data = res.json()
    
    # 2. 時間をセット
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    timestamp = now.strftime('%Y-%m-%d %H:%M')
    
    # 3. データを整理する
    new_records = []
    for item in data:
        # standbyTimeがない場合もあるので安全に取得
        wait = item.get('standbyTime')
        if wait is None:
            wait = 0
            
        new_records.append({
            "timestamp": timestamp,
            "name": item.get('name', 'Unknown'),
            "wait_time": wait
        })
    
    new_df = pd.DataFrame(new_records)

    # 4. ファイルに保存する（ここが重要！）
    file_path = 'wait_times_history.csv'
    if os.path.exists(file_path):
        new_df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        new_df.to_csv(file_path, index=False)
    print("Successfully saved to CSV") # ログに出す

if __name__ == "__main__":
    collect()
