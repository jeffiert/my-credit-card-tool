import streamlit as st

st.set_page_config(page_title="2026 信用卡優惠大管家 Pro", page_icon="💳", layout="centered")

# --- 1. 資料庫：強化關鍵字標籤 (加上隱藏關鍵字以利搜尋) ---
INITIAL_DATA = {
    "國泰世華 CUBE卡": {
        "period": "2026/01/01 - 2026/06/30",
        "url": "https://www.cathay-cube.com.tw/cathaybk/personal/product/credit-card/cards/cube-list",
        "schemes": [
            {"name": "玩數位", "tiers": [{"rate": "3%", "merchants": ["ChatGPT(AI)", "Canva(AI)", "Claude(AI)", "App Store", "Google Play", "Netflix(串流)", "Spotify(串流)", "蝦皮(電商)", "momo(電商)", "PChome", "酷澎(Coupang)", "淘寶"]}]},
            {"name": "樂饗購", "tiers": [{"rate": "3%", "merchants": ["新光三越(百貨)", "SOGO(百貨)", "遠東百貨", "101(百貨)", "微風", "誠品", "Uber Eats(外送)", "foodpanda(外送)", "麥當勞(速食)", "星巴克(咖啡)", "康是美(藥妝)", "屈臣氏(藥妝)", "50嵐(飲料)", "麻古"]}]},
            {"name": "趣旅行", "tiers": [{"rate": "3%", "merchants": ["海外實體消費", "日本", "韓國", "迪士尼(樂園)", "環球影城(樂園)", "Uber(叫車)", "Grab", "高鐵", "台鐵", "華航(航空)", "長榮(航空)", "星宇(航空)", "Agoda(訂房)", "Klook(旅遊)", "KKday(旅遊)"]}]},
            {"name": "集精選", "tiers": [{"rate": "2%", "merchants": ["家樂福(量販)", "全聯(超市)", "中油直營(加油)", "7-11(超商)", "全家(超商)", "IKEA", "車麻吉(停車)", "LOPIA"]}]},
            {"name": "慶生月", "tiers": [
                {"rate": "10%", "merchants": ["紅葉蛋糕", "詹記(火鍋)", "鼎王(火鍋)", "無老鍋(火鍋)", "錢櫃(KTV)", "好樂迪(KTV)", "星聚點(KTV)", "PlayStation", "Nintendo", "巴哈姆特"]},
                {"rate": "3.5%", "merchants": ["新光三越", "Uber Eats", "Klook", "FunNow"]}
            ]},
            {"name": "童樂匯", "tiers": [
                {"rate": "10%", "merchants": ["Mamas&Papas(母嬰)", "10mois", "朱宗慶打擊樂(教室)", "雲門舞集(教室/舞蹈)", "Yamaha音樂教室", "TutorABC Junior(線上教室)"]},
                {"rate": "5%", "merchants": ["親子餐廳", "貳樓", "大樹先生", "卡多摩(母嬰)", "六福村(樂園)", "九族(樂園)", "義大(樂園)", "麗寶樂園", "蘭城晶英(飯店)", "煙波大飯店"]},
                {"rate": "1%", "merchants": ["私校學費", "台北美國學校", "康橋", "復興實驗高中"]}
            ]},
            {"name": "瘋大港", "tiers": [
                {"rate": "10%", "merchants": ["大港開唱周邊", "現場星巴克", "ChargeSPOT"]},
                {"rate": "3.5%", "merchants": ["KKTIX(售票)", "拓元(售票)", "高雄指定住宿", "高鐵", "台鐵"]}
            ]}
        ]
    },
    "台新 Richart卡": {
        "period": "2025/01/01 - 2026/12/31",
        "url": "https://mkp.taishinbank.com.tw/s/2025/RichartCard_2025/index.html",
        "schemes": [
            {"name": "Pay著刷", "tiers": [{"rate": "3.8%", "merchants": ["台新Pay", "新光三越", "7-11", "全家", "康是美", "IKEA", "NET", "路易莎"]}]},
            {"name": "七大通路(天天/好饗/數趣/玩旅/大筆)", "tiers": [{"rate": "3.3%", "merchants": ["家樂福", "酷澎", "高鐵", "台鐵", "Uber", "寶雅", "屈臣氏", "全臺餐飲(餐廳)", "Uber Eats", "foodpanda", "中油直營", "蝦皮", "momo", "UNIQLO", "星宇", "華航", "長榮", "101", "SOGO"]}]},
            {"name": "假日刷", "tiers": [{"rate": "2%", "merchants": ["週六", "週日", "週末限定", "假日消費"]}]}
        ]
    },
    "玉山 Unicard": {
        "period": "2025/10/01 - 2026/06/30",
        "url": "https://event.esunbank.com.tw/credit/unicard/discount-channel.html",
        "schemes": [
            {"name": "百大特店(訂閱制)", "tiers": [{"rate": "4.5%", "merchants": ["LINE Pay", "街口支付", "全支付", "悠遊付", "momo", "蝦皮", "酷澎", "新光三越", "SOGO", "家樂福", "王品(餐廳)", "中油直營", "高鐵", "星宇", "Tesla", "YouBike"]}]}
        ]
    }
}

