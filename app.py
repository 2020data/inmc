import streamlit as st

# 設定網頁標題與圖示
st.set_page_config(page_title="2026 I-NMC Award Ceremony", page_icon="🏆", layout="centered")

# --- 步驟 1：建立中英文雙顯的得獎資料庫 ---
AWARDS_DATA = {
    "Category X - Malaysia (Mathketeers)": {
        "WINNER 🥇": {"ch": "黃偉健", "en": "Wong Wai Kin", "color": "#D4AF37", "bg": "#1c2d42", "rank_title": "CHAMPION / WINNER"},
        "1st RUNNER-UP 🥈": {"ch": "陳佳恩", "en": "Tan Jia En", "color": "#B4B4B4", "bg": "#2b3a4a", "rank_title": "1st RUNNER-UP"},
        "2nd RUNNER-UP 🥉": {"ch": "林俊傑", "en": "Lim Choon Kit", "color": "#CD7F32", "bg": "#2c3e50", "rank_title": "2nd RUNNER-UP"}
    },
    "Category X - Taiwan (Mathketeers)": {
        "WINNER 🥇": {"ch": "陳俊宏", "en": "Chun-Hung Chen", "color": "#D4AF37", "bg": "#1c2d42", "rank_title": "CHAMPION / WINNER"},
        "1st RUNNER-UP 🥈": {"ch": "林雅雯", "en": "Ya-Wen Lin", "color": "#B4B4B4", "bg": "#2b3a4a", "rank_title": "1st RUNNER-UP"},
        "2nd RUNNER-UP 🥉": {"ch": "黃建宇", "en": "Chien-Yu Huang", "color": "#CD7F32", "bg": "#2c3e50", "rank_title": "2nd RUNNER-UP"}
    },
    "Category Y - Malaysia (Theory of Everything)": {
        "WINNER 🥇": {"ch": "陳家輝", "en": "Gary Tan Kah Hui", "color": "#D4AF37", "bg": "#1c2d42", "rank_title": "CHAMPION / WINNER"},
        "1st RUNNER-UP 🥈": {"ch": "林美玲", "en": "May Lim Bee Leng", "color": "#B4B4B4", "bg": "#2b3a4a", "rank_title": "1st RUNNER-UP"},
        "2nd RUNNER-UP 🥉": {"ch": "李振豪", "en": "Jason Lee Chin How", "color": "#CD7F32", "bg": "#2c3e50", "rank_title": "2nd RUNNER-UP"}
    },
    "Category Y - Taiwan (Theory of Everything)": {
        "WINNER 🥇": {"ch": "陳怡君", "en": "Yi-Chun Chen", "color": "#D4AF37", "bg": "#1c2d42", "rank_title": "CHAMPION / WINNER"},
        "1st RUNNER-UP 🥈": {"ch": "林冠宇", "en": "Kuan-Yu Lin", "color": "#B4B4B4", "bg": "#2b3a4a", "rank_title": "1st RUNNER-UP"},
        "2nd RUNNER-UP 🥉": {"ch": "黃柏翰", "en": "Po-Han Huang", "color": "#CD7F32", "bg": "#2c3e50", "rank_title": "2nd RUNNER-UP"}
    },
    "Category Z - Malaysia (Running Math)": {
        "WINNER 🥇": {"ch": "葉子健", "en": "Ken Yap Tze Kin", "color": "#D4AF37", "bg": "#1c2d42", "rank_title": "CHAMPION / WINNER"},
        "1st RUNNER-UP 🥈": {"ch": "郭麗萍", "en": "Lily Kuek Lee Peng", "color": "#B4B4B4", "bg": "#2b3a4a", "rank_title": "1st RUNNER-UP"},
        "2nd RUNNER-UP 🥉": {"ch": "洪俊賢", "en": "Ivan Ang Choon Kheng", "color": "#CD7F32", "bg": "#2c3e50", "rank_title": "2nd RUNNER-UP"}
    },
    "Category Z - Taiwan (Running Math)": {
        "WINNER 🥇": {"ch": "郭俊宏", "en": "Chun-Hung Kuo", "color": "#D4AF37", "bg": "#1c2d42", "rank_title": "CHAMPION / WINNER"},
        "1st RUNNER-UP 🥈": {"ch": "曾菀婷", "en": "Wan-Ting Tseng", "color": "#B4B4B4", "bg": "#2b3a4a", "rank_title": "1st RUNNER-UP"},
        "2nd RUNNER-UP 🥉": {"ch": "洪宇恆", "en": "Yu-Heng Hung", "color": "#CD7F32", "bg": "#2c3e50", "rank_title": "2nd RUNNER-UP"}
    }
}

