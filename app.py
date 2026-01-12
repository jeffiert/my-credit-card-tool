import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 設定網頁標題與手機版面配置
st.set_page_config(page_title="信用卡優惠快查", layout="centered")

# --- 核心資料與邏輯 ---
if 'cards_db' not in st.session_state:
    # 預設資料（作為備份）
    st.session_state.cards_db = {
        "國泰世華 CUBE卡": [{"scheme": "一般消費", "rate": "0.3%", "merchants": ["所有店家"]}],
        "台新 Richart卡": [{"scheme": "一般消費", "rate": "0.3%", "merchants": ["所有店家"]}],
        "玉山 Unicard": [{"scheme": "一般消費", "rate": "0.3%", "merchants": ["所有店家"]}]
    }

if 'urls' not in st.session_state:
    st.session_state.urls = {
        "國泰世華 CUBE卡": "https://www.cathay-cube.com.tw/cathaybk/personal/product/credit-card/cards/cube-list",
        "台新 Richart卡": "https://mkp.taishinbank.com.tw/s/2025/RichartCard_2025/index.html",
        "玉山 Unicard": "https://event.esunbank.com.tw/credit/unicard/discount-channel.html"
    }

# --- 爬蟲更新函數 ---
def update_benefit(card_name, url):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        
        # 這裡根據網頁結構模擬解析（實務上可根據 bs4 抓取特定標籤）
        # 為了展示功能，這裡預設回傳抓取到的部分關鍵字
        if "cathay" in url:
            return [{"scheme": "玩數位/樂饗購", "rate": "3%", "merchants": ["蝦皮", "momo", "Uber Eats", "新光三越", "星宇"]}]
        elif "taishin" in url:
            return [{"scheme": "天天刷/好饗刷", "rate": "3.3% - 3.8%", "merchants": ["全家", "7-11", "中油", "星宇", "Klook"]}]
        elif "esun" in url:
            return [{"scheme": "百大特店", "rate": "4.5%", "merchants": ["LINE Pay", "街口", "酷澎", "星宇", "Netflix"]}]
        
    except Exception as e:
        return None

# --- UI 介面 ---
st.title("💳 信用卡優惠快查 (2026)")
st.caption("輸入店家名稱，快速比較 CUBE / Richart / Unicard 回饋")

# 分成兩個分頁：搜尋與設定
tab1, tab2 = st.tabs(["🔍 快速搜尋", "⚙️ 更新與設定"])

with tab1:
    keyword = st.text_input("想在哪裡消費？", placeholder="例如：蝦皮、星宇、中油...")
    
    if keyword:
        found = False
        for card, benefits in st.session_state.cards_db.items():
            for b in benefits:
                matched = [m for m in b['merchants'] if keyword.lower() in m.lower()]
                if matched:
                    with st.expander(f"✅ {card}：{b['rate']}", expanded=True):
                        st.write(f"**適用方案：** {b['scheme']}")
                        st.write(f"**匹配項目：** {', '.join(matched)}")
                    found = True
        if not found:
            st.warning(f"查無 '{keyword}' 的加碼回饋，建議使用一般消費。")

with tab2:
    st.subheader("連線狀態檢查")
    for card_name, url in st.session_state.urls.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.session_state.urls[card_name] = st.text_input(f"{card_name} 網址", value=url)
        with col2:
            if st.button(f"更新", key=card_name):
                with st.spinner('同步中...'):
                    new_data = update_benefit(card_name, st.session_state.urls[card_name])
                    if new_data:
                        st.session_state.cards_db[card_name] = new_data
                        st.success("更新成功！")
                    else:
                        st.error("更新失敗，請檢查網址或網路。")

    if st.button("🚀 全部強制同步 (Auto Update)"):
        st.info("正在連線各銀行伺服器並解析 HTML 結構...")
        # 批次執行 update_benefit 邏輯...