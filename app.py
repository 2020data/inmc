import streamlit as st
import base64
from PIL import Image
import io
import csv
import requests

# 設定網頁標題與圖示
st.set_page_config(page_title="2026 I-NMC Live Award System", page_icon="🏆", layout="wide")

# --- 步驟 1：預設官方資料庫 ---
DEFAULT_AWARDS_DATA = {
    "Category X - Malaysia": {
        "WINNER 🥇": [{"ch": "黃偉健", "en": "Wong Wai Kin", "cat_name": "Mathketeers - Group of 3"}],
        "1st RUNNER-UP 🥈": [{"ch": "陳佳恩", "en": "Tan Jia En", "cat_name": "Mathketeers - Group of 3"}],
        "2nd RUNNER-UP 🥉": [{"ch": "林俊傑", "en": "Lim Choon Kit", "cat_name": "Mathketeers - Group of 3"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "李欣怡", "en": "Lee Xin Yee", "cat_name": "Mathketeers - Group of 3"},
            {"ch": "吳嘉誠", "en": "Goh Kah Seng", "cat_name": "Mathketeers - Group of 3"}
        ]
    }
}

# --- 步驟 2：核心功能函數 ---
def convert_to_csv_url(url):
    if "docs.google.com/spreadsheets" in url:
        base_part = url.split("/edit")[0]
        gid_part = "gid=" + (url.split("gid=")[1].split("&")[0] if "gid=" in url else "0")
        return f"{base_part}/export?format=csv&{gid_part}"
    return url

@st.cache_data(ttl=10)
def load_live_sheet(url):
    try:
        res = requests.get(convert_to_csv_url(url))
        if res.status_code != 200: return None
        reader = csv.DictReader(res.content.decode('utf-8-sig').splitlines())
        live_data = {}
        for row in reader:
            cat, rank = row.get("Category", "").strip(), row.get("Rank", "").strip()
            if not cat or not rank: continue
            if cat not in live_data: live_data[cat] = {}
            if rank not in live_data[cat]: live_data[cat][rank] = []
            live_data[cat][rank].append({
                "ch": row.get("Chinese Name", "").strip(),
                "en": row.get("English Name", "").strip(),
                "cat_name": row.get("Category Name", "").strip()
            })
        return live_data
    except: return None

# --- 步驟 3：UI 設定 ---
st.sidebar.header("🌐 雲端連動設置")
sheet_url = st.sidebar.text_input("Google 試算表連結：")
AWARDS_DATA = load_live_sheet(sheet_url) if sheet_url else DEFAULT_AWARDS_DATA

st.title("🏆 2026 I-NMC Live Award System")
selected_category = st.selectbox("🎯 選擇賽事類別：", list(AWARDS_DATA.keys()))
current_winners = AWARDS_DATA[selected_category]

st.subheader("🎉 揭曉名次")
ranks = list(current_winners.keys())
cols = st.columns(len(ranks) if len(ranks) > 0 else 1)

if "selected_rank" not in st.session_state: st.session_state.selected_rank = None

for i, rank in enumerate(ranks):
    if cols[i % len(cols)].button(rank):
        st.session_state.selected_rank = rank

# --- 步驟 4：獎狀渲染 ---
if st.session_state.selected_rank and st.session_state.selected_rank in current_winners:
    rank = st.session_state.selected_rank
    winners = current_winners[rank]
    main_color = "#D4AF37" if "WINNER" in rank else "#B4B4B4" if "1st" in rank else "#CD7F32" if "2nd" in rank else "#4A90E2"
    
    css = f"""<style>
        .cert {{ width: 210mm; height: 297mm; padding: 20mm; margin: auto; border: 5px double {main_color}; 
                 display: flex; flex-direction: column; align-items: center; justify-content: space-between; 
                 font-family: 'Arial', sans-serif; background: #fdfbf7; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
    </style>"""
    
    full_html = css
    for w in winners:
        full_html += f"""
        <div class="cert">
            <h1>Congratulations</h1>
            <p>2026 International-National Mathematics Competition</p>
            <div style="background:{main_color}; color:white; padding:10px; border-radius:20px;">{selected_category}</div>
            <h2 style="font-size:40px;">{rank}</h2>
            <div style="text-align:center;">
                <div style="font-size:60px; font-weight:bold;">{w['ch']}</div>
                <div style="font-size:30px; font-style:italic;">{w['en']}</div>
            </div>
            <p>Organized by I-NMC Committee & UTAR Malaysia</p>
        </div><br>"""
    
    st.components.v1.html(full_html, height=1200, scrolling=True)
