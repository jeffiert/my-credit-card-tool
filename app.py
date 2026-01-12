import streamlit as st
import requests
from bs4 import BeautifulSoup

# 設定網頁標題
st.set_page_config(page_title="信用卡優惠快查", layout="centered")

# --- 1. 建立固定的 2026 優惠資料庫 (避免重置後變空白) ---
# 這些資料會作為網頁開啟時的預設內容
INITIAL_DATA = {
    "國泰世華 CUBE卡": [
        {"scheme": "玩數位", "rate": "3%", "merchants": ["ChatGPT", "Canva", "Apple", "Google Play", "Netflix", "Spotify", "蝦皮購物", "momo購物網", "PChome", "Coupang", "酷澎", "淘寶", "天貓"]},
        {"scheme": "樂饗購", "rate": "3%", "merchants": ["遠東SOGO", "新光三越", "遠東百貨", "台北101", "微風", "誠品", "Uber Eats", "foodpanda", "麥當勞", "康是美", "屈臣氏", "50嵐", "麻古茶坊"]},
        {"scheme": "集精選", "rate": "2%", "merchants": ["家樂福", "全聯", "中油直營", "7-ELEVEN", "7-11", "全家", "IKEA"]}
    ],
    "台新 Richart卡": [
        {"scheme": "Pay著刷", "rate": "3.8%", "merchants": ["台新Pay", "新光三越", "7-11", "全家", "康是美", "IKEA"]},
        {"scheme": "天天刷/好饗刷", "rate": "3.3%", "merchants": ["家樂福", "大買家", "高鐵", "台灣大車隊", "Uber", "寶雅", "屈臣氏", "全臺餐飲", "Uber Eats", "foodpanda", "中油直營", "台亞加油", "全國加油"]}
    ],
    "玉山 Unicard": [
        {"scheme": "百大特店(訂閱制)", "rate": "4.5%", "merchants": ["LINE Pay", "街口支付", "全支付", "悠遊付", "momo購物網", "蝦皮購物", "酷澎", "Coupang", "新光三越", "家樂福", "特力屋", "星宇航空", "中華航空", "長榮航空", "Klook", "KKday", "Tesla", "特斯拉"]}
    ]
}

# 初始化 session_state
if 'cards_db' not in st.session_state:
    st.session_state.cards_db = INITIAL_DATA

if 'urls' not in st.session_state:
    st.session_state.urls = {
        "國泰世華 CUBE卡": "https://www.cathay-cube.com.tw/cathaybk/personal/product/credit-card/cards/cube-list",
        "台新 Richart卡": "https://mkp.taishinbank.com.tw/s/2025/RichartCard_2025/index.html",
        "玉山 Unicard": "https://event.esunbank.com.tw/credit/unicard/discount-channel.html"
    }

# --- 2. 爬蟲更新函數 (保持結構) ---
def update_benefit(card_name, url):
    # 這裡可以保留之前的爬蟲邏輯，但建議先手動維護 INITIAL_DATA 較穩定
    # 因為銀行網頁有防爬蟲機制，Streamlit Server 的 IP 常會被擋
    st.warning(f"正在嘗試更新 {card_name}，若失敗請檢查網址或稍後再試。")
    return INITIAL_DATA.get(card_name) # 暫時回傳內建資料作為範例

# --- 3. UI 介面 ---
st.title("💳 信用卡優惠快查 (2026)")
st.info("💡 提示：輸入店家或支付名稱，例如：『中油』、『蝦皮』、『LINE Pay』")

tab1, tab2 = st.tabs(["🔍 快速搜尋", "⚙️ 更新網址"])

with tab1:
    keyword = st.text_input("📍 我要在哪裡消費？", placeholder="輸入店家名稱...", key="search_input")
    
    if keyword:
        results_found = False
        # 建立搜尋結果清單
        for card, benefits in st.session_state.cards_db.items():
            for b in benefits:
                # 模糊比對
                matched = [m for m in b['merchants'] if keyword.lower() in m.lower()]
                if matched:
                    with st.container():
                        st.markdown(f"### {card} | **{b['rate']}**")
                        st.write(f"🔹 **適用方案：** {b['scheme']}")
                        st.write(f"🔹 **匹配到：** {', '.join(matched)}")
                        st.divider()
                    results_found = True
        
        if not results_found:
            st.error(f"查無 '{keyword}' 的加碼回饋，建議使用一般消費。")

with tab2:
    st.subheader("🔗 銀行優惠網址管理")
    for card_name, url in st.session_state.urls.items():
        st.session_state.urls[card_name] = st.text_input(f"{card_name}", value=url)
    
    if st.button("🔄 立即同步最新資料"):
        # 這裡會重新跑一遍爬蟲邏輯
        st.toast("功能開發中：目前將維持內建優惠資料")
