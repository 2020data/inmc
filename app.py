import streamlit as st
import random

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
    parts = line.strip().split()
    if len(parts) > 1:
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
        
        # 這裡會同時噴發「滿天明星亮片」與「滿天上升氣球」，營造極度熱烈氣氛！
        st.snow()
        st.balloons()
        
        # 顯示奢華歡迎畫面
        # 顯示奢華歡迎畫面
        st.write("---")
        st.markdown(
            f"""
            <div style="background-color:#FFF3CD; padding: 40px 20px; border-radius: 20px; border: 5px solid #FFD700; text-align: center; box-shadow: 0px 10px 25px rgba(0,0,0,0.15); animation: pulse 2s infinite;">
                <h1 style="color: #856404; font-size: 55px; margin-bottom: 10px; font-family: 'Arial Black', sans-serif;">🎉 CONGRATULATIONS! 🎉</h1>
                <h2 style="color: #495057; font-size: 32px; letter-spacing: 1px; font-weight: bold;">{current_place}</h2>
                <hr style="border: 1px dashed #FFD700; width: 60%; margin: 20px auto;">
                <h1 style="color: #d39e00; font-size: 65px; font-weight: 900; letter-spacing: 3px; text-transform: uppercase; margin: 20px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                    ✨ {winner_name} ✨
                </h1>
                <p style="font-size: 22px; color: #6c757d; margin-top: 15px; font-style: italic;">Let's give them a big round of applause! 👏👏👏</p>
            </div>
            """, 
            unsafe_allow_html=True  # 👉 這裡修正為 unsafe_allow_html
        )
