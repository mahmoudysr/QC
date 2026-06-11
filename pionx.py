import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. إعداد الصفحة وتطبيق الهوية البصرية الفاخرة لمجموعة PCG / PIONX (أسود وذهبي ملكي)
st.set_page_config(
    page_title="منصة PIONX QC/QA - مجموعة PCG الاستشارية",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق الستاين والـ CSS الفاخر لمنع أي تداخل وبناء واجهة تليق بالشركات الكبرى
st.markdown("""
<style>
    html, body, [data-testid="stSidebar"] {
        background-color: #0d0d0d;
        color: #e5e5e5;
    }
    .stApp {
        background-color: #0d0d0d;
        color: #e5e5e5;
    }
    h1, h2, h3, h4 {
        color: #d4af37 !important;
        font-weight: bold;
    }
    .stButton>button {
        background: linear-gradient(135deg, #aa7c11 0%, #d4af37 100%) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 10px 24px !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    [data-testid="stSidebar"] {
        background-color: #141414 !important;
        border-left: 1px solid #aa7c11 !important;
    }
    .user-box {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 6px;
        border-right: 4px solid #d4af37;
        margin-bottom: 12px;
        text-align: right;
    }
    .ai-box {
        background-color: #111111;
        padding: 15px;
        border-radius: 6px;
        border-right: 4px solid #aa7c11;
        margin-bottom: 12px;
        text-align: right;
        border: 1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

# 2. إدارة وتخزين الحالة للمستخدمين والمشاريع برمجياً
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'projects_data' not in st.session_state:
    st.session_state.projects_data = {
        "مشروع أبراج أورا هيدس (جدة - Buildings B-C-E-V)": {
            "status": "مراجعة أنظمة MEP والإنشائي",
            "date": "2026-04-20",
            "notes": [
                {"كود الملاحظة": "PCG-QA-001", "القسم": "MEP / إنشائي", "تفاصيل التعارض الهندسي": "تعارض مسار دكت التكييف المخفي (Concealed HVAC) مع الجسر الإنشائي النازل في المحور الأفقي للمجلس الرئيسي.", "الخطورة": "حرجة جدًا", "الحالة": "معلقة"},
                {"كود الملاحظة": "PCG-QA-002", "القسم": "معماري", "تفاصيل التعارض الهندسي": "عدم مطابقة أبعاد وتوجيه فتحات الأبواب الداخلية لغرف النوم الرئيسية مع اشتراطات كود البناء المعتمد.", "الخطورة": "متوسطة", "الحالة": "تم التعديل والاعتماد"}
            ],
            "chat_history": [
                {"sender": "User", "text": "استخرج لي ملخص تعارضات التكييف في مشروع أورا هيدس؟"},
                {"sender": "AI", "text": "أهلاً بك في منصة مراجعة الجودة لمجموعة PCG. تم رصد تعارض حرج برقم PCG-QA-001: دكت التكييف المخفي (Concealed HVAC) يتقاطع مع الجسر الإنشائي النازل في المبنى B."}
            ]
        },
        "مشروع فيلا المشرقية (الرياض - G+2+ANNEX)": {
            "status": "مكتمل ومعتمد نهائياً",
            "date": "2026-05-15",
            "notes": [
                {"كود الملاحظة": "PCG-QA-003", "القسم": "إنشائي / تربة", "تفاصيل التعارض الهندسي": "تأكيد مطابقة تسليح القواعد المدمجة واللبشة مع توصيات هبوط التربة الواردة في تقرير فحص التربة المعتمد للفيلا.", "الخطورة": "حرجة جدًا", "الحالة": "تم الاعتماد نهائياً"}
            ],
            "chat_history": [
                {"sender": "User", "text": "هل تم مراجعة أساسات المشرقية؟"},
                {"sender": "AI", "text": "نعم يا فندم، تم فحص مطابقة تسليح القواعد مع تقرير التربة والتصميم آمن تماماً."}
            ]
        }
    }

# --- واجهة تسجيل الدخول وحفظ باقات الاشتراكات ---
if not st.session_state.logged_in:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='font-size: 28pt;'>👑 PCG | PIONX CONSULTING GROUP</h1>
        <h2 style='color: #aa7c11 !important; font-size: 16pt;'>المنصة الذكية المتكاملة لمراجعة الجودة الهندسية وكشف التعارضات (QC/QA)</h2>
        <hr style='border: 1px solid #aa7c11; width: 60%; margin: auto;'>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.subheader("🔐 تسجيل الدخول الآمن للمنصة")
        u_email = st.text_input("البريد الإلكتروني أو اسم المستخدم:")
        u_pass = st.text_input("كلمة المرور:", type="password")
        u_role = st.selectbox("تسجيل الدخول بصفتك الحالية:", ["مدير النظام (Admin)", "مهندس مراجع بالمجموعة (Reviewer)", "العميل المستفيد (Client)"])
        
        if st.button("✓ دخول المنصة"):
            if u_email and u_pass:
                st.session_state.logged_in = True
                st.session_state.user_role = u_role
                st.session_state.current_user = u_email
                st.rerun()
            else:
                st.error("الرجاء كتابة البيانات بشكل صحيح لتخطي جدار الحماية")

# --- واجهة النظام الداخلية بعد تسجيل الدخول ---
else:
    with st.sidebar:
        st.markdown("<div style='text-align:center;'><h2>PCG GROUP</h2><p style='color:#aa7c11;'>QUALITY ASSURANCE</p></div>", unsafe_allow_html=True)
        st.markdown(f"👤 المستخدم: **{st.session_state.current_user}**")
        st.markdown(f"💼 الصلاحية: **{st.session_state.user_role}**")
        p_options = list(st.session_state.projects_data.keys())
        current_sel_proj = st.selectbox("📁 اختر المشروع النشط للمراجعة والاستعلام:", p_options)
        if st.button("🚪 تسجيل خروج آمن"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown(f"<h1>🏢 لوحة تدقيق وضبط جودة المشروعات: {current_sel_proj}</h1>", unsafe_allow_html=True)
    tab_dashboard, tab_ai_chat, tab_exporter, tab_settings = st.tabs([
        "📋 سجل الأخطاء والتعارضات", 
        "💬 PIONX AI Chat (الشات الهندسي الذكي)", 
        "📄 مركز استخراج التقارير الفورية", 
        "⚙️ إدارة الاشتراكات والحسابات المالية"
    ])
    
    with tab_dashboard:
        current_p_data = st.session_state.projects_data[current_sel_proj]
        df_to_show = pd.DataFrame(current_p_data["notes"])
        if not df_to_show.empty:
            st.table(df_to_show)
            
        if st.session_state.user_role in ["مدير النظام (Admin)", "مهندس مراجع بالمجموعة (Reviewer)"]:
            st.subheader("➕ إضافة ملاحظة أو تعارض هندسي جديد")
            with st.form("new_discrepancy_form"):
                in_disc = st.selectbox("القسم الهندسي المتأثر:", ["معماري", "إنشائي", "MEP / أنظمة الميكانيك والكهرباء"])
                in_desc = st.text_area("وصف دقيق وتفصيلي للخطأ أو التعارض الهندسي المرصود:")
                in_sev = st.selectbox("درجة الخطورة:", ["منخفضة الخطورة", "متوسطة", "حرجة جدًا"])
                if st.form_submit_button("✓ حفظ الملحوظة وتحديث محرك الـ AI فوراً"):
                    new_code = f"PCG-QA-00{len(current_p_data['notes'])+1}"
                    st.session_state.projects_data[current_sel_proj]["notes"].append({
                        "كود الملاحظة": new_code, "القسم": in_disc, "تفاصيل التعارض الهندسي": in_desc, "الخطورة": in_sev, "الحالة": "معلقة"
                    })
                    st.success(f"تم حفظ الملحوذة بالرمز {new_code} بنجاح!")
                    st.rerun()

    with tab_ai_chat:
        st.subheader("💬 PIONX AI GPT - الشات الهندسي الذكي")
        current_p_data = st.session_state.projects_data[current_sel_proj]
        for m in current_p_data["chat_history"]:
            if m["sender"] == "User":
                st.markdown(f"<div class='user-box'>👨‍💼 <b>أنت:</b><br>{m['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ai-box'>🤖 <b>PIONX AI Bot:</b><br>{m['text']}</div>", unsafe_allow_html=True)
                
        user_msg_input = st.text_input("اسأل البوت عن أي تفاصيل في المشروع:")
        if st.button("إرسال الاستفسار"):
            if user_msg_input:
                ai_reply = f"تم فحص استفسارك حول '{user_msg_input}' ومطابقته مع قاعدة بيانات مشروع '{current_sel_proj}' لضمان الجودة وكود البناء."
                st.session_state.projects_data[current_sel_proj]["chat_history"].append({"sender": "User", "text": user_msg_input})
                st.session_state.projects_data[current_sel_proj]["chat_history"].append({"sender": "AI", "text": ai_reply})
                st.rerun()

    with tab_exporter:
        st.subheader("📄 توليد واستخراج تقارير الجودة والـ QC/QA الرسمية")
        current_p_data = st.session_state.projects_data[current_sel_proj]
        
        w_stream = io.BytesIO()
        w_stream.write(f"👑 تقرير فحص ومراجعة جودة المشروعات الهندسية - PCG CONSULTING GROUP\n".encode('utf-8'))
        w_stream.write(f"اسم المشروع: {current_sel_proj}\n".encode('utf-8'))
        w_stream.write(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d')}\n".encode('utf-8'))
        for note in current_p_data['notes']:
            w_stream.write(f"• [{note['كود الملاحظة']}] القسم: {note['القسم']} | الوصف: {note['تفاصيل التعارض الهندسي']}\n".encode('utf-8'))
            
        st.download_button(
            label="📥 تحميل التقرير التفصيلي بصيغة Word (قابل للتعديل)",
            data=w_stream.getvalue(),
            file_name=f"PCG_Quality_Report.doc",
            mime="application/msword"
        )

    with tab_settings:
        st.subheader("💳 بوابة إدارة الحساب المالي وباقات الـ SaaS")
        st.markdown("""
        <div style='background-color:#141414; padding:25px; border-radius:6px; border: 1px solid #aa7c11;'>
            <h4>📊 تفاصيل اشتراك مجموعة PCG الحالي للخدمة:</h4>
            <p>نوع الباقة المعتمدة: <b style='color:#d4af37;'>الباقة الاحترافية الكاملة (PIONX Pro SaaS License)</b></p>
            <p>حالة بوابة الدفع: <span style='color:#55ff55; font-weight:bold;'>مُسدّد ونشط (Active & Paid)</span></p>
        </div>
        """, unsafe_allow_html=True)
