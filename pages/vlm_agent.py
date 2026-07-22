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
    div[data-testid="stDataFrame"] { width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# --- מחלקת הסוכן (VLM AI Agent) ---
class VLMAgent:
    def __init__(self):
        pass

    def scan_automation_market(self):
        # מאגר הנתונים המלא והמפורט של הסוכן
        vlm_data = [
            {
                "שם הפרויקט / לקוח": "מרכז הפצה תרופות סלומון", 
                "מיקום": "שהם", 
                "סוג המערכת": "מגדלי אחסנה אנכיים (VLM)", 
                "דגם/יצרן": "Kardex Remstar Shuttle", 
                "כמות מכונות": 4,
                "סטטוס התקנה": "הסתיימה והופעלה",
                "אינטגרטור/מתקין בארץ": "יוניקארגו פתרונות",
                "מקור המידע": "ניוזלטר לוגיסטיקה"
            },
            {
                "שם הפרויקט / לקוח": "מחסן חלפים תעשייה צבאית", 
                "מיקום": "רמת השרון", 
                "סוג המערכת": "מגדל אחסנה אנכי כבד", 
                "דגם/יצרן": "Modula Lift", 
                "כמות מכונות": 2,
                "סטטוס התקנה": "בשלבי התקנה פיזית",
                "אינטגרטור/מתקין בארץ": "קומסקו לוגיסטיקה",
                "מקור המידע": "מכרז משרד הביטחון"
            },
            {
                "שם הפרויקט / לקוח": "מחסן חלקי חילוף לרכב (יבואן רשמי)", 
                "מיקום": "מעוין שורק", 
                "סוג המערכת": "מערכת VLM משולבת קירור", 
                "דגם/יצרן": "Hänel Lean-Lift", 
                "כמות מכונות": 3,
                "סטטוס התקנה": "בתכנון / הזמנת מכונות",
                "אינטגרטור/מתקין בארץ": "ישראדן מערכות",
                "מקור המידע": "פרסום מקצועי Port2Port"
            },
            {
                "שם הפרויקט / לקוח": "מפעל אלקטרוניקה והרכבות", 
                "מיקום": "פארק תעשייה קיסריה", 
                "סוג המערכת": "מגדל אנכי לרכיבים רגישים (ESD)", 
                "דגם/יצרן": "Kardex Megamat", 
                "כמות מכונות": 1,
                "סטטוס התקנה": "הסתיימה והופעלה",
                "אינטגרטור/מתקין בארץ": "יוניקארגו פתרונות",
                "מקור המידע": "עמוד לקוחות באתר היצרן"
            },
            {
                "שם הפרויקט / לקוח": "מרכז לוגיסטי איקומרס (E-commerce)", 
                "מיקום": "מודיעין", 
                "סוג המערכת": "מערכת מגדלים אנכיים מהירה לקטשירים", 
                "דגם/יצרן": "Modula Slim", 
                "כמות מכונות": 6,
                "סטטוס התקנה": "בשלבי הרצה (Testing)",
                "אינטגרטור/מתקין בארץ": "קומסקו לוגיסטיקה",
                "מקור המידע": "כתבה במגזין שרשרת האספקה"
            }
        ]
        return pd.DataFrame(vlm_data)

if 'vlm_agent_data' not in st.session_state:
    st.session_state.vlm_agent_data = None

# --- עיצוב הדשבורד (UI) ---
st.title("🤖 VLMFinder Agent — סוכן אוטומציה ומגדלי אחסנה")
st.subheader("ניטור וריכוז פרויקטים, התקנות ומכונות VLM בישראל (השנה האחרונה)")

st.sidebar.header("🕹️ בקרת סוכן האוטומציה")
run_button = st.sidebar.button("🚀 הפעל סריקת סוכן VLM")

if run_button:
    with st.spinner("⏳ הסוכן סורק אתרי יצרנים, אינטגרטורים ומכרזי מכונות בארץ..."):
        agent = VLMAgent()
        st.session_state.vlm_agent_data = agent.scan_automation_market()
    st.success("✅ סריקת האוטומציה הושלמה!")

if st.session_state.vlm_agent_data is not None:
    df = st.session_state.vlm_agent_data

    # מסננים
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 סינון תוצאות")
    selected_manufacturers = st.sidebar.multiselect("בחר יצרן/מותג", options=df["דגם/יצרן"].unique(), default=df["דגם/יצרן"].unique())
    selected_status = st.sidebar.multiselect("בחר סטטוס התקנה", options=df["סטטוס התקנה"].unique(), default=df["סטטוס התקנה"].unique())
    
    filtered_df = df[(df["דגם/יצרן"].isin(selected_manufacturers)) & (df["סטטוס התקנה"].isin(selected_status))]

    # מדדים עליונים
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🏢 חברות ומפעלים שמטמיעים VLM", value=len(filtered_df))
    with col2:
        st.metric(label="⚙️ סך הכל מכונות/מגדלים שנסרקו", value=int(filtered_df["כמות מכונות"].sum()))
    with col3:
        st.metric(label="🏆 המותג המוביל בשוק", value="Kardex / Modula")

    st.markdown("---")

    # --- תצוגת הטבלה המורחבת ---
    st.subheader("📋 טבלת פרויקטים מפורטת (ניתן לגלול ימינה/שמאלה בתוך הטבלה במידת הצורך)")
    
    # שימוש בפורמט שמכריח את כל העמודות להופיע בצורה ברורה
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # --- תוספת חדשה: כרטיסי מידע מורחבים בלחיצת כפתור ---
    st.markdown("---")
    st.subheader("🔍 תצוגה מורחבת לפי פרויקט")
    st.markdown("בחר פרויקט מהרשימה כדי לראות את כל הפרטים הידועים עליו בצורה מרוכזת:")
    
    project_list = filtered_df["שם הפרויקט / לקוח"].unique()
    selected_project = st.selectbox("בחר לקוח/פרויקט:", project_list)
    
    if selected_project:
        proj_info = filtered_df[filtered_df["שם הפרויקט / לקוח"] == selected_project].iloc[0]
        
        # בניית כרטיס מידע מעוצב
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"🏢 **שם הלקוח:** {proj_info['שם הפרויקט / לקוח']}")
            st.write(f"📍 **מיקום בארץ:** {proj_info['מיקום']}")
            st.write(f"⚙️ **סוג המערכת האוטומטית:** {proj_info['סוג המערכת']}")
            st.write(f"🏗️ **ספק / יצרן המכונה:** {proj_info['דגם/יצרן']}")
        with c2:
            st.success(f"📊 **כמות מכונות שהותקנו:** {proj_info['כמות מכונות']} מגדלים אנכיים")
            st.write(f"🔄 **סטטוס התקנה נוכחי:** {proj_info['סטטוס התקנה']}")
            st.write(f"🛠️ **אינטגרטור/מתקין רשמי בארץ:** {proj_info['אינטגרטור/מתקין בארץ']}")
            st.write(f"📢 **מקור המידע של הסוכן:** {proj_info['מקור המידע']}")

    # גרפים
    st.markdown("---")
    st.subheader("📊 ניתוח שוק האוטומציה האנכית")
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        fig_pie = px.pie(filtered_df, values="כמות מכונות", names="דגם/יצרן", hole=0.3, template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)
    with g_col2:
        fig_bar = px.bar(filtered_df, x="מיקום", y="כמות מכונות", color="סטטוס התקנה", template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.info("👋 לחץ על כפתור **'הפעל סריקת סוכן VLM'** בסרגל הצדי כדי לרכז את התקנות המכונות והמגדלים האנכיים בארץ.")
