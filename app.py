import streamlit as st
import base64
from PIL import Image
import io
import csv

# 設定網頁標題與圖示
st.set_page_config(page_title="2026 I-NMC Award System", page_icon="🏆", layout="centered")

# --- 步驟 1：預設資料庫 (官方 2026 I-NMC 名單) ---
DEFAULT_AWARDS_DATA = {
    "Category X - Malaysia (Mathketeers)": {
        "WINNER 🥇": [{"ch": "黃偉健", "en": "Wong Wai Kin"}],
        "1st RUNNER-UP 🥈": [{"ch": "陳佳恩", "en": "Tan Jia En"}],
        "2nd RUNNER-UP 🥉": [{"ch": "林俊傑", "en": "Lim Choon Kit"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "李欣怡", "en": "Lee Xin Yee"}, {"ch": "吳嘉誠", "en": "Goh Kah Seng"},
            {"ch": "王淑芬", "en": "Ong Su Fen"}, {"ch": "張家豪", "en": "Chong Kah How"},
            {"ch": "許紫晴", "en": "Koh Tze Ching"}, {"ch": "曾偉翔", "en": "Chan Wai Siang"},
            {"ch": "鄭子睿", "en": "Teh Tze Chui"}, {"ch": "劉志明", "en": "Liew Chee Ming"},
            {"ch": "蔡宇軒", "en": "Chua Yi Hin"}, {"ch": "郭美玲", "en": "Kuek Mei Ling"}
        ]
    },
    "Category X - Taiwan (Mathketeers)": {
        "WINNER 🥇": [{"ch": "陳俊宏", "en": "Chun-Hung Chen"}],
        "1st RUNNER-UP 🥈": [{"ch": "林雅雯", "en": "Ya-Wen Lin"}],
        "2nd RUNNER-UP 🥉": [{"ch": "黃建宇", "en": "Chien-Yu Huang"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "張佩珊", "en": "Pei-Shan Chang"}, {"ch": "李柏翰", "en": "Po-Han Lee"},
            {"ch": "王佳蓉", "en": "Chia-Jung Wang"}, {"ch": "吳宗翰", "en": "Tsung-Han Wu"},
            {"ch": "劉詩婷", "en": "Shih-Ting Liu"}, {"ch": "蔡宇軒", "en": "Yu-Hsuan Tsai"},
            {"ch": "楊凱文", "en": "Kai-Wen Yang"}, {"ch": "許家豪", "en": "Chia-Hao Hsu"},
            {"ch": "鄭欣儀", "en": "Hsin-I Cheng"}, {"ch": "謝孟哲", "en": "Meng-Che Hsieh"}
        ]
    },
    "Category Y - Malaysia (Theory of Everything)": {
        "WINNER 🥇": [{"ch": "陳家輝", "en": "Gary Tan Kah Hui"}],
        "1st RUNNER-UP 🥈": [{"ch": "林美玲", "en": "May Lim Bee Leng"}],
        "2nd RUNNER-UP 🥉": [{"ch": "李振豪", "en": "Jason Lee Chin How"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "吳淑珍", "en": "Jane Goh Suat Chen"}, {"ch": "張國榮", "en": "Leslie Chong Kok Weng"},
            {"ch": "曾慧敏", "en": "Amanda Chan Wai Mun"}, {"ch": "許俊傑", "en": "Jack Koh Choon Kit"},
            {"ch": "劉雪芬", "en": "Shirley Liew Suet Fun"}, {"ch": "蔡嘉誠", "en": "Aaron Chua Kah Seng"},
            {"ch": "何佩瑜", "en": "Fiona Ho Pui Yee"}, {"ch": "張凱文", "en": "Calvin Teo Kai Wen"}
        ]
    },
    "Category Y - Taiwan (Theory of Everything)": {
        "WINNER 🥇": [{"ch": "陳怡君", "en": "Yi-Chun Chen"}],
        "1st RUNNER-UP 🥈": [{"ch": "林冠宇", "en": "Kuan-Yu Lin"}],
        "2nd RUNNER-UP 🥉": [{"ch": "黃柏翰", "en": "Po-Han Huang"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "李宗翰", "en": "Tsung-Han Li"}, {"ch": "吳佳蓉", "en": "Chia-Jung Wu"},
            {"ch": "劉宇軒", "en": "Yu-Hsuan Liu"}, {"ch": "蔡孟哲", "en": "Meng-Che Tsai"},
            {"ch": "楊詩婷", "en": "Shih-Ting Yang"}, {"ch": "許家豪", "en": "Chia-Hao Hsu"},
            {"ch": "鄭心怡", "en": "Hsin-I Cheng"}, {"ch": "謝承恩", "en": "Cheng-En Hsieh"}
        ]
    },
    "Category Z - Malaysia (Running Math)": {
        "WINNER 🥇": [{"ch": "葉子健", "en": "Ken Yap Tze Kin"}],
        "1st RUNNER-UP 🥈": [{"ch": "郭麗萍", "en": "Lily Kuek Lee Peng"}],
        "2nd RUNNER-UP 🥉": [{"ch": "洪俊賢", "en": "Ivan Ang Choon Kheng"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "鄭偉杰", "en": "Ryan Tay Wai Kit"}, {"ch": "潘宇恆", "en": "Ian Poon Yee Heng"},
            {"ch": "梁嘉欣", "en": "Carmen Leong Kah Yan"}, {"ch": "沈宇軒", "en": "Shawn Sim Yee Hin"},
            {"ch": "彭佳恩", "en": "Joanne Pang Jia En"}, {"ch": "羅俊宇", "en": "Lucas Loh Choon Yee"},
            {"ch": "賴美君", "en": "Michelle Lai Mee Kuen"}, {"ch": "馮健明", "en": "Daniel Fong Kin Ming"}
        ]
    },
    "Category Z - Taiwan (Running Math)": {
        "WINNER 🥇": [{"ch": "郭俊宏", "en": "Chun-Hung Kuo"}],
        "1st RUNNER-UP 🥈": [{"ch": "曾菀婷", "en": "Wan-Ting Tseng"}],
        "2nd RUNNER-UP 🥉": [{"ch": "洪宇恆", "en": "Yu-Heng Hung"}],
        "Top 25% (Q1) 🎖️": [
            {"ch": "蘇奕翔", "en": "Yi-Hsiang Su"}, {"ch": "葉柏廷", "en": "Po-Ting Yeh"},
            {"ch": "高嘉妤", "en": "Chia-Yu Kao"}, {"ch": "莊智淵", "en": "Chih-Yuan Chuang"},
            {"ch": "侯佩珊", "en": "Pei-Shan Hou"}, {"ch": "邱子軒", "en": "Tzu-Hsuan Chiu"},
            {"ch": "賴冠廷", "en": "Kuan-Ting Lai"}, {"ch": "簡宇翔", "en": "Yu-Hsiang Chien"}
        ]
    }
}

