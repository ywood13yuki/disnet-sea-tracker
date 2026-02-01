import requests
import pandas as pd
import datetime
import os

def collect():
    try:
        # ディズニーシーのデータを取得
        url = "https://disney-api.0505keitan.com/exec?park=tds"
        res = requests.get(url, timeout=10)
        data = res.json()
        
        # 現在の時刻を取得
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timestamp = now.strftime('%Y-%m-%d %H:%M')
        
        # 必要な情報だけリストにする
        new_records = []
        for item in data:
            name = item.get('name', 'Unknown')
            wait = item.get('standbyTime')
            if wait is None: wait = 0
            new_records.append([timestamp, name, wait])
        
        # CSVファイルに追記する（ここを一番確実な方法に変更！）
        file_path = 'wait_times_history.csv'
        new_df = pd.DataFrame(new_records)
        
        # ファイルが存在すれば追記、なければ新規作成
        if os.path.exists(file_path):
            new_df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            new_df.to_csv(file_path, header=['timestamp', 'name', 'wait_time'], index=False)
            
        print(f"成功！ {len(new_records)}件のデータを追記しました。")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    collect()
