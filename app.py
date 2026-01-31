import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="TDS混雑ナビ", layout="centered")
st.title("🌋 TDS 待ち時間分析")

file_path = 'wait_times_history.csv'

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    if not df.empty and 'name' in df.columns:
        selected = st.selectbox("アトラクションを選択", df['name'].unique())
        target_df = df[df['name'] == selected]
        st.subheader(f"📊 {selected} の推移")
        fig = px.bar(target_df, x='timestamp', y='wait_time', color='wait_time', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("データが溜まるのを待っています...")
else:
    st.warning("ファイルが見つかりません。")
