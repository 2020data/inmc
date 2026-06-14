import streamlit as st
import base64
from PIL import Image
import io
import csv
import requests

# 設定網頁標題與圖示
st.set_page_config(page_title="2026 I-NMC Live Award System", page_icon="🏆", layout="centered")

# --- 步驟 1：預設官方資料庫 (若未連結 Google 表單時作為備用) ---
DEFAULT_AWARDS_DATA = {
    "Category X - Malaysia (Mathketeers)": {
        "WINNER 🥇": [{"ch": "黃偉健", "en": "Wong Wai Kin"}],
        "1st RUNNER-UP 🥈": [{"ch": "陳佳恩", "en": "Tan Jia En"}],
        "2nd RUNNER-UP 🥉": [{"ch": "林俊傑", "en": "Lim Choon Kit"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "李欣怡", "en": "Lee Xin Yee"}, {"ch": "吳嘉誠", "en": "Goh Kah Seng"},
            {"ch": "王淑芬", "en": "Ong Su Fen"}, {"ch": "張家豪", "en": "Chong Kah How"}
        ]
    },
    "Category X - Taiwan (Mathketeers)": {
        "WINNER 🥇": [{"ch": "陳俊宏", "en": "Chun-Hung Chen"}],
        "1st RUNNER-UP 🥈": [{"ch": "林雅雯", "en": "Ya-Wen Lin"}],
        "2nd RUNNER-UP 🥉": [{"ch": "黃建宇", "en": "Chien-Yu Huang"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "張佩珊", "en": "Pei-Shan Chang"}, {"ch": "李柏翰", "en": "Po-Han Lee"}
        ]
    },
    "Category Y - Malaysia (Theory of Everything)": {
        "WINNER 🥇": [{"ch": "陳家輝", "en": "Gary Tan Kah Hui"}],
        "1st RUNNER-UP 🥈": [{"ch": "林美玲", "en": "May Lim Bee Leng"}],
        "2nd RUNNER-UP 🥉": [{"ch": "李振豪", "en": "Jason Lee Chin How"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "吳淑珍", "en": "Jane Goh Suat Chen"}, {"ch": "張國榮", "en": "Leslie Chong Kok Weng"}
        ]
    },
    "Category Y - Taiwan (Theory of Everything)": {
        "WINNER 🥇": [{"ch": "陳怡君", "en": "Yi-Chun Chen"}],
        "1st RUNNER-UP 🥈": [{"ch": "林冠宇", "en": "Kuan-Yu Lin"}],
        "2nd RUNNER-UP 🥉": [{"ch": "黃柏翰", "en": "Po-Han Huang"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "李宗翰", "en": "Tsung-Han Li"}, {"ch": "吳佳蓉", "en": "Chia-Jung Wu"}
        ]
    },
    "Category Z - Malaysia (Running Math)": {
        "WINNER 🥇": [{"ch": "葉子健", "en": "Ken Yap Tze Kin"}],
        "1st RUNNER-UP 🥈": [{"ch": "郭麗萍", "en": "Lily Kuek Lee Peng"}],
        "2nd RUNNER-UP 🥉": [{"ch": "洪俊賢", "en": "Ivan Ang Choon Kheng"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "鄭偉杰", "en": "Ryan Tay Wai Kit"}, {"ch": "潘宇恆", "en": "Ian Poon Yee Heng"}
        ]
    },
    "Category Z - Taiwan (Running Math)": {
        "WINNER 🥇": [{"ch": "郭俊宏", "en": "Chun-Hung Kuo"}],
        "1st RUNNER-UP 🥈": [{"ch": "曾菀婷", "en": "Wan-Ting Tseng"}],
        "2nd RUNNER-UP 🥉": [{"ch": "洪宇恆", "en": "Yu-Heng Hung"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "蘇奕翔", "en": "Yi-Hsiang Su"}, {"ch": "葉柏廷", "en": "Po-Ting Yeh"}
        ]
    }
}

# --- 步驟 2：雲端網址轉換與讀取 ---
def convert_to_csv_url(url):
    if "docs.google.com/spreadsheets" in url:
        try:
            base_part = url.split("/edit")[0]
            gid_part = "gid=0"
            if "gid=" in url:
                gid_part = "gid=" + url.split("gid=")[1].split("&")[0]
            return f"{base_part}/export?format=csv&{gid_part}"
        except:
            return url
    return url

@st.cache_data(ttl=10)
def load_live_sheet(url):
    try:
        csv_url = convert_to_csv_url(url)
        res = requests.get(csv_url)
        if res.status_code != 200: return None
        content = res.content.decode('utf-8-sig').splitlines()
        reader = csv.DictReader(content)
        live_data = {}
        for row in reader:
            cat = row.get("Category", "").strip()
            rank = row.get("Rank", "").strip()
            ch = row.get("Chinese Name", "").strip()
            en = row.get("English Name", "").strip()
            if not cat or not rank: continue
            if cat not in live_data: live_data[cat] = {}
            if rank not in live_data[cat]: live_data[cat][rank] = []
            live_data[cat][rank].append({"ch": ch, "en": en})
        return live_data
    except:
        return None