# --- 步驟 2：初始化 Session State ---
if "selected_place" not in st.session_state:
    st.session_state.selected_place = None
if "current_category" not in st.session_state:
    st.session_state.current_category = list(AWARDS_DATA.keys())[0]

st.title("🏆 2026 I-NMC Grand Award Ceremony")
st.markdown("### 榮耀頒獎典禮（中英雙語對應版）")

# --- 步驟 3：選擇獎項類別 ---
st.write("---")
selected_category = st.selectbox(
    "1. 請選擇要頒發的賽事類別與賽區：", 
    list(AWARDS_DATA.keys())
)

# 當切換賽事類別時，重置得獎畫面的顯示狀態
if selected_category != st.session_state.current_category:
    st.session_state.current_category = selected_category
    st.session_state.selected_place = None

# --- 步驟 4：點選名次按鈕 ---
st.subheader(f"2. 揭曉 {selected_category} 得獎者！")

col1, col2, col3 = st.columns(3)
current_winners = AWARDS_DATA[selected_category]

with col3:
    if st.button("🥉 2nd RUNNER-UP"):
        st.session_state.selected_place = "2nd RUNNER-UP 🥉"
with col2:
    if st.button("🥈 1st RUNNER-UP"):
        st.session_state.selected_place = "1st RUNNER-UP 🥈"
with col1:
    if st.button("🥇 WINNER", type="primary"):
        st.session_state.selected_place = "WINNER 🥇"

# --- 步驟 5：華麗設計感「電子獎狀圖片」畫面 ---
if st.session_state.selected_place:
    place_key = st.session_state.selected_place
    winner_info = current_winners[place_key]
    
    # 抽取特定名次的設計樣式
    theme_color = winner_info["color"]      # 獎項主色（金/銀/銅）
    bg_frame = winner_info["bg"]            # 獎狀厚重外框顏色
    rank_title = winner_info["rank_title"]  # 英文名次大標
    ch_name = winner_info["ch"]              # 中文姓名
    en_name = winner_info["en"]              # 英文姓名
    
    # 特效全開！
    st.snow()
    st.balloons()
    
    st.write("---")
    
    # 顯示奢華歡迎畫面 (使用乾淨無空行的 HTML 避免 Streamlit 解析錯誤)
    st.write("---")
    st.markdown(
        f"""
        <div style="background-color: {bg_frame}; padding: 25px; border-radius: 15px; box-shadow: 0px 15px 35px rgba(0,0,0,0.3); max-width: 650px; margin: 0 auto;">
            <div style="background: #fdfbf7; border: 4px double {theme_color}; border-radius: 8px; padding: 40px 30px; text-align: center; position: relative;">
                <div style="font-size: 55px; margin-bottom: 10px;">🏆</div>
                <h2 style="color: {theme_color}; font-family: 'Georgia', serif; font-size: 26px; letter-spacing: 3px; margin: 0 0 5px 0; font-weight: bold;">CERTIFICATE OF AWARD</h2>
                <p style="color: #666666; font-size: 13px; letter-spacing: 1px; margin: 0 0 25px 0; font-weight: 600;">2026 I-NMC COMPETITION</p>
                <p style="color: #777777; font-size: 16px; font-style: italic; margin-bottom: 20px;">This honor is proudly presented to</p>
                <div style="margin: 30px 0;">
                    <div style="font-size: 45px; font-weight: 900; color: #111111; font-family: 'Microsoft JhengHei', sans-serif; margin-bottom: 8px; letter-spacing: 2px;">{ch_name}</div>
                    <div style="font-size: 28px; font-style: italic; color: #444444; font-family: 'Georgia', serif; letter-spacing: 1px;">{en_name}</div>
                </div>
                <hr style="border: 0; border-top: 2px solid {theme_color}; width: 45%; margin: 25px auto 20px auto;">
                <div style="font-size: 24px; font-weight: 800; color: {theme_color}; letter-spacing: 2px; font-family: 'Arial Black', sans-serif; text-transform: uppercase;">✨ {rank_title} ✨</div>
                <p style="color: #666666; font-size: 13px; margin-top: 10px; font-weight: 500;">{selected_category}</p>
                <p style="font-size: 14px; color: #a0a0a0; margin-top: 25px; font-style: italic;">Let's celebrate this wonderful achievement! 👏👏👏</p>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
