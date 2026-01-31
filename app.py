import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ページの設定
st.set_page_config(page_title="TDS混雑ナビ", layout="centered")

st.title("🌋 TDS 待ち時間分析")

file_path = 'wait_times_history.csv'

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    
    if not df.empty and 'name' in df.columns:
        # アトラクション選択
        attractions = df['name'].unique()
        selected = st.selectbox("アトラクションを選択", attractions)
        
        # データの絞り込み
        target_df = df[df['name'] == selected]
        
        # グラフ作成
        st.subheader(f"📊 {selected} の推移")
        fig = px.bar(target_df, x='timestamp', y='wait_time', 
                     color='wait_time', color_continuous_scale='Reds',
                     labels={'timestamp': '時刻', 'wait_time': '待ち時間(分)'})
        st.plotly_chart(fig, use_container_width=True)
        
        # 最新の待ち時間を表示
        latest_wait = target_df['wait_time'].iloc[-1]
        st.metric("現在の待ち時間", f"{latest_wait} 分")
    else:
        st.info("データがまだ十分に貯まっていません。1時間後にもう一度見てみてね！")
else:
    st.error("データファイルが見つかりません。")
