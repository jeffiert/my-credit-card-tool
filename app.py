import streamlit as st

# 設定網頁標題
st.set_page_config(page_title="信用卡優惠快查", layout="centered")

# --- 1. 補齊資料庫：加入【適用期間】 ---
INITIAL_DATA = {
    "國泰世華 CUBE卡": {
        "period": "2026/01/01 - 2026/06/30",
        "benefits": [
            {"scheme": "玩數位", "rate": "3%", "merchants": ["ChatGPT", "Canva", "Apple", "Google Play", "Netflix", "Spotify", "蝦皮購物", "momo購物網", "PChome", "Coupang", "酷澎", "淘寶", "天貓"]},
            {"scheme": "樂饗購", "rate": "3%", "merchants": ["遠東SOGO", "新光三越", "遠東百貨", "台北101", "微風", "誠品", "Uber Eats", "foodpanda", "麥當勞", "康是美", "屈臣氏", "50嵐", "麻古茶坊"]},
            {"scheme": "趣旅行", "rate": "3%", "merchants": ["海外實體消費", "日本", "韓國", "泰國", "歐洲", "美國", "日本迪士尼", "環球影城", "Uber", "Grab", "台灣高鐵", "yoxi", "台灣大車隊", "iRent", "和運租車", "格上租車", "航空機票", "Agoda", "Booking.com", "KKday", "Klook"]},
            {"scheme": "集精選", "rate": "2%", "merchants": ["家樂福", "全聯", "中油直營", "7-ELEVEN", "7-11", "全家", "IKEA"]}
        ]
    },
    "台新 Richart卡": {
        "period": "2025/01/01 - 2026/12/31", # 台新 2025 權益通常延續至 2026 年底
        "benefits": [
            {"scheme": "Pay著刷", "rate": "3.8%", "merchants": ["台新Pay", "新光三越", "7-11", "全家", "康是美", "IKEA", "NET", "路易莎"]},
            {"scheme": "天天刷/好饗刷/數趣刷", "rate": "3.3%", "merchants": ["家樂福", "大買家", "高鐵", "台灣大車隊", "Uber", "寶雅", "屈臣氏", "全臺餐飲", "Uber Eats", "foodpanda", "中油直營", "台亞加油", "全國加油", "蝦皮", "momo", "PChome", "酷澎", "Coupang", "星宇航空", "中華航空", "長榮航空"]}
        ]
    },
    "玉山 Unicard": {
        "period": "2025/10/01 - 2026/06/30",
        "benefits": [
            {"scheme": "百大特店(訂閱制)", "rate": "4.5%", "merchants": ["LINE Pay", "街口支付", "全支付", "悠遊付", "momo購物網", "蝦皮購物", "酷澎", "Coupang", "新光三越", "遠東百貨", "家樂福", "特力屋", "星宇航空", "中華航空", "長榮航空", "Klook", "KKday", "Tesla", "特斯拉", "Gogoro", "YouBike"]}
        ]
    }
}

# 初始化
if 'cards_db' not in st.session_state:
    st.session_state.cards_db = INITIAL_DATA

# --- 2. UI 介面 ---
st.title("💳 信用卡優惠快查 (2026)")
st.caption("即時比對 CUBE / Richart / Unicard 最優回饋")

# 搜尋框
keyword = st.text_input("📍 我要在哪裡消費？", placeholder="輸入：中油、蝦皮、LINE Pay...", key="search_input")

if keyword:
    results = []
    # 搜尋與排序邏輯
    for card_name, info in st.session_state.cards_db.items():
        for b in info['benefits']:
            matched = [m for m in b['merchants'] if keyword.lower() in m.lower()]
            if matched:
                # 提取利率數字進行排序 (處理 3.3% - 3.8% 這種區間)
                rate_val = float(b['rate'].replace('%', '').split('-')[0])
                results.append({
                    "card": card_name,
                    "rate": b['rate'],
                    "scheme": b['scheme'],
                    "period": info['period'],
                    "matched": matched,
                    "sort_key": rate_val
                })

    # 依利率排序 (由高到低)
    results = sorted(results, key=lambda x: x['sort_key'], reverse=True)

    if results:
        for res in results:
            with st.container():
                # 使用明顯的標題顯示利率與卡片
                st.markdown(f"### {res['card']} | <span style='color:#ff4b4b'>{res['rate']}</span>", unsafe_allow_html=True)
                st.write(f"✅ **適用方案：** {res['scheme']}")
                st.write(f"✅ **匹配到：** {', '.join(res['matched'])}")
                st.info(f"📅 **適用期間：** {res['period']}")
                st.divider()
    else:
        st.error(f"查無 '{keyword}' 的加碼回饋。")

# 頁尾小提醒
st.caption("⚠️ 提醒：CUBE卡需於消費當天切換方案；Unicard 4.5% 需維持訂閱狀態。")
