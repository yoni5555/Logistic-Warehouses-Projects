import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- הגדרות עמוד הדשבורד ---
st.set_page_config(page_title="LogiFinder Dashboard", layout="wide", initial_sidebar_state="expanded")

# התאמת התצוגה לעברית (מימין לשמאל)
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 95%; }
    body, div, h1, h2, h3, h4, h5, h6, p, span, table { direction: RTL; text-align: right; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- מחלקת הסוכן (The AI Agent) ---
class LogisticsAgent:
    def __init__(self):
        pass

    def run_agent_scan(self):
        """
        פונקציה המדמה את פעולת הסוכן: סריקת אתרי רמ"י, מאיה, ועיתונות כלכלית, 
        וסינון המידע באמצעות LLM רק לפרויקטים לוגיסטיים מהשנה האחרונה.
        """
        # סימולציית זמן ריצה של הסוכן (סריקה ועיבוד)
        time.sleep(2) 
        
        # מאגר הנתונים המעובד שהסוכן מפיק (נתוני אמת ומגמות מהשנה האחרונה)
        raw_data = [
            {"שם הפרויקט/היזם": "מסוף לוגיסטי גולד בונד", "אזור": "צפון", "מיקום מדויק": "בית שאן", "שטח (מ\"ר)": 45000, "סטטוס": "הושק ואוכלס", "גובה תקרה (מ')": 14, "מקור המידע": "Port2Port"},
            {"שם הפרויקט/היזם": "Metro Park 456", "אזור": "מרכז", "מיקום מדויק": "פתח תקווה", "שטח (מ\"ר)": 18000, "סטטוס": "בביצוע ושיווק", "גובה תקרה (מ')": 11, "מקור המידע": "עיתונות כלכלית"},
            {"שם הפרויקט/היזם": "מכרז אחסנה פתוחה חנ\"י", "אזור": "דרום", "מיקום מדויק": "עורף נמל אשדוד", "שטח (מ\"ר)": 120000, "סטטוס": "מכרז פעיל", "גובה תקרה (מ')": 0, "מקור המידע": "מכרזי חנ\"י"},
            {"שם הפרויקט/היזם": "מרלו\"ג מגה אור ושופרסל", "אזור": "מרכז", "מיקום מדויק": "חבל מודיעין", "שטח (מ\"ר)": 35000, "סטטוס": "בהקמה/הרחבה", "גובה תקרה (מ')": 15, "מקור המידע": "דיווח בורסאי (מאיה)"},
            {"שם הפרויקט/היזם": "פארק לוגיסטי אמות", "אזור": "דרום", "מיקום מדויק": "צומת כנות", "שטח (מ\"ר)": 50000, "סטטוס": "בביצוע", "גובה תקרה (מ')": 13, "מקור המידע": "דיווח בורסאי (מאיה)"},
            {"שם הפרויקט/היזם": "מחסני קירור מתקדמים גב-ים", "אזור": "צפון", "מיקום מדויק": "מפרץ חיפה", "שטח (מ\"ר)": 22000, "סטטוס": "בתכנון מתקדם", "גובה תקרה (מ')": 12, "מקור המידע": "מרכז הנדל\"ן"}
        ]
        return pd.DataFrame(raw_data)

# אתחול הסוכן בזיכרון המערכת
if 'agent_data' not in st.session_state:
    st.session_state.agent_data = None

# --- עיצוב הדשבורד (UI) ---

st.title("🎯 LogiFinder Agent — דשבורד פרויקטים לוגיסטיים")
st.subheader("ניהול, איתור וריכוז מחסנים ומרלו\"גים בישראל")

# סרגל צדי (Sidebar) להפעלת הסוכן וסינונים
st.sidebar.header("🕹️ בקרת סוכן")
run_button = st.sidebar.button("🚀 הפעל סריקת סוכן בזמן אמת")

if run_button:
    with st.spinner("⏳ הסוכן סורק כעת את מאיה (בורסה), רמ\"י ואתרי חדשות כלכליים..."):
        agent = LogisticsAgent()
        st.session_state.agent_data = agent.run_agent_scan()
    st.success("✅ הסריקה הושלמה בהצלחה! הנתונים מעודכנים לשנה האחרונה.")

# בדיקה אם יש נתונים להציג
if st.session_state.agent_data is not None:
    df = st.session_state.agent_data

    # מסננים בסרגל הצדי (דינמיים לפי המידע שנמצא)
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 סינון תוצאות")
    selected_regions = st.sidebar.multiselect("בחר אזור בארץ", options=df["אזור"].unique(), default=df["אזור"].unique())
    selected_status = st.sidebar.multiselect("בחר סטטוס פרויקט", options=df["סטטוס"].unique(), default=df["סטטוס"].unique())
    
    # החלת הסינונים
    filtered_df = df[(df["אזור"].isin(selected_regions)) & (df["סטטוס"].isin(selected_status))]

    # קוביות מדדים עליונות (KPIs)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🏗️ סך הכל פרויקטים שנמצאו", value=len(filtered_df))
    with col2:
        total_sqm = filtered_df["שטח (מ\"ר)"].sum()
        st.metric(label="📐 סך שטח בפיתוח/אחסנה (מ\"ר)", value=f"{total_sqm:,}")
    with col3:
        avg_height = filtered_df[filtered_df["גובה תקרה (מ')"] > 0]["גובה תקרה (מ')"].mean()
        st.metric(label="🧱 גובה תקרה ממוצע (מרלו\"גים מודרניים)", value=f"{avg_height:.1f} מטר")

    st.markdown("---")

    # תצוגת הטבלה המרכזית
    st.subheader("📋 רשימת הפרויקטים המרוכזת — השנה האחרונה")
    st.dataframe(filtered_df, use_container_width=True)

    # אזור הגרפים והניתוח הוויזואלי
    st.markdown("---")
    st.subheader("📊 ניתוח מגמות שוק")
    
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.markdown("**פיזור שטחי אחסנה (מ\"ר) לפי אזורים בארץ**")
        fig_pie = px.pie(filtered_df, values="שטח (מ\"ר)", names="אזור", hole=0.3, template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with g_col2:
        st.markdown("**נפח הפרויקטים (מ\"ר) לפי מיקום וסטטוס**")
        fig_bar = px.bar(filtered_df, x="מיקום מדויק", y="שטח (מ\"ר)", color="סטטוס", barmode="group", template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)

    # אפשרות הורדה לאקסל / CSV
    st.markdown("---")
    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 הורד את הדו\"ח הנוכחי לקובץ Excel / CSV",
        data=csv,
        file_name='logistics_projects_report.csv',
        mime='text/csv',
    )

else:
    # הודעת ברירת מחדל כאשר הדשבורד נפתח אך הסוכן עדיין לא הופעל
    st.info("👋 ברוך הבא לדשבורד הסוכן הלוגיסטי. לחץ על כפתור **'הפעל סריקת סוכן בזמן אמת'** בסרגל הצדי כדי לאסוף ולרכז את כל פרויקטי האחסנה מהשנה האחרונה.")
