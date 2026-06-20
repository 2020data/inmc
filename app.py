import streamlit as st
import pandas as pd
import base64
from PIL import Image
import io
import math

# ==========================================
# 1. 網頁基本設定與標題
# ==========================================
st.set_page_config(page_title="2026 I-NMC Live Award System", page_icon="🏆", layout="wide")
st.title("🏆 2026 I-NMC 動態頒獎系統")

# Google Sheets 匯出連結
sheet_url = "https://docs.google.com/spreadsheets/d/1v9HWOKlq0Mb7xKwyVT64hO64eoGUeHaN2kbflbVKlGw/export?format=xlsx"

# 建立工作表名稱、顯示標題、以及獎狀用分類名稱的對應表
sheet_mapping = {
    "2026_UTAR_X": {"display": "Category X - UTAR", "cat_name": "Mathketeers - Group of 3"},
    "2026_THU_X": {"display": "Category X - THU", "cat_name": "Mathketeers - Group of 3"},
    "2026_UTAR_Y": {"display": "Category Y - UTAR", "cat_name": "Theory of Everything"},
    "2026_THU_Y": {"display": "Category Y - THU", "cat_name": "Theory of Everything"},
    "2026_UTAR_Z": {"display": "Category Z - UTAR", "cat_name": "Running Math - Timed Event"},
    "2026_THU_Z": {"display": "Category Z - THU", "cat_name": "Running Math - Timed Event"},
    "2026_UTARIronMath": {"display": "IronMath - UTAR", "cat_name": "IronMath Individual"},
    "2026_THUIronMath": {"display": "IronMath - THU", "cat_name": "IronMath Individual"}
}

RANK_LABELS = ["WINNER 🥇", "1st RUNNER-UP 🥈", "2nd RUNNER-UP 🥉"]
Q1_LABEL = "Top 25% (Q1) 🎖️"
UTTU_TROPHY_TITLE = "🏆 UTTU Trophy (IronMath 總冠軍)"

# ==========================================
# 2. 資料處理與快取函式
# ==========================================
@st.cache_data(ttl=60)
def load_data():
    return pd.read_excel(sheet_url, sheet_name=None)

