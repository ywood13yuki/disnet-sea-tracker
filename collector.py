import requests
import pandas as pd
import datetime
import os

def collect():
    url = "https://disney-api.0505keitan.com/exec?park=tds"
    print(f"APIにアクセス中: {url}")
    
    try:
        res = requests.get(url, timeout=20)
        data = res.json()
        
        # ログに取得件数を出す（ここが大事！）
        print(f"取得したデータ数: {len(data)}件")
        
        if len(data) == 0:
            print("警告: 取得したデータが0件です。")
            return

        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timestamp = now.strftime('%Y-%m-%d %H:%M')
        
        new_records = []
        for item in data:
            new_records.append({
                "timestamp": timestamp,
                "name": item.get('name', 'Unknown'),
                "wait_time": item.get('standbyTime', 0)
            })
        
        df = pd.DataFrame(new_records)
        file_path = 'wait_times_history.csv'
        
        # 強制的に書き込む
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)
            
        print("CSVへの書き込みが完了しました。")
        
    except Exception as e:
        print(f"実行エラー: {e}")

if __name__ == "__main__":
    collect()