# --- 步驟 2：優化版圖片處理函數 ---
@st.cache_data
def get_optimized_image_base64(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    img.thumbnail((1500, 2000), Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"

# --- 步驟 3：側邊欄設置 (匯入名單與背景圖) ---
st.sidebar.header("📁 1. 匯入得獎名單")

# 產生範例 CSV (使用 utf-8-sig 讓 Excel 繁體中文不會亂碼)
sample_csv = "Category,Rank,Chinese Name,English Name\n"
sample_csv += "示範賽事 A,WINNER 🥇,王小明,Wang Xiao Ming\n"
sample_csv += "示範賽事 A,1st RUNNER-UP 🥈,陳美麗,Chen Mei Li\n"
sample_csv += "示範賽事 A,2nd RUNNER-UP 🥉,張大山,Zhang Da Shan\n"
sample_csv += "示範賽事 A,Top 25% (Q1) 🎖️,李四,Li Si\n"
sample_csv += "示範賽事 A,Top 25% (Q1) 🎖️,林五,Lin Wu\n"
st.sidebar.download_button("📥 下載範例 CSV 格式", data=sample_csv.encode('utf-8-sig'), file_name="sample_winners.csv", mime="text/csv")

# 處理檔案上傳
uploaded_csv = st.sidebar.file_uploader("上傳您的得獎名單 (CSV)", type=["csv"])
AWARDS_DATA = DEFAULT_AWARDS_DATA # 預設使用官方資料

if uploaded_csv is not None:
    try:
        content = uploaded_csv.getvalue().decode('utf-8-sig').splitlines()
        reader = csv.DictReader(content)
        custom_data = {}
        for row in reader:
            cat = row.get("Category", "").strip()
            rank = row.get("Rank", "").strip()
            ch = row.get("Chinese Name", "").strip()
            en = row.get("English Name", "").strip()
            
            if not cat or not rank: continue
            if cat not in custom_data: custom_data[cat] = {}
            if rank not in custom_data[cat]: custom_data[cat][rank] = []
            
            custom_data[cat][rank].append({"ch": ch, "en": en})
            
        if custom_data:
            AWARDS_DATA = custom_data
            st.sidebar.success("✅ 成功載入自訂得獎名單！")
    except Exception as e:
        st.sidebar.error(f"❌ 讀取檔案失敗，請確保格式正確：{e}")

st.sidebar.markdown("---")
st.sidebar.header("🎨 2. 獎狀外觀與列印")
bg_option = st.sidebar.radio("獎狀背景選擇：", ["預設白金質感底色", "使用上傳背景圖"])
uploaded_bg = st.sidebar.file_uploader("上傳背景圖 (建議 A4 比例)", type=["jpg", "png", "jpeg"])

if st.sidebar.button("🖨️ 批次下載 / 存為 PDF"):
    st.sidebar.info("💡 請在彈出的視窗中選擇「另存為 PDF」。")
    st.components.v1.html("<script>window.print();</script>", height=0)

# --- 步驟 4：主畫面選擇 ---
st.title("🏆 榮耀頒獎典禮系統")
selected_category = st.selectbox("🎯 選擇賽事類別：", list(AWARDS_DATA.keys()))
current_winners = AWARDS_DATA[selected_category]

st.write("---")
st.subheader("🎉 揭曉名次")
ranks = list(current_winners.keys())
cols = st.columns(len(ranks) if len(ranks) > 0 else 1)

if "selected_rank" not in st.session_state: st.session_state.selected_rank = None

for i, rank in enumerate(ranks):
    if cols[i % len(cols)].button(rank):
        st.session_state.selected_rank = rank
        if "Q1" not in rank: 
            st.snow()
            st.balloons()

# --- 步驟 5：渲染獎狀 (動態加入賽事名稱) ---
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

    html_content = f"""<style>
@media print {{
    body * {{ visibility: hidden; }}
    .print-area, .print-area * {{ visibility: visible; }}
    .print-area {{ position: absolute; left: 0; top: 0; width: 100%; }}
    .page-break {{ page-break-after: always; }}
}}
{custom_css}
</style>
<div class="print-area">
"""

    for idx, w in enumerate(winners):
        # 注意 HTML 中加入了 <div style="background-color: {main_color}; ...>{selected_category}</div> 顯示賽事名稱
        cert_html = f"""<div class="cert-container" style="width: 100%; min-height: 700px; padding: 40px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; margin-bottom: 30px; page-break-inside: avoid; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
<div style="background-color: rgba(255, 255, 255, 0.92); width: 90%; padding: 40px 30px; border-radius: 12px; border: 3px double {main_color}; text-align: center; box-shadow: 0px 5px 20px rgba(0,0,0,0.1);">
<h1 style="color: {main_color}; margin: 0; font-size: 38px; font-family: 'Times New Roman', serif;">CERTIFICATE OF AWARD</h1>
<p style="letter-spacing: 2px; color: #666; font-size: 14px; margin-bottom: 5px;">2026 I-NMC INTERNATIONAL COMPETITION</p>

<div style="background-color: {main_color}; color: #ffffff; display: inline-block; padding: 6px 25px; border-radius: 30px; font-size: 15px; font-weight: bold; letter-spacing: 1px; margin: 15px 0;">
    {selected_category}
</div>

<p style="margin-top: 15px; font-style: italic; color: #777; font-size: 18px;">This is to certify that the award for</p>
<h2 style="color: #222; text-transform: uppercase; font-size: 32px; margin: 10px 0;">{rank}</h2>
<p style="color: #777; font-style: italic; font-size: 18px;">is proudly presented to</p>
<div style="margin: 30px 0;">
<div style="font-size: 50px; font-weight: 900; color: #111;">{w['ch']}</div>
<div style="font-size: 26px; font-style: italic; color: #555; margin-top: 5px;">{w['en']}</div>
</div>
<div style="margin-top: 30px; border-top: 1px solid #ccc; padding-top: 15px; font-size: 14px; color: #888;">
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