# --- 2. 搜尋與顯示邏輯 ---
st.title("💳 信用卡優惠大管家 Pro")
st.caption("支援多項目搜尋：試試輸入「教室」、「航空」、「火鍋」或「外送」")

keyword = st.text_input("📍 搜尋店家、支付或類別：", placeholder="例如：教室", key="search")

if keyword:
    search_results = []
    
    for card_name, info in INITIAL_DATA.items():
        for scheme in info['schemes']:
            for tier in scheme['tiers']:
                # 找出所有符合關鍵字的店家
                matched = [m for m in tier['merchants'] if keyword.lower() in m.lower()]
                if matched:
                    # 移除店家名稱中的標籤括號，讓顯示更乾淨
                    clean_matched = [m.split('(')[0] for m in matched]
                    
                    search_results.append({
                        "card": card_name,
                        "scheme": scheme['name'],
                        "rate": tier['rate'],
                        "rate_num": float(tier['rate'].replace('%','').split('-')[0]),
                        "matched": clean_matched,
                        "period": info['period']
                    })
    
    # 先依利率排序
    search_results = sorted(search_results, key=lambda x: x['rate_num'], reverse=True)

    if search_results:
        for res in search_results:
            color = "#FF4B4B" if res['rate_num'] >= 4.0 else "#1E88E5" if res['rate_num'] >= 3.0 else "#757575"
            with st.container():
                # UI 加強：如果有多個命中，使用清單顯示
                st.markdown(f"""
                <div style="border-left: 5px solid {color}; padding: 10px 15px; margin-bottom: 15px; background-color: #fcfcfc; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                    <h3 style="margin:0;">{res['card']} | <span style="color:{color};">{res['rate']}</span></h3>
                    <p style="margin:5px 0;">🎯 <b>方案：</b>{res['scheme']}</p>
                    <p style="margin:5px 0;">✅ <b>符合項目：</b> <span style="background-color:#e1f5fe; padding:2px 5px; border-radius:3px;">{"</span> <span style='background-color:#e1f5fe; padding:2px 5px; border-radius:3px;'>".join(res['matched'])}</span></p>
                    <p style="margin:5px 0; font-size: 0.8em; color: #999;">📅 適用至：{res['period'].split('-')[-1].strip()}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning(f"查無 '{keyword}' 的加碼回饋。")

st.divider()
st.sidebar.markdown("### 🔍 搜尋小撇步")
st.sidebar.write("- 搜「**樂園**」：看迪士尼、六福村")
st.sidebar.write("- 搜「**AI**」：看 ChatGPT、Claude")
st.sidebar.write("- 搜「**火鍋**」：看詹記、鼎王")
st.sidebar.write("- 搜「**教室**」：看所有教學機構")
