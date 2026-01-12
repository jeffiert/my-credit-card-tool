import streamlit as st

st.set_page_config(page_title="2026 信用卡大管家 Pro", page_icon="💳", layout="centered")

# --- 1. 結構化資料庫：支援多層級利率 ---
INITIAL_DATA = {
    "國泰世華 CUBE卡": {
        "period": "2026/01/01 - 2026/06/30",
        "url": "https://www.cathay-cube.com.tw/cathaybk/personal/product/credit-card/cards/cube-list",
        "schemes": [
            {"name": "玩數位", "tiers": [{"rate": "3%", "merchants": ["ChatGPT", "Canva", "Claude", "App Store", "Google Play", "Netflix", "Spotify", "蝦皮", "momo", "PChome", "酷澎", "Coupang", "淘寶"]}]},
            {"name": "樂饗購", "tiers": [{"rate": "3%", "merchants": ["新光三越", "SOGO", "遠東百貨", "101", "微風", "誠品", "Uber Eats", "foodpanda", "麥當勞", "星巴克", "康是美", "屈臣氏", "50嵐", "麻古"]}]},
            {"name": "趣旅行", "tiers": [{"rate": "3%", "merchants": ["海外實體", "日本", "韓國", "歐洲", "美國", "迪士尼", "環球影城", "Uber", "Grab", "高鐵", "台鐵", "華航", "長榮", "星宇", "Agoda", "Klook", "KKday"]}]},
            {"name": "集精選", "tiers": [{"rate": "2%", "merchants": ["家樂福", "全聯", "中油直營", "7-11", "全家", "IKEA", "車麻吉", "LOPIA"]}]},
            {"name": "慶生月", "tiers": [
                {"rate": "10%", "merchants": ["紅葉蛋糕", "詹記", "鼎王", "無老鍋", "錢櫃", "好樂迪", "星聚點", "PlayStation", "Nintendo", "巴哈姆特", "指定生日餐廳"]},
                {"rate": "3.5%", "merchants": ["新光三越", "Uber Eats", "Klook", "FunNow"]}
            ]},
            {"name": "童樂匯", "tiers": [
                {"rate": "10%", "merchants": ["Mamas&Papas", "10mois", "古北町", "朱宗慶打擊樂", "雲門舞集", "Yamaha音樂教室", "TutorABC Junior"]},
                {"rate": "5%", "merchants": ["親子餐廳", "貳樓", "大樹先生", "卡多摩", "樂兒屋", "六福村", "九族", "義大", "麗寶樂園", "蘭城晶英", "煙波大飯店"]},
                {"rate": "1%", "merchants": ["私校學費", "台北美國學校", "康橋", "復興實驗高中"]}
            ]},
            {"name": "瘋大港", "tiers": [
                {"rate": "10%", "merchants": ["大港開唱現場周邊", "現場星巴克", "大港倉", "ChargeSPOT"]},
                {"rate": "3.5%", "merchants": ["KKTIX", "拓元", "大港周邊商品預購", "高雄指定住宿", "高雄Klook", "高鐵", "台鐵"]}
            ]}
        ]
    },
    "台新 Richart卡": {
        "period": "2025/01/01 - 2026/12/31",
        "url": "https://mkp.taishinbank.com.tw/s/2025/RichartCard_2025/index.html",
        "schemes": [
            {"name": "Pay著刷", "tiers": [{"rate": "3.8%", "merchants": ["台新Pay", "新光三越", "7-11", "全家", "康是美", "IKEA", "NET", "路易莎"]}]},
            {"name": "天天刷", "tiers": [{"rate": "3.3%", "merchants": ["家樂福", "大買家", "唐吉訶德", "高鐵", "台鐵", "台灣大車隊", "Uber", "寶雅", "屈臣氏", "車麻吉"]}]},
            {"name": "大筆刷", "tiers": [{"rate": "3.3%", "merchants": ["遠東百貨", "SOGO", "微風", "101", "誠品", "特力屋", "HOLA", "宜得利"]}]},
            {"name": "好饗刷", "tiers": [{"rate": "3.3%", "merchants": ["全臺餐飲", "餐廳", "王品瘋Pay", "Uber Eats", "foodpanda", "錢櫃", "好樂迪", "中油直營", "EVOASIS"]}]},
            {"name": "數趣刷", "tiers": [{"rate": "3.3%", "merchants": ["蝦皮", "momo", "PChome", "酷澎", "Coupang", "Yahoo購物", "博客來", "UNIQLO", "GU", "ZARA", "Netflix", "Spotify"]}]},
            {"name": "玩旅刷", "tiers": [{"rate": "3.3%", "merchants": ["海外消費", "華航", "長榮", "星宇", "Klook", "KKday", "Agoda", "Airbnb"]}]},
            {"name": "假日刷", "tiers": [{"rate": "2%", "merchants": ["週六", "週日", "週末限定", "假日消費"]}]} # 修正為 2%
        ]
    },
    "玉山 Unicard": {
        "period": "2025/10/01 - 2026/06/30",
        "url": "https://event.esunbank.com.tw/credit/unicard/discount-channel.html",
        "schemes": [
            {"name": "百大特店(訂閱制)", "tiers": [{"rate": "4.5%", "merchants": ["LINE Pay", "街口", "全支付", "悠遊付", "momo", "蝦皮", "酷澎", "新光三越", "SOGO", "家樂福", "王品", "中油直營", "高鐵", "星宇", "Tesla", "YouBike"]}]}
        ]
    }
}

# --- 2. 處理搜尋與顯示 ---
st.title("💳 信用卡優惠搜尋 Pro")
keyword = st.text_input("📍 我要在哪裡消費？", placeholder="例如：紅葉蛋糕、學費、全家、週末...")

if keyword:
    results = []
    for card_name, info in INITIAL_DATA.items():
        for scheme in info['schemes']:
            for tier in scheme['tiers']:
                matched = [m for m in tier['merchants'] if keyword.lower() in m.lower()]
                if matched:
                    results.append({
                        "card": card_name,
                        "scheme": scheme['name'],
                        "rate": tier['rate'],
                        "rate_num": float(tier['rate'].replace('%','')),
                        "matched": matched,
                        "period": info['period']
                    })
    
    # 排序：高利率在前
    results = sorted(results, key=lambda x: x['rate_num'], reverse=True)

    if results:
        for res in results:
            color = "#FF4B4B" if res['rate_num'] >= 4.0 else "#1E88E5" if res['rate_num'] >= 3.0 else "#757575"
            with st.container():
                st.markdown(f"""
                <div style="border-left: 5px solid {color}; padding: 10px 15px; margin-bottom: 15px; background-color: #fcfcfc; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                    <h3 style="margin:0;">{res['card']} | <span style="color:{color};">{res['rate']}</span></h3>
                    <p style="margin:5px 0;">🎯 <b>方案：</b>{res['scheme']}</p>
                    <p style="margin:5px 0;">📌 <b>符合：</b>{', '.join(res['matched'])}</p>
                    <p style="margin:5px 0; font-size: 0.8em; color: #999;">📅 適用期間：{res['period']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning(f"查無 '{keyword}' 的加碼。")

st.sidebar.markdown("### 📋 快速提醒")
st.sidebar.info("1. CUBE 慶生月 10% 僅限壽星當月。")
st.sidebar.info("2. 台新假日刷 2% 適用於週六與週日。")
st.sidebar.info("3. 玉山 4.5% 需於 App 內訂閱方案。")
