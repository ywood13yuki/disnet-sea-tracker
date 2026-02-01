import requests
import pandas as pd
import datetime
import os

def collect():
    print("--- 収集開始 ---")
    url = "https://disney-api.0505keitan.com/exec?park=tds"
    
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        
        # APIの中身をログに表示（これで何が届いたか分かります）
        print(f"取得したデータ件数: {len(data)} 件")
        if len(data) > 0:
            print(f"最初のデータ例: {data[0]}")
        
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timestamp = now.strftime('%Y-%m-%d %H:%M')
        
        new_records = [[timestamp, i.get('name', '???'), i.get('standbyTime', 0)] for i in data]
        new_df = pd.DataFrame(new_records)
        
        file_path = 'wait_times_history.csv'
        if os.path.exists(file_path):
            new_df.to_csv(file_path, mode='a', header=False, index=False)
            print("既存のCSVに追記しました。")
        else:
            new_df.to_csv(file_path, header=['timestamp', 'name', 'wait_time'], index=False)
            print("新しいCSVを作成しました。")
            
    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    collect()
