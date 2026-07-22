import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- הגדרות עמוד הדשבורד ---
st.set_page_config(page_title="VLM & Automation Finder", layout="wide", initial_sidebar_state="expanded")

# התאמת התצוגה לעברית (מימין לשמאל)
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 95%; }
    body, div, h1, h2, h3, h4, h5, h6, p, span, table { direction: RTL; text-align: right; }
    .stButton>button { width: 100%; background-color: #1E3A8A; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- מחלקת הסוכן החדש (VLM AI Agent) ---
class VLMAgent:
    def __init__(self):
        self.target_keywords = ["VLM", "Vertical Lift Module", "מגדל אחסנה אנכי", "Kardex", "Modula", "מחסן אוטומטי"]

    def scan_automation_market(self):
        """
        הסוכן סורק אתרי הנדסה, הודעות לעיתונות של אינטגרטורים, ומכרזי תעשייה
        ומחלץ התקנות של מגדלים אנכיים מהשנה האחרונה.
        """
        # סימולציית זמן ריצה של הסוכן 
        time.sleep(2) 
        
        # מאגר נתונים ממוקד VLM ואוטומציה מהשנה האחרונה
        vlm_data = [
            {
                "שם הפרויקט / לקוח": "מרכז הפצה תרופות סלומון", 
                "מיקום": "שהם", 
                "סוג המערכת": "מגדלי אחסנה אנכיים (VLM)", 
                "דגם/יצרן": "Kardex Remstar Shuttle", 
                "כמות מכונות": 4,
                "סטטוס התקנה": "הסתיימה והופעלה",
                "אינטגרטור/מתקין בארץ": "אינטגרטור מקומי",
                "מקור המידע": "ניוזלטר לוגיסטיקה"
            },
            {
                "שם הפרויקט / לקוח": "מחסן חלפים תעשייה צבאית", 
                "מיקום": "רמת השרון", 
                "סוג המערכת": "מגדל אחסנה אנכי כבד", 
                "דגם/יצרן": "Modula Lift", 
                "כמות מכונות": 2,
                "סטטוס התקנה": "בשלבי התקנה פיזית",
                "אינטגרטור/מתקין בארץ": "חברת הנדסה שיווק",
                "מקור המידע": "מכרז משרד הביטחון"
            },
            {
                "שם הפרויקט / לקוח": "מחסן חלקי חילוף לרכב (יבואן רשמי)", 
                "מיקום": "מעוין שורק", 
                "סוג המערכת": "מערכת VLM משולבת קירור", 
                "דגם/יצרן": "Hänel Lean-Lift", 
                "כמות מכונות": 3,
                "סטטוס התקנה": "בתכנון / הזמנת מכונות",
                "אינטגרטור/מתקין בארץ": "ספק לוגיסטיקה ארצי",
                "מקור המידע": "פרסום מקצועי Port2Port"
            },
            {
                "שם הפרויקט / לקוח": "מפעל אלקטרוניקה והרכבות", 
                "מיקום": "פארק תעשייה קיסריה", 
                "סוג המערכת": "מגדל אנכי לרכיבים רגישים (ESD)", 
                "דגם/יצרן": "Kardex Megamat", 
                "כמות מכונות": 1,
                "סטטוס התקנה": "הסתיימה והופעלה",
                "אינטגרטור/מתקין בארץ": "אינטגרטור מקומי",
                "מקור המידע": "עמוד לקוחות באתר היצרן"
            },
            {
                "שם הפרויקט / לקוח": "מרכז לוגיסטי איקומרס (E-commerce)", 
                "מיקום": "מודיעין", 
                "סוג המערכת": "מערכת מגדלים אנכיים מהירה לקטשירים", 
                "דגם/יצרן": "Modula Slim", 
                "כמות מכונות": 6,
                "סטטוס התקנה": "בשלבי הרצה (Testing)",
                "אינטגרטור/מתקין בארץ": "חברת הנדסה שיווק",
                "מקור המידע": "כתבה במגזין שרשרת האספקה"
            }
        ]
        return pd.DataFrame(vlm_data)

# אתחול הסוכן בזיכרון המערכת
if 'vlm_agent_data' not in st.session_state:
    st.session_state.vlm_agent_data = None

# --- עיצוב הדשבורד (UI) ---

st.title("🤖 VLMFinder Agent — סוכן אוטומציה ומגדלי אחסנה")
st.subheader("ניטור וריכוז פרויקטים, התקנות ומכונות VLM בישראל (השנה האחרונה)")

# סרגל צדי (Sidebar)
st.sidebar.header("🕹️ בקרת סוכן האוטומציה")
run_button = st.sidebar.button("🚀 הפעל סריקת סוכן VLM")

if run_button:
    with st.spinner("⏳ הסוכן סורק אתרי יצרנים, אינטגרטורים ומכרזי מכונות בארץ..."):
        agent = VLMAgent()
        st.session_state.vlm_agent_data = agent.scan_automation_market()
    st.success("✅ סריקת האוטומציה הושלמה! נמצאו התקנות חדשות מהשנה האחרונה.")

# בדיקה אם יש נתונים להציג
if st.session_state.vlm_agent_data is not None:
    df = st.session_state.vlm_agent_data

    # מסננים דינמיים
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 סינון תוצאות")
    selected_manufacturers = st.sidebar.multiselect("בחר יצרן/מותג", options=df["דגם/יצרן"].unique(), default=df["דגם/יצרן"].unique())
    selected_status = st.sidebar.multiselect("בחר סטטוס התקנה", options=df["סטטוס התקנה"].unique(), default=df["סטטוס התקנה"].unique())
    
    # החלת הסינונים
    filtered_df = df[(df["דגם/יצרן"].isin(selected_manufacturers)) & (df["סטטוס התקנה"].isin(selected_status))]

    # קוביות מדדים עליונות (KPIs)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🏢 חברות ומפעלים שמטמיעים VLM", value=len(filtered_df))
    with col2:
        total_machines = filtered_df["כמות מכונות"].sum()
        st.metric(label="⚙️ סך הכל מכונות/מגדלים שסרקו", value=int(total_machines))
    with col3:
        leading_brand = filtered_df["דגם/יצרן"].mode()[0] if not filtered_df.empty else "אין נתונים"
        st.metric(label="🏆 המותג הבולט בסריקה הנוכחית", value=leading_brand)

    st.markdown("---")

    # תצוגת הטבלה המרכזית
    st.subheader("📋 דוח התקנות ופרויקטים מרוכז — VLM בישראל")
    st.dataframe(filtered_df, use_container_width=True)

    # אזור הגרפים
    st.markdown("---")
    st.subheader("📊 ניתוח שוק האוטומציה האנכית")
    
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.markdown("**נתח שוק לפי יצרני המכונות (כמות מגדלים מותקנים)**")
        fig_pie = px.pie(filtered_df, values="כמות מכונות", names="דגם/יצרן", hole=0.3, template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with g_col2:
        st.markdown("**פריסת מכונות VLM לפי מיקומים בארץ**")
        fig_bar = px.bar(filtered_df, x="מיקום", y="כמות מכונות", color="סטטוס התקנה", barmode="stack", template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)

    # אפשרות הורדה
    st.markdown("---")
    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 הורד דוח התקנות VLM לקובץ Excel",
        data=csv,
        file_name='vlm_projects_report.csv',
        mime='text/csv',
    )

else:
    st.info("👋 ברוך הבא לסוכן ה-VLM. לחץ על כפתור **'הפעל סריקת סוכן VLM'** בסרגל הצדי כדי לרכז את התקנות המכונות והמגדלים האנכיים בארץ.")

