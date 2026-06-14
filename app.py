import streamlit as st

# 設定網頁標題與圖示
st.set_page_config(page_title="2026 I-NMC Award Ceremony", page_icon="🏆", layout="centered")

# --- 步驟 1：建立 2026 I-NMC 得獎資料庫 (根據 Excel 檔案) ---
# 依照檔案萃取前三名，並只保留英文名字
AWARDS_DATA = {
    "Category X - Malaysia (Mathketeers)": {
        "WINNER 🥇": "Wong Wai Kin",
        "1st RUNNER-UP 🥈": "Tan Jia En",
        "2nd RUNNER-UP 🥉": "Lim Choon Kit"
    },
    "Category X - Taiwan (Mathketeers)": {
        "WINNER 🥇": "Chun-Hung Chen",
        "1st RUNNER-UP 🥈": "Ya-Wen Lin",
        "2nd RUNNER-UP 🥉": "Chien-Yu Huang"
    },
    "Category Y - Malaysia (Theory of Everything)": {
        "WINNER 🥇": "Gary Tan Kah Hui",
        "1st RUNNER-UP 🥈": "May Lim Bee Leng",
        "2nd RUNNER-UP 🥉": "Jason Lee Chin How"
    },
    "Category Y - Taiwan (Theory of Everything)": {
        "WINNER 🥇": "Yi-Chun Chen",
        "1st RUNNER-UP 🥈": "Kuan-Yu Lin",
        "2nd RUNNER-UP 🥉": "Po-Han Huang"
    },
    "Category Z - Malaysia (Running Math)": {
        "WINNER 🥇": "Ken Yap Tze Kin",
        "1st RUNNER-UP 🥈": "Lily Kuek Lee Peng",
        "2nd RUNNER-UP 🥉": "Ivan Ang Choon Kheng"
    },
    "Category Z - Taiwan (Running Math)": {
        "WINNER 🥇": "Chun-Hung Kuo",
        "1st RUNNER-UP 🥈": "Wan-Ting Tseng",
        "2nd RUNNER-UP 🥉": "Yu-Heng Hung"
    }
}

# --- 步驟 2：初始化 Session State ---
if "selected_place" not in st.session_state:
    st.session_state.selected_place = None
if "current_category" not in st.session_state:
    st.session_state.current_category = list(AWARDS_DATA.keys())[0]

st.title("🏆 2026 I-NMC Award Ceremony")
st.markdown("### 榮耀頒獎典禮")

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

# 建立三欄式按鈕 (依照順序揭曉：第三名 -> 第二名 -> 第一名)
col1, col2, col3 = st.columns(3)

# 取得目前選擇的賽事資料
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

# --- 步驟 5：熱烈的歡迎畫面 ---
if st.session_state.selected_place:
    place_title = st.session_state.selected_place
    winner_name = current_winners[place_title]
    
    # 觸發雙重特效：滿天星辰 (snow) + 滿天歡慶氣球 (balloons)
    st.snow()
    st.balloons()
    
    # 顯示奢華歡迎畫面 (HTML)
    st.write("---")
    st.markdown(
        f"""
        <div style="background-color:#FFF3CD; padding: 40px 20px; border-radius: 20px; border: 5px solid #FFD700; text-align: center; box-shadow: 0px 10px 25px rgba(0,0,0,0.15); animation: pulse 2s infinite;">
            <h1 style="color: #856404; font-size: 55px; margin-bottom: 10px; font-family: 'Arial Black', sans-serif;">🎉 CONGRATULATIONS! 🎉</h1>
            <h2 style="color: #495057; font-size: 32px; letter-spacing: 1px; font-weight: bold;">{place_title}</h2>
            <hr style="border: 1px dashed #FFD700; width: 60%; margin: 20px auto;">
            <h1 style="color: #d39e00; font-size: 65px; font-weight: 900; letter-spacing: 3px; text-transform: uppercase; margin: 20px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                ✨ {winner_name} ✨
            </h1>
            <p style="font-size: 22px; color: #6c757d; margin-top: 15px; font-style: italic;">Let's give them a big round of applause! 👏👏👏</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
