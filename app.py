import streamlit as st

st.set_page_config(page_title="2026 信用卡優惠大管家 Pro", page_icon="💳", layout="centered")

# --- 1. 資料庫：全通路標籤化 (確保關鍵字在各卡一致) ---
INITIAL_DATA = {
    "國泰世華 CUBE卡": {
        "period": "2026/01/01 - 2026/06/30",
        "url": "https://www.cathay-cube.com.tw/cathaybk/personal/product/credit-card/cards/cube-list",
        "schemes": [
            {"name": "玩數位", "tiers": [{"rate": "3%", "merchants": ["ChatGPT(AI)", "Canva(AI)", "Claude(AI)", "App Store", "Google Play", "Netflix(串流)", "Spotify(串流)", "蝦皮(網購/電商)", "momo(網購/電商)", "PChome(網購)", "酷澎(Coupang/網購)", "淘寶(網購)"]}]},
            {"name": "樂饗購", "tiers": [{"rate": "3%", "merchants": ["新光三越(百貨)", "SOGO(百貨)", "遠東百貨(百貨)", "101(百貨)", "微風(百貨)", "誠品", "Uber Eats(外送)", "foodpanda(外送)", "麥當勞(速食)", "星巴克(咖啡)", "康是美(藥妝)", "屈臣氏(藥妝)", "50嵐(飲料)", "麻古(飲料)"]}]},
            {"name": "趣旅行", "tiers": [{"rate": "3%", "merchants": ["海外實體消費", "日本", "韓國", "歐洲", "美國", "迪士尼(樂園)", "環球影城(樂園)", "Uber(叫車)", "Grab(叫車)", "高鐵", "台鐵", "華航(航空)", "長榮(航空)", "星宇(航空)", "Agoda(訂房)", "Klook(旅遊)", "KKday(旅遊)"]}]},
            {"name": "集精選", "tiers": [{"rate": "2%", "merchants": ["家樂福(超市/量販)", "全聯(超市)", "中油直營(加油)", "7-11(超商)", "全家(超商)", "IKEA", "車麻吉", "LOPIA"]}]},
            {"name": "慶生月", "tiers": [
                {"rate": "10%", "merchants": ["紅葉蛋糕", "詹記(火鍋)", "鼎王(火鍋)", "無老鍋(火鍋)", "錢櫃(KTV)", "好樂迪(KTV)", "星聚點(KTV)", "PlayStation(遊戲)", "Nintendo(遊戲)", "巴哈姆特"]},
                {"rate": "3.5%", "merchants": ["新光三越(百貨)", "Uber Eats(外送)", "Klook(旅遊)", "FunNow"]}
            ]},
            {"name": "童樂匯", "tiers": [
                {"rate": "10%", "merchants": ["Mamas&Papas(母嬰)", "10mois", "朱宗慶打擊樂(教室)", "雲門舞集(教室)", "Yamaha音樂教室", "TutorABC Junior(教室)"]},
                {"rate": "5%", "merchants": ["親子餐廳", "貳樓", "大樹先生", "卡多摩(母嬰)", "六福村(樂園)", "九族(樂園)", "義大(樂園)", "蘭城晶英(飯店)", "煙波大飯店"]},
                {"rate": "1%", "merchants": ["私校學費", "台北美國學校", "康橋", "復興實驗高中"]}
            ]}
        ]
    },
    "台新 Richart卡": {
        "period": "2025/01/01 - 2026/12/31",
        "url": "https://mkp.taishinbank.com.tw/s/2025/RichartCard_2025/index.html",
        "schemes": [
            {"name": "Pay著刷", "tiers": [{"rate": "3.8%", "merchants": ["台新Pay", "新光三越(百貨)", "7-11(超商)", "全家(超商)", "康是美(藥妝)", "IKEA", "NET", "路易莎(咖啡)"]}]},
            {"name": "七大通路刷", "tiers": [{"rate": "3.3%", "merchants": ["家樂福(超市/量販)", "酷澎(Coupang/網購)", "高鐵", "台鐵", "Uber(叫車)", "寶雅(藥妝)", "屈臣氏(藥妝)", "全臺餐飲(餐廳)", "Uber Eats(外送)", "foodpanda(外送)", "中油直營(加油)", "蝦皮(網購/電商)", "momo(網購/電商)", "UNIQLO", "星宇(航空)", "華航(航空)", "長榮(航空)", "101(百貨)", "SOGO(百貨)", "微風(百貨)", "誠品"]}]},
            {"name": "假日刷", "tiers": [{"rate": "2%", "merchants": ["週六(週末)", "週日(週末)", "週末限定", "假日消費"]}]}
        ]
    },
    "玉山 Unicard": {
        "period": "2025/10/01 - 2026/06/30",
        "url": "https://event.esunbank.com.tw/credit/unicard/discount-channel.html",
        "schemes": [
            {"name": "百大特店(訂閱制)", "tiers": [{"rate": "4.5%", "merchants": ["LINE Pay(支付)", "街口支付(支付)", "全支付(支付)", "悠遊付(支付)", "momo(網購/電商)", "蝦皮(網購/電商)", "酷澎(Coupang/網購)", "新光三越(百貨)", "SOGO(百貨)", "遠東百貨(百貨)", "家樂福(超市/量販)", "王品(餐廳)", "中油直營(加油)", "高鐵", "台鐵", "星宇(航空)", "華航(航空)", "長榮(航空)", "Klook(旅遊)", "KKday(旅遊)", "Tesla(加油/充電)", "YouBike", "Uber Eats(外送)", "foodpanda(外送)"]}]}
        ]
    }
}