@st.cache_data
def get_optimized_image_base64(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    img.thumbnail((1500, 2000), Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"

# --- 步驟 3：側邊欄雲端連動與優化列印設置 ---
st.sidebar.header("🌐 雲端連動設置")
sheet_url = st.sidebar.text_input("請輸入 Google 試算表連結：", placeholder="https://docs.google.com/spreadsheets/d/.../edit")

AWARDS_DATA = DEFAULT_AWARDS_DATA
if sheet_url:
    live_res = load_live_sheet(sheet_url)
    if live_res:
        AWARDS_DATA = live_res
        st.sidebar.success("🚀 已即時連線 Google 表單資料庫！")
    else:
        st.sidebar.error("❌ 無法讀取，請檢查雲端共用權限是否開啟。")

st.sidebar.markdown("---")
st.sidebar.header("🎨 獎狀外觀與列印")
bg_option = st.sidebar.radio("獎狀背景選擇：", ["官方預設樣式", "使用上傳背景圖"])
uploaded_bg = st.sidebar.file_uploader("上傳背景圖 (建議 A4 比例)", type=["jpg", "png", "jpeg"])

# 核心修復：使用 window.parent.print() 突破 Iframe 限制，並使用 display:none 精準隱藏 Streamlit UI 
if st.sidebar.button("🖨️ 批次下載 / 存為 PDF"):
    st.sidebar.info("💡 請在彈出的系統列印視窗中，將目標列印機選擇為「另存為 PDF」。")
    st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- 步驟 4：主畫面動態選擇 ---
st.title("🏆 2026 I-NMC Live Award System")
selected_category = st.selectbox("🎯 1. 選擇賽事類別：", list(AWARDS_DATA.keys()))
current_winners = AWARDS_DATA[selected_category]

st.write("---")
st.subheader("🎉 2. 揭曉名次")
ranks = list(current_winners.keys())
cols = st.columns(len(ranks) if len(ranks) > 0 else 1)

if "selected_rank" not in st.session_state: st.session_state.selected_rank = None

for i, rank in enumerate(ranks):
    if cols[i % len(cols)].button(rank):
        st.session_state.selected_rank = rank
        if "Q1" not in rank: 
            st.snow()
            st.balloons()

# --- 步驟 5：精密防重疊與自動斷行獎狀渲染 ---
if st.session_state.selected_rank and st.session_state.selected_rank in current_winners:
    rank = st.session_state.selected_rank
    winners = current_winners[rank]
    
    main_color = "#D4AF37" if "WINNER" in rank else "#B4B4B4" if "1st" in rank else "#CD7F32" if "2nd" in rank else "#4A90E2"
    
    custom_css = ""
    if bg_option == "使用上傳背景圖" and uploaded_bg:
        img_b64 = get_optimized_image_base64(uploaded_bg.getvalue())
        custom_css = f".cert-container {{ background-image: url('{img_b64}'); background-size: cover; background-position: center; border: none; }}"
    else:
        custom_css = f".cert-container {{ background: #fdfbf7; border: none; }}"

    # 核心修復：強效型國王級列印樣式，強制在列印時隱藏 Streamlit 的所有控制面板、按鈕、側邊欄
    html_content = f"""<style>
@media print {{
    [data-testid="stSidebar"], 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"],
    .stButton,
    footer,
    hr {{ 
        display: none !important; 
    }}
    .print-area {{ 
        display: block !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    .page-break {{ 
        page-break-after: always !important; 
        break-after: page !important;
    }}
}}
{custom_css}
</style>
<div class="print-area">
"""

    for idx, w in enumerate(winners):
        # 核心修復：在賽事名稱的 div 中加入了 max-width, word-break, line-height 確保超長名稱自動完美斷行不重疊
        cert_html = f"""<div class="cert-container" style="width: 100%; min-height: 700px; padding: 45px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; margin-bottom: 30px; page-break-inside: avoid; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
<div style="background-color: rgba(255, 255, 255, 0.93); width: 92%; padding: 45px 30px; border-radius: 12px; border: 3px double {main_color}; text-align: center; box-shadow: 0px 5px 20px rgba(0,0,0,0.1); box-sizing: border-box;">
<h1 style="color: {main_color}; margin: 0; font-size: 36px; font-family: 'Times New Roman', serif; font-weight: bold;">CERTIFICATE OF AWARD</h1>
<p style="letter-spacing: 2px; color: #666; font-size: 13px; margin: 5px 0 15px 0;">2026 I-NMC INTERNATIONAL COMPETITION</p>

<div style="background-color: {main_color}; color: #ffffff; display: inline-block; padding: 8px 22px; border-radius: 30px; font-size: 14px; font-weight: bold; letter-spacing: 0.5px; margin-bottom: 10px; max-width: 90%; word-break: break-word; line-height: 1.4;">
    {selected_category}
</div>

<p style="margin-top: 15px; font-style: italic; color: #777; font-size: 18px;">This is to certify that the award for</p>
<h2 style="color: #222; text-transform: uppercase; font-size: 30px; margin: 10px 0; font-weight: 800;">{rank}</h2>
<p style="color: #777; font-style: italic; font-size: 18px;">is proudly presented to</p>

<div style="margin: 30px 0;">
<div style="font-size: 48px; font-weight: 900; color: #111; font-family: 'Microsoft JhengHei', sans-serif;">{w['ch']}</div>
<div style="font-size: 26px; font-style: italic; color: #555; margin-top: 5px; font-family: 'Times New Roman', serif;">{w['en']}</div>
</div>

<div style="margin-top: 35px; border-top: 1px solid #ccc; padding-top: 15px; font-size: 14px; color: #888; font-weight: 500;">
Organized by I-NMC Committee & UTAR Malaysia
</div>
</div>
</div>
"""
        html_content += cert_html
        
        if idx < len(winners) - 1:
            html_content += '<div class="page-break"></div>\n'

    html_content += "</div>"

    st.write("---")
    st.markdown(html_content, unsafe_allow_html=True)
