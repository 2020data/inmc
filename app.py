import streamlit as st
import random
from streamlit_confetti import confetti

# 設定網頁標題與圖示
st.set_page_config(page_title="頒獎典禮 Award Ceremony", page_icon="🏆", layout="centered")

# 初始化 Session State，用來記錄得獎名單與當前點選的名次
if "winners" not in st.session_state:
    st.session_state.winners = {}
if "selected_place" not in st.session_state:
    st.session_state.selected_place = None

st.title("🏆 榮耀頒獎典禮 Grand Award Ceremony")
st.write("請在下方輸入參賽者名單（中英文皆可），系統將隨機抽出前三名（顯示為英文名字）。")

# --- 第一步：輸入名單 ---
st.subheader("1. 填寫參賽者名單")
# 提供預設文字方便測試
default_names = "王小明 Wang Xiao Ming\n陳美麗 Chen Mei Li\n張三 Zhang San\n李四 Li Si\n林志玲 Lin Zhi Ling"
names_input = st.text_area("每行輸入一個名字（格式：中文 英文名字）：", value=default_names, height=150)

# 處理輸入的名單，只抓取英文部分
def extract_english_name(line):
    # 簡單的切分：假設中文和英文中間有空格，我們抓取後半段的英文
    parts = line.strip().split()
    if len(parts) > 1:
        # 將後半段的所有英文單字組合起來
        return " ".join(parts[1:])
    elif len(parts) == 1:
        return parts[0]
    return ""

if st.button("🎉 生成前三名得獎名單", type="primary"):
    # 清洗名單
    name_list = [extract_english_name(line) for line in names_input.split("\n") if line.strip()]
    
    if len(name_list) < 3:
        st.error("❌ 參賽人數不足 3 人，請多輸入一些名字！")
    else:
        # 隨機抽取前三名
        lucky_drawn = random.sample(name_list, 3)
        st.session_state.winners = {
            "1st Place 🥇": lucky_drawn[0],
            "2nd Place 🥈": lucky_drawn[1],
            "3rd Place 🥉": lucky_drawn[2]
        }
        st.session_state.selected_place = None # 重置點選狀態
        st.success("✨ 得獎名單已成功生成！請在下方揭曉！")

# --- 第二步：點選名次揭曉 ---
if st.session_state.winners:
    st.write("---")
    st.subheader("2. 點擊名次揭曉得獎者！")
    
    # 建立三欄式按鈕
    col1, col2, col3 = st.columns(3)
    
    with col3:
        if st.button("🥉 揭曉第三名"):
            st.session_state.selected_place = "3rd Place 🥉"
    with col2:
        if st.button("🥈 揭曉第二名"):
            st.session_state.selected_place = "2nd Place 🥈"
    with col1:
        if st.button("🥇 揭曉第一名"):
            st.session_state.selected_place = "1st Place 🥇"

    # --- 第三步：熱烈的歡迎畫面 ---
    if st.session_state.selected_place:
        current_place = st.session_state.selected_place
        winner_name = st.session_state.winners[current_place]
        
        # 觸發噴紙花特效（非常熱烈！）
        confetti()
        
        # 顯示歡迎畫面
        st.write("---")
        st.balloons() # 同步飄起氣球
        
        # 使用 HTML 豐富視覺效果
        st.markdown(
            f"""
            <div style="background-color:#FFF3CD; padding: 30px; border-radius: 15px; border-left: 10px solid #FFD700; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <h1 style="color: #856404; font-size: 50px; margin-bottom: 10px;">🎉 CONGRATULATIONS! 🎉</h1>
                <h2 style="color: #1b1e21; font-size: 30px;">{current_place}</h2>
                <h1 style="color: #d39e00; font-size: 60px; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; margin-top: 20px;">
                    ✨ {winner_name} ✨
                </h1>
                <p style="font-size: 20px; color: #6c757d; margin-top: 15px;">Let's give them a big round of applause! 👏👏👏</p>
            </div>
            """, 
            unsafe_html=True
        )