@st.cache_data
def get_optimized_image_base64(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    img.thumbnail((1500, 2000), Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"

def find_name_columns(df):
    cols = list(df.columns.astype(str))
    ch_col = next((c for c in cols if '姓名' in c), None)
    if not ch_col: ch_col = next((c for c in cols if 'name' in c.lower() and 'english' not in c.lower() and '英文' not in c), cols[0])
    en_col = next((c for c in cols if 'english' in c.lower() or '英文' in c), ch_col)
    return ch_col, en_col

def clean_name(val):
    if pd.isna(val): return ""
    val_str = str(val).strip()
    return "" if val_str.lower() in ["nan", "none", "null", "nat"] else val_str

# ==========================================
# 3. 側邊欄設定 (顯示開關、背景、列印)
# ==========================================
st.sidebar.header("⚙️ 顯示設定")
show_leaderboard = st.sidebar.checkbox("📊 顯示各組別排行榜", value=False)

st.sidebar.markdown("---")
st.sidebar.header("🎨 獎狀外觀與列印")
bg_option = st.sidebar.radio("獎狀背景選擇：", ["官方預設樣式", "使用上傳背景圖"])
uploaded_bg = st.sidebar.file_uploader("上傳背景圖 (建議 A4 比例)", type=["jpg", "png", "jpeg"])

if st.sidebar.button("🖨️ 批次下載 / 存為 PDF"):
    st.sidebar.info("💡 請在彈出的系統列印視窗中，將目標列印機選擇為「另存為 PDF」。")
    st.components.v1.html("<script>window.parent.print();</script>", height=0)

# ==========================================
# 4. 背景資料處理 (成績結算與排名邏輯)
# ==========================================
AWARDS_DATA = {}

# UTTU Trophy 對決用變數
utar_ironmath_score = -1
thu_ironmath_score = -1
utar_ironmath_data = None
thu_ironmath_data = None

try:
    with st.spinner("正在從 Google Drive 同步最新成績資料..."):
        all_sheets = load_data()
        
    if show_leaderboard:
        st.header("🏅 第一階段：各組別成績排行榜")
        col1, col2 = st.columns(2)
    
    for i, (sheet_name, info) in enumerate(sheet_mapping.items()):
        display_title = info["display"]
        cat_name = info["cat_name"]
        AWARDS_DATA[display_title] = {}
        
        if sheet_name in all_sheets:
            df = all_sheets[sheet_name]
            
            if "Grade/10" in df.columns:
                is_ironmath = "IronMath" in sheet_name
                is_category_x = "Category X" in display_title
                # 尋找是否有名稱為組別或 group 的欄位
                group_col = next((c for c in df.columns.astype(str) if '組別' in c or 'group' in c.lower()), None)

                ch_col, en_col = find_name_columns(df)

                if is_category_x and group_col:
                    # ==========================================
                    # [專屬邏輯] Category X - 團隊計分模式
                    # ==========================================
                    # 依組別分組，這裡使用 sum() 代表隊員總分。
                    # (註：如果 Excel 裡該組所有人都直接填寫同一個團隊總分，請將 sum() 改為 max() 避免重複計算)
                    group_scores = df.groupby(group_col)['Grade/10'].sum().reset_index()
                    group_scores_sorted = group_scores.sort_values(by="Grade/10", ascending=False).reset_index(drop=True)
                    
                    top_n = 3
                    q1_count = max(1, math.ceil(len(group_scores_sorted) * 0.25))
                    
                    top_groups = group_scores_sorted.head(top_n)
                    q1_groups = group_scores_sorted.head(q1_count)
                    
                    if show_leaderboard:
                        with col1 if i % 2 == 0 else col2:
                            st.subheader(display_title + " (團隊排名)")
                            st.markdown(f"**🏅 Top {top_n} & Top 25% (共 {q1_count} 組)**")
                            st.dataframe(q1_groups, use_container_width=True)
                            
                    # [A] 頒發主名次 (WINNER / 1st / 2nd)
                    for rank_idx in range(len(top_groups)):
                        grp_name = top_groups.iloc[rank_idx][group_col]
                        rank_label = RANK_LABELS[rank_idx]
                        
                        # 找出該隊伍所有成員
                        members = df[df[group_col] == grp_name]
                        ch_names = [clean_name(x) for x in members[ch_col] if clean_name(x)]
                        en_names = [clean_name(x) for x in members[en_col] if clean_name(x) and clean_name(x) not in ch_names]
                        
                        ch_joined = " & ".join(ch_names)
                        en_joined = " & ".join(en_names)
                        
                        # 將隊名與成員姓名組裝 (利用 HTML 控制字體大小，主顯隊名小字，隊員大字)
                        final_ch = f"<span style='font-size: 32px; color: #555;'>Team: {grp_name}</span><br><span style='font-size: 52px;'>{ch_joined}</span>"
                        
                        if rank_label not in AWARDS_DATA[display_title]:
                            AWARDS_DATA[display_title][rank_label] = []
                        AWARDS_DATA[display_title][rank_label].append({"ch": final_ch, "en": en_joined, "cat_name": cat_name})
                        
                    # [B] 頒發 Top 25% (Q1)
                    AWARDS_DATA[display_title][Q1_LABEL] = []
                    for rank_idx in range(len(q1_groups)):
                        grp_name = q1_groups.iloc[rank_idx][group_col]
                        
                        members = df[df[group_col] == grp_name]
                        ch_names = [clean_name(x) for x in members[ch_col] if clean_name(x)]
                        en_names = [clean_name(x) for x in members[en_col] if clean_name(x) and clean_name(x) not in ch_names]
                        
                        ch_joined = " & ".join(ch_names)
                        en_joined = " & ".join(en_names)
                        final_ch = f"<span style='font-size: 32px; color: #555;'>Team: {grp_name}</span><br><span style='font-size: 52px;'>{ch_joined}</span>"
                        
                        AWARDS_DATA[display_title][Q1_LABEL].append({"ch": final_ch, "en": en_joined, "cat_name": cat_name})

                else:
                    # ==========================================
                    # [原本邏輯] Y, Z, IronMath - 個人計分模式
                    # ==========================================
                    df_sorted = df.sort_values(by="Grade/10", ascending=False).reset_index(drop=True)
                    
                    top_n = 1 if is_ironmath else 3
                    q1_count = max(1, math.ceil(len(df_sorted) * 0.25))
                    
                    top_df = df_sorted.head(top_n)
                    q1_df = df_sorted.head(q1_count)
                    
                    if show_leaderboard:
                        with col1 if i % 2 == 0 else col2:
                            st.subheader(display_title)
                            st.markdown(f"**🏅 Top {top_n} & Top 25% (共 {q1_count} 名)**")
                            st.dataframe(q1_df, use_container_width=True)
                    
                    # [A] 頒發主名次 (WINNER / 1st / 2nd)
                    for rank_idx in range(len(top_df)):
                        row = top_df.iloc[rank_idx]
                        rank_label = RANK_LABELS[rank_idx]
                        
                        ch_name, en_name = clean_name(row[ch_col]), clean_name(row[en_col])
                        if ch_name == en_name: en_name = ""
                            
                        if rank_label not in AWARDS_DATA[display_title]:
                            AWARDS_DATA[display_title][rank_label] = []
                        AWARDS_DATA[display_title][rank_label].append({"ch": ch_name, "en": en_name, "cat_name": cat_name})

                    # [B] 頒發 Top 25% (Q1) - IronMath 組別不再發放 Q1
                    if not is_ironmath:
                        AWARDS_DATA[display_title][Q1_LABEL] = []
                        for rank_idx in range(len(q1_df)):
                            row = q1_df.iloc[rank_idx]
                            ch_name, en_name = clean_name(row[ch_col]), clean_name(row[en_col])
                            if ch_name == en_name: en_name = ""
                            AWARDS_DATA[display_title][Q1_LABEL].append({"ch": ch_name, "en": en_name, "cat_name": cat_name})

                    # [C] 紀錄 UTTU Trophy 對決資訊
                    if is_ironmath and not top_df.empty:
                        best_score = top_df.iloc[0]["Grade/10"]
                        best_ch = clean_name(top_df.iloc[0][ch_col])
                        best_en = clean_name(top_df.iloc[0][en_col])
                        if best_ch == best_en: best_en = ""
                        
                        if "UTAR" in sheet_name:
                            utar_ironmath_score = best_score
                            utar_ironmath_data = {"ch": best_ch, "en": best_en, "cat_name": "IronMath Overall Champion"}
                        elif "THU" in sheet_name:
                            thu_ironmath_score = best_score
                            thu_ironmath_data = {"ch": best_ch, "en": best_en, "cat_name": "IronMath Overall Champion"}
            else:
                if show_leaderboard: st.warning(f"⚠️ 在 {sheet_name} 中找不到 'Grade/10' 欄位。")
        else:
            if show_leaderboard: st.error(f"❌ 找不到工作表：{sheet_name}")

    # ==========================================
    # 結算 UTTU Trophy，加入頒獎選單
    # ==========================================
    if utar_ironmath_score > -1 and thu_ironmath_score > -1:
        if utar_ironmath_score > thu_ironmath_score:
            uttu_winner = utar_ironmath_data
        elif thu_ironmath_score > utar_ironmath_score:
            uttu_winner = thu_ironmath_data
        else:
            # 雙方平手
            uttu_winner = {"ch": f"{utar_ironmath_data['ch']} & {thu_ironmath_data['ch']}", 
                           "en": "UTAR & THU Co-Champions", 
                           "cat_name": "IronMath Overall Champions"}
            
        AWARDS_DATA[UTTU_TROPHY_TITLE] = {
            "WINNER 🏆": [uttu_winner]
        }

        # 顯示於排行榜底部
        if show_leaderboard:
            st.markdown("---")
            st.header("🏆 UTTU Trophy (IronMath 巔峰對決)")
            if utar_ironmath_score > thu_ironmath_score:
                st.success(f"### 🎉 得主：**{utar_ironmath_data['ch']}** (UTAR) - {utar_ironmath_score} 分")
                st.info(f"⚔️ 成功擊敗 THU 的 {thu_ironmath_data['ch']} ({thu_ironmath_score} 分)！")
            elif thu_ironmath_score > utar_ironmath_score:
                st.success(f"### 🎉 得主：**{thu_ironmath_data['ch']}** (THU) - {thu_ironmath_score} 分")
                st.info(f"⚔️ 成功擊敗 UTAR 的 {utar_ironmath_data['ch']} ({utar_ironmath_score} 分)！")
            else:
                st.warning(f"### 🤝 平手！**{utar_ironmath_data['ch']}** (UTAR) & **{thu_ironmath_data['ch']}** (THU)")
                st.info(f"⚔️ 雙方同為 {utar_ironmath_score} 分，共享 UTTU Trophy 榮耀！")
            st.markdown("---")

except Exception as e:
    st.error("❌ 讀取資料失敗，請確認連結或檔案權限。")
    st.exception(e)


# ==========================================
# 5. Live Award 頒獎系統介面 (主畫面重心)
# ==========================================
st.header("🎉 現場頒獎揭曉")

if AWARDS_DATA:
    # 建立選單 (包含 UTTU Trophy)
    category_options = [info["display"] for info in sheet_mapping.values() if info["display"] in AWARDS_DATA]
    if UTTU_TROPHY_TITLE in AWARDS_DATA:
        category_options.append(UTTU_TROPHY_TITLE)

    selected_category = st.selectbox("🎯 1. 選擇賽事類別：", category_options)
    current_winners = AWARDS_DATA[selected_category]
    
    st.subheader("🥁 2. 揭曉名次 (點擊按鈕產生 A4 獎狀)")
    ranks = list(current_winners.keys())
    
    if ranks:
        cols = st.columns(len(ranks))
        if "selected_rank" not in st.session_state: 
            st.session_state.selected_rank = None
            st.session_state.selected_cat = None
            
        if st.session_state.selected_cat != selected_category:
            st.session_state.selected_rank = None
            st.session_state.selected_cat = selected_category

        for i, rank in enumerate(ranks):
            if cols[i].button(rank, use_container_width=True):
                st.session_state.selected_rank = rank
                if "WINNER" in rank:
                    st.balloons()
                else:
                    st.snow()

        if st.session_state.selected_rank and st.session_state.selected_rank in current_winners:
            rank = st.session_state.selected_rank
            winners = current_winners[rank]
            
            # 設定顏色配置：WINNER 🏆 (包含 UTTU) 都是金色
            main_color = "#D4AF37" if "WINNER" in rank else "#B4B4B4" if "1st" in rank else "#CD7F32" if "2nd" in rank else "#8E44AD"
            
            custom_css = ""
            if bg_option == "使用上傳背景圖" and uploaded_bg:
                img_b64 = get_optimized_image_base64(uploaded_bg.getvalue())
                custom_css = f".cert-container {{ background-image: url('{img_b64}'); background-size: 100% 100%; background-repeat: no-repeat; background-position: center; border: none; }}"
            else:
                custom_css = f".cert-container {{ background: #fdfbf7; border: none; }}"

            # A4 滿版列印 CSS
            html_content = f"""<style>
            @page {{ size: A4 portrait; margin: 12mm !important; }}
            @media print {{
                [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"], .stButton, footer, hr {{ display: none !important; }}
                .print-area {{ display: block !important; width: 100% !important; margin: 0 !important; padding: 0 !important; }}
                .cert-container {{ width: 100% !important; max-width: none !important; height: 270mm !important; margin: 0 auto !important; box-shadow: none !important; page-break-inside: avoid !important; }}
                .page-break {{ page-break-after: always !important; break-after: page !important; }}
            }}
            {custom_css}
            </style>
            <div class="print-area">
            """

            for idx, w in enumerate(winners):
                cat_name_value = w.get("cat_name", "").strip()
                
                # HTML 結構加入「霸氣排版」 (加大字體、字重加深、增加陰影效果)
                cert_html = f"""
                <div class="cert-container" style="width: 100%; max-width: 794px; aspect-ratio: 210 / 297; padding: 40px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; margin: 0 auto 30px auto; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    <div style="background-color: rgba(255, 255, 255, 0.93); width: 100%; height: 100%; padding: 10% 8%; border-radius: 12px; border: 4px double {main_color}; text-align: center; box-shadow: 0px 8px 30px rgba(0,0,0,0.15); box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; align-items: center;">
                        
                        <div style="width: 100%;">
                            <h1 style="color: {main_color}; margin: 0; font-size: 46px; font-family: 'Times New Roman', serif; font-weight: 900; letter-spacing: 2px; text-transform: uppercase;">Congratulations</h1>
                            <p style="letter-spacing: 3px; color: #555; font-size: 15px; margin: 10px 0 25px 0; font-weight: bold;">2026 International-National Mathematics Competition</p>
                            
                            <div style="background-color: {main_color}; color: #ffffff; display: inline-block; padding: 8px 28px; border-radius: 40px; font-size: 18px; font-weight: 900; letter-spacing: 1px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                                {selected_category}
                            </div>
                            <div style="height: 12px;"></div>
                            <div style="background-color: #f5f5f7; color: {main_color}; display: inline-block; padding: 6px 24px; border-radius: 30px; font-size: 15px; font-weight: 900; letter-spacing: 0.5px; box-shadow: inset 0 0 0 1px rgba(0,0,0,0.05);">
                                {cat_name_value}
                            </div>
                        </div>

                        <div style="width: 100%;">
                            <p style="margin-top: 15px; font-style: italic; color: #666; font-size: 20px; margin-bottom: 5px;">This is to certify that the award for</p>
                            <h2 style="color: #111; text-transform: uppercase; font-size: 42px; margin: 10px 0; font-weight: 900; letter-spacing: 2px; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">{rank}</h2>
                            <p style="color: #666; font-style: italic; font-size: 20px; margin-bottom: 0;">is proudly presented to</p>
                            
                            <div style="margin: 40px 0;">
                                <div style="font-size: 72px; font-weight: 900; color: #000; font-family: 'Microsoft JhengHei', sans-serif; min-height: 90px; line-height: 1.1; letter-spacing: 4px; text-shadow: 2px 2px 4px rgba(0,0,0,0.15); margin-bottom: 10px;">{w['ch']}</div>
                                <div style="font-size: 34px; font-style: italic; font-weight: bold; color: #444; font-family: 'Times New Roman', serif; min-height: 45px; line-height: 1.1; letter-spacing: 1px;">{w['en']}</div>
                            </div>
                        </div>

                        <div style="width: 100%;">
                            <div style="border-top: 2px solid #ddd; padding-top: 20px; font-size: 16px; color: #777; font-weight: bold; letter-spacing: 1px;">
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
            st.html(html_content)
    else:
        st.info("此組別目前尚無排名資料。")
else:
    st.warning("目前沒有可用的頒獎資料。")
