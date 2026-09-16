import streamlit as st
import pandas as pd
import hashlib
import time

# Page Configuration
st.set_page_config(
    page_title="Sri Lanka AI Garage - Manager",
    page_icon="🚗",
    layout="centered"
)

# --- Security Helper Functions ---
def hash_password(password):
    """මුරපදය SHA-256 මඟින් Encrypt කරයි"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    """ඇතුළත් කළ මුරපදය සහ Hash එක සමාන දැයි පරීක්ෂා කරයි"""
    return hash_password(password) == hashed

# --- Global Session State Initialization ---
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# Login attempt tracker for security (Brute-force protection)
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = {}

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = {}

# Users database structure (Admin ගිණුමේ මුරපදය ද Hash කර සේවා කර ඇත)
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin_boss": {
            "password": hash_password("supersecretpassword123"), 
            "vehicles": ["ADMIN-CAR"], 
            "expenses": []
        }
    }

# Determine current step based on login status
if st.session_state.logged_in_user is not None:
    current_step = "app_dashboard"
else:
    if "step" not in st.session_state:
        st.session_state.step = "proposal"
    current_step = st.session_state.step


# ==========================================
# STEP 1: PROJECT PROPOSAL PAGE
# ==========================================
if current_step == "proposal":
    st.title("🚗 Sri Lanka AI Garage: Project Proposal")
    st.markdown("අපගේ ව්‍යාපෘතියේ ව්‍යාපාරික යෝජනාව (Proposal) පහත දැක්වේ:")
    st.markdown("---")
    
    with st.expander("📌 1. හැඳින්වීම (Introduction)", expanded=True):
        st.write(
            "**Sri Lanka AI Garage** යනු ශ්‍රී ලංකාවේ වාහන හිමිකරුවන්ට තම වාහනවල ඉන්ධන පරිභෝජනය, "
            "නඩත්තු වියදම් සහ සේවා කාලසටහන් පහසුවෙන් කළමනාකරණය කරගැනීමට සහය වන ඩිජිටල් වේදිකාවකි."
        )
    
    with st.expander("🎯 2. ව්‍යාපෘතියේ අරමුණු (Objectives)"):
        st.markdown("""
        * 🚗 වාහන නඩත්තු වියදම් නිවැරදිව වාර්තා කරගැනීම සහ විශ්ලේෂණය කිරීම.
        * ⛽ ඉන්ධන කාර්යක්ෂමතාව (Fuel Efficiency) පාලනය කරගැනීම.
        * 📉 අනපේක්ෂිත අලුත්වැඩියා වියදම් අවම කරගැනීම.
        """)

    with st.expander("🌐 3. සම්බන්ධ වීමට (Contact & Sponsorship)"):
        facebook_link = "https://www.facebook.com/share/1CmkuWayeL/"
        st.markdown(f"👉 **[Sri Lanka AI Garage Facebook Page වෙත පිවිසෙන්න]({facebook_link})**", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Next ➡️ (Go to Login / App)", use_container_width=True, type="primary"):
        st.session_state.step = "auth"
        st.rerun()

# ==========================================
# STEP 2: SECURE USER AUTHENTICATION
# ==========================================
elif current_step == "auth":
    if st.button("⬅️ Back to Project Proposal"):
        st.session_state.step = "proposal"
        st.rerun()

    st.title("🔐 ආරක්ෂිත පරිශීලක ගිණුම (Secure User Account)")
    st.markdown("ඔබගේ වාහන දත්ත ඉහළම ආරක්ෂාව යටතේ තබා ගැනීමට කරුණාකර ලොග් වන්න.")
    
    auth_tab1, auth_tab2 = st.tabs(["🔑 ලොග් වීම (Login)", "📝 ගිණුමක් තැනීම (Sign Up)"])
    
    with auth_tab1:
        st.subheader("පවතින ගිණුමකට පිවිසෙන්න")
        with st.form("login_form"):
            login_user = st.text_input("පරිශීලක නම (Username):").strip()
            login_pass = st.text_input("මුරපදය (Password):", type="password")
            login_btn = st.form_submit_button("ලොග් වන්න (Login)")
            
            if login_btn:
                # Check for lockout
                current_time = time.time()
                if login_user in st.session_state.lockout_time:
                    remaining_lock = st.session_state.lockout_time[login_user] - current_time
                    if remaining_lock > 0:
                        st.error(f"🚫 ආරක්ෂක හේතු මත මෙම ගිණුම තාවකාලිකව අගුළු දමා ඇත. කරුණාකර තවත් තත්පර {int(remaining_lock)}කින් උත්සාහ කරන්න.")
                        st.stop()
                    else:
                        del st.session_state.lockout_time[login_user]
                        st.session_state.login_attempts[login_user] = 0

                if login_user in st.session_state.users_db and check_password(login_pass, st.session_state.users_db[login_user]["password"]):
                    # Reset attempts on successful login
                    st.session_state.login_attempts[login_user] = 0
                    st.session_state.logged_in_user = login_user
                    st.success(f"සාර්ථකයි! සාදරයෙන් පිළිගනිමු, {login_user}!")
                    st.rerun()
                else:
                    # Track failed attempts
                    if login_user not in st.session_state.login_attempts:
                        st.session_state.login_attempts[login_user] = 0
                    st.session_state.login_attempts[login_user] += 1
                    
                    attempts_left = 3 - st.session_state.login_attempts[login_user]
                    if attempts_left > 0:
                        st.error(f"❌ වැරදි පරිශීලක නමක් හෝ මුරපදයකි. ඔබට ඉතිරිව ඇත්තේ උත්සාහයන් {attempts_left} කි.")
                    else:
                        st.session_state.lockout_time[login_user] = time.time() + 30  # Lock for 30 seconds
                        st.error("🚫 වැරදි මුරපද වාර ගණන ඉක්මවා ඇත! ආරක්ෂාව සඳහා ගිණුම තත්පර 30කට අගුළු දමන ලදී.")

    with auth_tab2:
        st.subheader("නව ගිණුමක් සාදාගන්න")
        st.info("💡 **ආරක්ෂක නීති:** මුරපදය අවම වශයෙන් අක්ෂර 8ක්වත් දිග විය යුතු අතර, අංක සහ අකුරු අඩංගු විය යුතුය.")
        with st.form("signup_form"):
            new_user = st.text_input("නව පරිශීලක නමක් (Username):").strip()
            new_pass = st.text_input("මුරපදයක් (Password):", type="password")
            signup_btn = st.form_submit_button("ගිණුම සාදන්න (Register)")
            
            if signup_btn:
                if new_user == "" or new_pass == "":
                    st.warning("⚠️ කරුණාකර නම සහ මුරපදය ඇතුළත් කරන්න.")
                elif len(new_pass) < 8:
                    st.warning("⚠️ මුරපදය ඉතා කෙටි වේ. කරුණාකර අවම වශයෙන් අක්ෂර 8ක්වත් යොදන්න.")
                elif new_user in st.session_state.users_db:
                    st.warning("⚠️ මෙම පරිශීලක නම දැනටමත් භාවිතා කර ඇත. වෙනත් නමක් තෝරන්න.")
                else:
                    # Save with Hashed Password
                    st.session_state.users_db[new_user] = {
                        "password": hash_password(new_pass),
                        "vehicles": [],
                        "expenses": []
                    }
                    st.success("✅ ගිණුම ආරක්ෂිතව සාදන ලදී! දැන් 'Login' ටැබ් එකට ගොස් ලොග් වන්න.")

# ==========================================
# STEP 3: MAIN APP MANAGEMENT PORTAL
# ==========================================
elif current_step == "app_dashboard":
    current_user = st.session_state.logged_in_user
    
    # Top bar with user greeting and logout
    col_u1, col_u2 = st.columns([3, 1])
    with col_u1:
        st.title(f"🚗 {current_user}ගේ වාහන කළමනාකරණය")
    with col_u2:
        if st.button("🚪 ඉවත් වන්න (Logout)"):
            st.session_state.logged_in_user = None
            st.session_state.step = "proposal"
            st.rerun()

    st.markdown("---")

    # --- ADMIN ONLY PANEL WITH USER SELECTOR ---
    if current_user == "admin_boss":
        with st.expander("🛠️ [ADMIN PANEL] සියලුම පරිශීලක ගිණුම් පරීක්ෂා කිරීම", expanded=True):
            st.warning("⚠️ ඔබ Admin බලතල යටතේ සිටී. පහත ලැයිස්තුවෙන් පරිශීලකයෙකු තෝරා ඔහුගේ විස්තර බලන්න:")
            
            all_users = list(st.session_state.users_db.keys())
            selected_target_user = st.selectbox("පරිශීලකයන්ගේ ලැයිස්තුවෙන් කෙනෙක් තෝරන්න:", all_users)
            
            if selected_target_user:
                t_info = st.session_state.users_db[selected_target_user]
                st.markdown(f"### 👤 පරිශීලකයා: `{selected_target_user}`")
                st.write(f"🔑 **මුරපද Hash එක (ආරක්ෂිතව සේව් වී ඇත):** `{t_info['password'][:15]}...`")
                st.write(f"🚗 **ලියාපදිංචි වාහන:** {t_info['vehicles']}")
                
                if len(t_info['expenses']) > 0:
                    st.write("💰 **වියදම් විස්තර:**")
                    st.dataframe(pd.DataFrame(t_info['expenses']), use_container_width=True)
                else:
                    st.info("මෙම පරිශීලකයා තවම වියදම් එකතු කර නැත.")
            st.markdown("---")

    # Get user specific data references for regular usage
    user_data = st.session_state.users_db[current_user]

    st.subheader("🚗 1. නව වාහනයක් ලියාපදිංචි කිරීම හෝ මැකීම")
    
    with st.form("vehicle_form_center"):
        v_name = st.text_input("වාහන අංකය (උදා: WP CAB-1234):").upper()
        add_submitted = st.form_submit_button("වාහනය එකතු කරන්න")
        
        if add_submitted and v_name.strip() != "":
            if len(v_name.strip()) >= 4:
                if v_name not in user_data["vehicles"]:
                    user_data["vehicles"].append(v_name)
                    st.success(f"'{v_name}' වාහනය සාර්ථකව ඔබේ ගිණුමට එකතු කරන ලදී!")
                    st.rerun()
                else:
                    st.warning("මෙම වාහනය දැනටමත් ඔබේ ගිණුමේ ලියාපදිංචි කර ඇත.")
            else:
                st.error("❌ කාරුණාකර సరైన ශ්‍රී ලංකා වාහන අංකයක් ඇතුළත් කරන්න.")

    # Vehicle Deletion Section
    if len(user_data["vehicles"]) > 0:
        st.markdown("##### 🗑️ ලියාපදිංචි වාහනයක් ඉවත් කිරීම (Delete Vehicle)")
        with st.form("delete_vehicle_form"):
            del_vehicle = st.selectbox("මකා දැමිය යුතු වාහනය තෝරන්න:", user_data["vehicles"])
            del_v_btn = st.form_submit_button("තෝරාගත් වාහනය මකන්න")
            
            if del_v_btn:
                user_data["vehicles"].remove(del_vehicle)
                user_data["expenses"] = [exp for exp in user_data["expenses"] if exp["Vehicle"] != del_vehicle]
                st.success(f"✅ '{del_vehicle}' වාහනය සහ එයට අදාළ දත්ත සාර්ථකව ඉවත් කරන ලදී!")
                st.rerun()

    # If user has registered vehicles
    if len(user_data["vehicles"]) > 0:
        st.markdown("---")
        st.subheader("⚙️ 2. වාහනය තෝරා ගැනීම සහ වියදම් කළමනාකරණය")
        selected_vehicle = st.selectbox("පාලනය කිරීමට අවශ්‍ය වාහනය තෝරන්න:", user_data["vehicles"])
        st.markdown("---")

        tab1, tab2 = st.tabs(["⛽ වියදම් ඇතුළත් කරන්න (Add Expense)", "📊 වියදම් වාර්තා හා මැකීම (Dashboard & Delete)"])
        
        with tab1:
            st.subheader(f"⛽ {selected_vehicle} - නව වියදමක් එකතු කිරීම")
            with st.form("expense_form_center"):
                category = st.selectbox("වියදම් වර්ගය:", ["Fuel", "Full Service", "Tyre Change", "Repairs", "Other"])
                cost = st.number_input("මුළු මුදල (LKR):", min_value=0.0, value=3000.0)
                
                fuel_info = ""
                if category == "Fuel":
                    fuel_type = st.selectbox("ඉන්ධන වර්ගය:", ["Petrol 92", "Petrol 95", "Auto Diesel", "Super Diesel"])
                    price_dict = {
                        "Petrol 92": 370.0,
                        "Petrol 95": 410.0,
                        "Auto Diesel": 360.0,
                        "Super Diesel": 410.0
                    }
                    unit_price = price_dict.get(fuel_type, 370.0)
                    calculated_litres = cost / unit_price if unit_price > 0 else 0
                    st.caption(f"💡 ඇස්තමේන්තුගත ලීටර් ප්‍රමාණය: **{calculated_litres:.2f} L**")
                    fuel_info = f" [{fuel_type}: {calculated_litres:.2f}L]"

                details = st.text_input("අතිරේක විස්තර (අවශ්‍ය නම්):")
                log_date = st.date_input("දිනය:")
                
                exp_submitted = st.form_submit_button("වියදම සුරකින්න")
                if exp_submitted:
                    final_details = details + fuel_info if category == "Fuel" else details
                    user_data["expenses"].append({
                        "Vehicle": selected_vehicle,
                        "Category": category,
                        "Cost (LKR)": cost,
                        "Details": final_details,
                        "Date": str(log_date)
                    })
                    st.success("දත්ත සාර්ථකව ගිණුමේ සුරකින ලදී!")
                    st.rerun()
                    
        with tab2:
            st.subheader(f"📊 {selected_vehicle} - වියදම් වාර්තාව සහ ඉවත් කිරීම")
            
            v_expenses = [i for i, exp in enumerate(user_data["expenses"]) if exp["Vehicle"] == selected_vehicle]
            
            if len(v_expenses) > 0:
                display_data = []
                for idx in v_expenses:
                    item = user_data["expenses"][idx].copy()
                    item["ID"] = idx
                    display_data.append(item)
                
                df = pd.DataFrame(display_data)
                total_spent = df["Cost (LKR)"].sum()
                st.metric(label="මෙම වාහනය සඳහා දැරූ මුළු වියදම", value=f"Rs. {total_spent:,.2f}")
                
                st.dataframe(df[["ID", "Category", "Cost (LKR)", "Details", "Date"]], use_container_width=True)
                
                st.markdown("##### 🗑️ නිශ්චිත වියදම් සටහනක් මකන්න")
                with st.form("delete_expense_form"):
                    exp_to_del = st.selectbox("මකා දැමිය යුතු වියදමේ ID අංකය තෝරන්න:", v_expenses)
                    del_exp_btn = st.form_submit_button("වියදම් සටහන මකන්න")
                    
                    if del_exp_btn:
                        user_data["expenses"].pop(exp_to_del)
                        st.success("✅ අදාළ වියදම් සටහන සාර්ථකව මකා දමන ලදී!")
                        st.rerun()
            else:
                st.info("මෙම වාහනය සඳහා තවම වියදම් ඇතුළත් කර නැත.")
    else:
        st.info("💡 කරුණාකර ඉහත පෝරමයෙන් ඔබගේ වාහන අංකය ඇතුළත් කර ලියාපදිංචි කරන්න.")