# --- 2. 搜尋與顯示邏輯 ---
st.title("💳 信用卡優惠大管家 Pro")
st.info("💡 試試搜尋：外送、網購、百貨、航空、加油、超商、火鍋")

keyword = st.text_input("📍 輸入店家或類別關鍵字：", placeholder="例如：外送", key="search")

if keyword:
    search_results = []
    
    for card_name, info in INITIAL_DATA.items():
        for scheme in info['schemes']:
            for tier in scheme['tiers']:
                # 同時檢查店家名與括號內的標籤
                matched = [m for m in tier['merchants'] if keyword.lower() in m.lower()]
                if matched:
                    # 顯示時移除標籤
                    clean_matched = [m.split('(')[0] for m in matched]
                    
                    search_results.append({
                        "card": card_name,
                        "scheme": scheme['name'],
                        "rate": tier['rate'],
                        "rate_num": float(tier['rate'].replace('%','').split('-')[0]),
                        "matched": list(set(clean_matched)), # 去重
                        "period": info['period']
                    })
    
    # 排序：高利率在前
    search_results = sorted(search_results, key=lambda x: x['rate_num'], reverse=True)

    if search_results:
        for res in search_results:
            color = "#FF4B4B" if res['rate_num'] >= 4.0 else "#1E88E5" if res['rate_num'] >= 3.0 else "#757575"
            with st.container():
                st.markdown(f"""
                <div style="border-left: 5px solid {color}; padding: 10px 15px; margin-bottom: 15px; background-color: #fcfcfc; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                    <h3 style="margin:0;">{res['card']} | <span style="color:{color};">{res['rate']}</span></h3>
                    <p style="margin:5px 0;">🎯 <b>方案：</b>{res['scheme']}</p>
                    <p style="margin:5px 0;">✅ <b>符合項目：</b> <span style="background-color:#e1f5fe; padding:2px 5px; border-radius:3px;">{"</span> <span style='background-color:#e1f5fe; padding:2px 5px; border-radius:3px;'>".join(res['matched'])}</span></p>
                    <p style="margin:5px 0; font-size: 0.8em; color: #999;">📅 適用至：{res['period'].split('-')[-1].strip()}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning(f"查無 '{keyword}' 的相關加碼回饋。")

st.divider()
st.sidebar.markdown("### 📊 本次搜尋覆蓋範圍")
st.sidebar.write("- **外送**：Uber Eats, foodpanda")
st.sidebar.write("- **網購**：蝦皮, momo, 酷澎, 淘寶")
st.sidebar.write("- **百貨**：新光三越, SOGO, 101, 遠百")
st.sidebar.write("- **超商**：7-11, 全家")
st.sidebar.write("- **航空**：星宇, 華航, 長榮")
