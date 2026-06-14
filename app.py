import streamlit as st
import base64

# 設定網頁標題與圖示
st.set_page_config(page_title="2026 I-NMC Award System", page_icon="🏆", layout="centered")

# --- 步驟 1：完整資料庫 (含 Top 25% / Q1 名單) ---
AWARDS_DATA = {
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
    }
}

# --- 步驟 2：背景圖處理函數 ---
def get_image_base64(image_file):
    encoded_string = base64.b64encode(image_file.getvalue()).decode()
    return f"data:image/png;base64,{encoded_string}"

# --- 步驟 3：側邊欄設置 (上傳背景與批次列印) ---
st.sidebar.header("🎨 獎狀自定義設置")
bg_option = st.sidebar.radio("獎狀背景選擇：", ["官方預設樣式", "使用上傳背景圖"])
uploaded_bg = st.sidebar.file_uploader("上傳背景圖 (建議 A4 比例)", type=["jpg", "png", "jpeg"])

if st.sidebar.button("🖨️ 批次下載 / 存為 PDF"):
    st.sidebar.info("💡 請在彈出的視窗中選擇「另存為 PDF」，即可一次下載所有產生的獎狀！")
    st.components.v1.html("<script>window.print();</script>", height=0)

# --- 步驟 4：主畫面選擇 ---
st.title("🏆 2026 I-NMC Award Ceremony")
selected_category = st.selectbox("1. 選擇賽事類別：", list(AWARDS_DATA.keys()))
current_winners = AWARDS_DATA[selected_category]

st.write("---")
st.subheader("2. 揭曉名次")
cols = st.columns(4)
ranks = list(current_winners.keys())

# 使用 Session State 紀錄點擊
if "selected_rank" not in st.session_state: st.session_state.selected_rank = None

for i, rank in enumerate(ranks):
    if cols[i].button(rank):
        st.session_state.selected_rank = rank
        if "Q1" not in rank: # 前三名才有強烈特效
            st.snow()
            st.balloons()

# --- 步驟 5：渲染獎狀 (修復縮排問題並支援批次產生) ---
if st.session_state.selected_rank:
    rank = st.session_state.selected_rank
    winners = current_winners[rank]
    
    # 樣式定義
    main_color = "#D4AF37" if "WINNER" in rank else "#B4B4B4" if "1st" in rank else "#CD7F32" if "2nd" in rank else "#4A90E2"
    
    # 如果有上傳背景，則將 HTML 結構改為背景圖覆蓋
    if bg_option == "使用上傳背景圖" and uploaded_bg:
        img_b64 = get_image_base64(uploaded_bg)
        bg_style = f"background-image: url('{img_b64}'); background-size: cover; background-position: center; border: none;"
    else:
        bg_style = f"background: #fdfbf7; border: 10px double {main_color};"

    # 建立整體 HTML 的開頭 (包含 CSS 列印分頁設定)
    # 注意：這裡刻意不縮排，防止 Markdown 誤判
    html_content = f"""<style>
@media print {{
    body * {{ visibility: hidden; }}
    .print-area, .print-area * {{ visibility: visible; }}
    .print-area {{ position: absolute; left: 0; top: 0; width: 100%; }}
    .page-break {{ page-break-after: always; }}
}}
</style>
<div class="print-area">
"""

    # 迴圈批次產生每一位得獎者的獎狀
    for idx, w in enumerate(winners):
        # 單張獎狀 HTML (無縮排防跑版)
        cert_html = f"""<div style="{bg_style} width: 100%; min-height: 550px; border-radius: 15px; padding: 40px; text-align: center; box-shadow: 0px 10px 30px rgba(0,0,0,0.1); font-family: 'Times New Roman', serif; margin-bottom: 30px; page-break-inside: avoid;">
<h1 style="color: {main_color}; margin: 0; font-size: 40px;">CERTIFICATE OF AWARD</h1>
<p style="letter-spacing: 2px; color: #666;">2026 I-NMC INTERNATIONAL COMPETITION</p>
<p style="margin-top: 20px; font-style: italic; color: #888;">This is to certify that the award for</p>
<h2 style="color: #222; text-transform: uppercase;">{rank}</h2>
<p style="color: #888; font-style: italic;">is proudly presented to</p>
<div style="margin: 40px 0;">
<div style="font-size: 50px; font-weight: 900; color: #111;">{w['ch']}</div>
<div style="font-size: 28px; font-style: italic; color: #444;">{w['en']}</div>
</div>
<div style="margin-top: 30px; border-top: 1px solid #ddd; padding-top: 10px; font-size: 14px; color: #999;">
Organized by I-NMC Committee & UTAR Malaysia
</div>
</div>
"""
        html_content += cert_html
        
        # 如果不是最後一張，插入 CSS 分頁符號
        if idx < len(winners) - 1:
            html_content += '<div class="page-break"></div>\n'

    # 封閉 print-area div
    html_content += "</div>"

    # 最終渲染
    st.write("---")
    st.markdown(html_content, unsafe_allow_html=True)
