import streamlit as st
import base64
from PIL import Image
import io
import csv
import requests

# 設定網頁標題與圖示
st.set_page_config(page_title="2026 I-NMC Live Award System", page_icon="🏆", layout="centered")

# --- 步驟 1：預設官方資料庫 (包含 Category 與 Category Name 欄位) ---
DEFAULT_AWARDS_DATA = {
    "Category X - Malaysia": {
        "WINNER 🥇": [{"ch": "黃偉健", "en": "Wong Wai Kin", "cat_name": "Mathketeers - Group of 3"}],
        "1st RUNNER-UP 🥈": [{"ch": "陳佳恩", "en": "Tan Jia En", "cat_name": "Mathketeers - Group of 3"}],
        "2nd RUNNER-UP 🥉": [{"ch": "林俊傑", "en": "Lim Choon Kit", "cat_name": "Mathketeers - Group of 3"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "李欣怡", "en": "Lee Xin Yee", "cat_name": "Mathketeers - Group of 3"},
            {"ch": "吳嘉誠", "en": "Goh Kah Seng", "cat_name": "Mathketeers - Group of 3"},
            {"ch": "王淑芬", "en": "Ong Su Fen", "cat_name": "Mathketeers - Group of 3"},
            {"ch": "張家豪", "en": "Chong Kah How", "cat_name": "Mathketeers - Group of 3"}
        ]
    },
    "Category X - Taiwan": {
        "WINNER 🥇": [{"ch": "陳俊宏", "en": "Chun-Hung Chen", "cat_name": "Mathketeers - Group of 3"}],
        "1st RUNNER-UP 🥈": [{"ch": "林雅雯", "en": "Ya-Wen Lin", "cat_name": "Mathketeers - Group of 3"}],
        "2nd RUNNER-UP 🥉": [{"ch": "黃建宇", "en": "Chien-Yu Huang", "cat_name": "Mathketeers - Group of 3"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "張佩珊", "en": "Pei-Shan Chang", "cat_name": "Mathketeers - Group of 3"},
            {"ch": "李柏翰", "en": "Po-Han Lee", "cat_name": "Mathketeers - Group of 3"}
        ]
    },
    "Category Y - Malaysia": {
        "WINNER 🥇": [{"ch": "陳家輝", "en": "Gary Tan Kah Hui", "cat_name": "Theory of Everything - Individual Competition"}],
        "1st RUNNER-UP 🥈": [{"ch": "林美玲", "en": "May Lim Bee Leng", "cat_name": "Theory of Everything - Individual Competition"}],
        "2nd RUNNER-UP 🥉": [{"ch": "李振豪", "en": "Jason Lee Chin How", "cat_name": "Theory of Everything - Individual Competition"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "吳淑珍", "en": "Jane Goh Suat Chen", "cat_name": "Theory of Everything - Individual Competition"},
            {"ch": "張國榮", "en": "Leslie Chong Kok Weng", "cat_name": "Theory of Everything - Individual Competition"}
        ]
    },
    "Category Y - Taiwan": {
        "WINNER 🥇": [{"ch": "陳怡君", "en": "Yi-Chun Chen", "cat_name": "Theory of Everything - Individual Competition"}],
        "1st RUNNER-UP 🥈": [{"ch": "林冠宇", "en": "Kuan-Yu Lin", "cat_name": "Theory of Everything - Individual Competition"}],
        "2nd RUNNER-UP 🥉": [{"ch": "黃柏翰", "en": "Po-Han Huang", "cat_name": "Theory of Everything - Individual Competition"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "李宗翰", "en": "Tsung-Han Li", "cat_name": "Theory of Everything - Individual Competition"},
            {"ch": "吳佳蓉", "en": "Chia-Jung Wu", "cat_name": "Theory of Everything - Individual Competition"}
        ]
    },
    "Category Z - Malaysia": {
        "WINNER 🥇": [{"ch": "葉子健", "en": "Ken Yap Tze Kin", "cat_name": "Running Math - Individual Timed Event"}],
        "1st RUNNER-UP 🥈": [{"ch": "郭麗萍", "en": "Lily Kuek Lee Peng", "cat_name": "Running Math - Individual Timed Event"}],
        "2nd RUNNER-UP 🥉": [{"ch": "洪俊賢", "en": "Ivan Ang Choon Kheng", "cat_name": "Running Math - Individual Timed Event"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "鄭偉杰", "en": "Ryan Tay Wai Kit", "cat_name": "Running Math - Individual Timed Event"},
            {"ch": "潘宇恆", "en": "Ian Poon Yee Heng", "cat_name": "Running Math - Individual Timed Event"}
        ]
    },
    "Category Z - Taiwan": {
        "WINNER 🥇": [{"ch": "郭俊宏", "en": "Chun-Hung Kuo", "cat_name": "Running Math - Individual Timed Event"}],
        "1st RUNNER-UP 🥈": [{"ch": "曾菀婷", "en": "Wan-Ting Tseng", "cat_name": "Running Math - Individual Timed Event"}],
        "2nd RUNNER-UP 🥉": [{"ch": "洪宇恆", "en": "Yu-Heng Hung", "cat_name": "Running Math - Individual Timed Event"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "蘇奕翔", "en": "Yi-Hsiang Su", "cat_name": "Running Math - Individual Timed Event"},
            {"ch": "葉柏廷", "en": "Po-Ting Yeh", "cat_name": "Running Math - Individual Timed Event"}
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
            cat_name = row.get("Category Name", "").strip()
            rank = row.get("Rank", "").strip()
            ch = row.get("Chinese Name", "").strip()
            en = row.get("English Name", "").strip()
            if not cat or not rank: continue
            if cat not in live_data: live_data[cat] = {}
            if rank not in live_data[cat]: live_data[cat][rank] = []
            live_data[cat][rank].append({"ch": ch, "en": en, "cat_name": cat_name})
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

# --- 步驟 3：側邊欄雲端連動與範例下載 ---
st.sidebar.header("🌐 雲端連動設置")
sheet_url = st.sidebar.text_input("請輸入 Google 試算表連結：", placeholder="https://docs.google.com/spreadsheets/d/.../edit")

# 新增 Category Name 欄位的範例 CSV
sample_csv = "Category,Category Name,Rank,Chinese Name,English Name\n"
sample_csv += "Category X - Malaysia,Mathketeers - Group of 3,WINNER 🥇,王小明,Wang Xiao Ming\n"
sample_csv += "Category Y - Taiwan,Theory of Everything - Individual Competition,1st RUNNER-UP 🥈,陳美麗,Chen Mei Li\n"
st.sidebar.download_button("📥 下載全新範例 CSV 格式", data=sample_csv.encode('utf-8-sig'), file_name="sample_winners_v2.csv", mime="text/csv")

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

if st.sidebar.button("🖨️ 批次下載 / 存為 PDF"):
    st.sidebar.info("💡 請在彈出的系統列印視窗中，將目標列印機選擇為「另存為 PDF」。")
    st.components.v1.html("<script>window.parent.print();</script>", height=0)

# --- 步驟 4：主畫面選擇 ---
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

# --- 步驟 5：滿版 A4 列印與雙防護罩渲染 ---
if st.session_state.selected_rank and st.session_state.selected_rank in current_winners:
    rank = st.session_state.selected_rank
    winners = current_winners[rank]
    
    main_color = "#D4AF37" if "WINNER" in rank else "#B4B4B4" if "1st" in rank else "#CD7F32" if "2nd" in rank else "#4A90E2"
    
    custom_css = ""
    if bg_option == "使用上傳背景圖" and uploaded_bg:
        img_b64 = get_optimized_image_base64(uploaded_bg.getvalue())
        custom_css = f".cert-container {{ background-image: url('{img_b64}'); background-size: 100% 100%; background-repeat: no-repeat; background-position: center; border: none; }}"
    else:
        custom_css = f".cert-container {{ background: #fdfbf7; border: none; }}"

    # 核心修正：利用 @page 與絕對毫米單位控制，達成 PDF 列印時「滿版且精準留 12mm 邊框」
    html_content = f"""<style>
@page {{
    size: A4 portrait;
    margin: 12mm !important; /* 決定 PDF 產出時的外圍留白邊框厚度 */
}}
@media print {{
    [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"], .stButton, footer, hr {{ 
        display: none !important; 
    }}
    .print-area {{ 
        display: block !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    .cert-container {{ 
        width: 100% !important;
        height: 270mm !important; /* 精準符合 A4 高度扣除上下邊距後的滿版尺寸 */
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin: 0 auto !important;
        box-shadow: none !important;
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
# --- 調整字體大小變數 ---
font_config = {
    "h1": "42px",       # Congratulations 大標題
    "rank": "36px",     # 名次 (Winner...)
    "name_ch": "56px",  # 中文姓名
    "name_en": "32px",  # 英文姓名
    "cat_label": "16px" # 類別標籤
}

# --- 姓名渲染邏輯 ---
name_display = ""
if w['ch'] and w['en']:
    # 中英都有：上下排列，字體正常
    name_display = f"""
    <div style="margin: 25px 0;">
        <div style="font-size: {font_config['name_ch']}; font-weight: 900; color: #111; font-family: 'Microsoft JhengHei', sans-serif;">{w['ch']}</div>
        <div style="font-size: {font_config['name_en']}; font-style: italic; color: #555; margin-top: 5px; font-family: 'Times New Roman', serif;">{w['en']}</div>
    </div>"""
else:
    # 只有其中一個：放大顯示，垂直置中
    single_name = w['ch'] if w['ch'] else w['en']
    name_display = f"""
    <div style="margin: 40px 0;">
        <div style="font-size: 68px; font-weight: 900; color: #111; font-family: 'Microsoft JhengHei', sans-serif;">{single_name}</div>
    </div>"""
    
    for idx, w in enumerate(winners):
        # 讀取 Category Name 欄位
        cat_name_value = w.get("cat_name", "").strip()
    
    cert_html = f"""<div class="cert-container" style="width: 100%; min-height: 720px; padding: 40px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; margin-bottom: 30px; page-break-inside: avoid; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <div style="background-color: rgba(255, 255, 255, 0.93); width: 92%; height: 92%; padding: 40px 30px; border-radius: 12px; border: 3px double {main_color}; text-align: center; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
        <div style="width: 100%;">
            <h1 style="color: {main_color}; margin: 0; font-size: {font_config['h1']}; font-family: 'Times New Roman', serif; font-weight: bold; letter-spacing: 1px;">Congratulations</h1>
            <p style="letter-spacing: 2px; color: #666; font-size: 13px; margin: 5px 0 15px 0;">2026 International-National Mathematics Competition</p>
            
            <div style="background-color: {main_color}; color: #ffffff; display: inline-block; padding: 6px 24px; border-radius: 30px; font-size: {font_config['cat_label']}; font-weight: bold; letter-spacing: 1px; max-width: 90%; word-break: break-word;">
                {selected_category}
            </div>
            <div style="height: 8px;"></div>
            <div style="background-color: #f5f5f7; color: {main_color}; display: inline-block; padding: 5px 22px; border-radius: 30px; font-size: {font_config['cat_label']}; font-weight: 800; border: 1px solid {main_color};">
                {cat_name_value}
            </div>
        </div>

        <div style="width: 100%;">
            <p style="margin-top: 10px; font-style: italic; color: #777; font-size: 18px; margin-bottom: 5px;">This is to certify that the award for</p>
            <h2 style="color: #222; text-transform: uppercase; font-size: {font_config['rank']}; margin: 5px 0; font-weight: 800; letter-spacing: 0.5px;">{rank}</h2>
            <p style="color: #777; font-style: italic; font-size: 18px; margin-bottom: 0;">is proudly presented to</p>
            {name_display}
        </div>

        <div style="width: 100%;">
            <div style="border-top: 1px solid #ccc; padding-top: 15px; font-size: 14px; color: #888; font-weight: 500;">
                Organized by I-NMC Committee & UTAR Malaysia
            </div>
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
