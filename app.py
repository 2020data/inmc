import streamlit as st
import base64

# 設定網頁標題與圖示
st.set_page_config(page_title="2026 I-NMC Award System", page_icon="🏆", layout="centered")

# --- 2026 I-NMC 完整得獎資料庫 ---
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

# 剛幫你設計的張大千+趙無極+唐伯虎風格 A4 獎狀背景圖網址
DEFAULT_BG_URL = "https://images.squarespace-cdn.com/content/v1/621353e144a83556f8fbf538/b64cc7f2-6468-45fc-ae5b-0a7587efae27/00003-2470762957.png"

def get_image_base64(image_file):
    encoded_string = base64.b64encode(image_file.getvalue()).decode()
    return f"data:image/png;base64,{encoded_string}"

# --- 側邊欄設置 ---
st.sidebar.header("🎨 獎狀自定義設置")
bg_option = st.sidebar.radio("獎狀背景選擇：", ["使用官方潑彩水墨底圖", "上傳自訂背景圖"])
uploaded_bg = st.sidebar.file_uploader("上傳背景圖", type=["jpg", "png", "jpeg"])

if st.sidebar.button("🖨️ 準備列印 / 存為 PDF"):
    st.sidebar.info("請在彈出的列印視窗中選擇「另存為 PDF」。")
    st.components.v1.html("<script>window.print();</script>", height=0)

# --- 主畫面 ---
st.title("🏆 2026 I-NMC Award Ceremony")
selected_category = st.selectbox("1. 選擇賽事類別：", list(AWARDS_DATA.keys()))
current_winners = AWARDS_DATA[selected_category]

st.write("---")
st.subheader("2. 揭曉名次")
cols = st.columns(4)
ranks = list(current_winners.keys())

if "selected_rank" not in st.session_state: 
    st.session_state.selected_rank = None

for i, rank in enumerate(ranks):
    if cols[i].button(rank):
        st.session_state.selected_rank = rank
        if "Q1" not in rank:
            st.snow()
            st.balloons()

# --- 渲染獎狀 (修復 HTML 原始碼洩漏問題) ---
if st.session_state.selected_rank:
    rank = st.session_state.selected_rank
    winners = current_winners[rank]
    
    # 決定背景圖來源
    if bg_option == "上傳自訂背景圖" and uploaded_bg:
        bg_image_style = get_image_base64(uploaded_bg)
    else:
        bg_image_style = DEFAULT_BG_URL

    # 針對 Top Q1 多人與前三名單人動態生成緊湊的 HTML（移除換行與縮排，避免解析錯誤）
    if len(winners) > 1:
        name_html = "<div style='display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:20px 0;max-height:260px;overflow-y:auto;'>"
        for w in winners:
            name_html += f"<div style='font-size:18px;color:#222;line-height:1.2;'><b>{w['ch']}</b><br><span style='font-size:14px;color:#555;'>{w['en']}</span></div>"
        name_html += "</div>"
    else:
        w = winners[0]
        name_html = f"<div style='margin:45px 0;'><div style='font-size:52px;font-weight:900;color:#111;font-family:\"Microsoft JhengHei\",sans-serif;letter-spacing:3px;'>{w['ch']}</div><div style='font-size:26px;font-style:italic;color:#444;font-family:\"Georgia\",serif;margin-top:5px;'>{w['en']}</div></div>"

    main_color = "#D4AF37" if "WINNER" in rank else "#B4B4B4" if "1st" in rank else "#CD7F32" if "2nd" in rank else "#0056B3"

    # 核心修正：將所有 HTML 串接在同一行或確保沒有引發 Markdown 解析問題的縮排
    html_template = f"""<style>
@media print {{
    body * {{ visibility: hidden; }}
    .print-area, .print-area * {{ visibility: visible; }}
    .print-area {{ position: absolute; left: 0; top: 0; width: 100%; }}
}}
</style>
<div class="print-area" style="background-image: url('{bg_image_style}'); background-size: 100% 100%; background-repeat: no-repeat; background-position: center; width: 100%; aspect-ratio: 1 / 1.414; border-radius: 15px; padding: 12% 10% 8% 10%; text-align: center; box-shadow: 0px 10px 30px rgba(0,0,0,0.15); box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
<div style="width: 100%;">
<h1 style="color: {main_color}; margin: 0; font-size: 38px; font-family: 'Georgia', serif; letter-spacing: 2px; font-weight: bold;">CERTIFICATE OF AWARD</h1>
<p style="letter-spacing: 2px; color: #555; font-size: 13px; font-weight: 600; margin: 5px 0 0 0;">2026 I-NMC INTERNATIONAL COMPETITION</p>
</div>
<div style="width: 100%; margin: auto 0;">
<p style="font-style: italic; color: #666; font-size: 16px; margin: 0;">This is to certify that the award for</p>
<h2 style="color: #222; text-transform: uppercase; font-size: 28px; font-weight: 800; margin: 10px 0; letter-spacing: 1px;">✨ {rank} ✨</h2>
<p style="color: #666; font-style: italic; font-size: 16px; margin: 0;">is proudly presented to</p>
{name_html}
</div>
<div style="width: 100%;">
<div style="border-top: 1px solid rgba(0,0,0,0.1); padding-top: 15px; font-size: 13px; color: #666; font-weight: 500; letter-spacing: 0.5px;">Organized by I-NMC Committee & UTAR Malaysia</div>
</div>
</div>"""

    # 執行渲染
    st.write("---")
    st.markdown(html_template, unsafe_allow_html=True)
