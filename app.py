import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Sri Lanka AI Garage - Manager",
    page_icon="🚗",
    layout="centered"
)

# --- Global Session State Initialization ---
if "step" not in st.session_state:
    st.session_state.step = "proposal"
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# Users database structure: {username: {"password": str, "vehicles": [...], "expenses": [...]}}
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        # පෙරනිමියෙන් රහස් Admin ගිණුමක් (අවශ්‍ය නම් මෙයින් පරීක්ෂා කළ හැක)
        "admin_boss": {
            "password": "supersecretpassword123", 
            "vehicles": ["ADMIN-CAR"], 
            "expenses": []
        }
    }

# ==========================================
# STEP 1: PROJECT PROPOSAL PAGE
# ==========================================
if st.session_state.step == "proposal":
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
# STEP 2: USER AUTHENTICATION (Login / Sign Up)
# ==========================================
elif st.session_state.step == "auth":
    if st.button("⬅️ Back to Project Proposal"):
        st.session_state.step = "proposal"
        st.rerun()

    st.title("🔐 පරිශීලක ගිණුම (User Account)")
    st.markdown("ඔබගේ වාහන දත්ත සුරක්ෂිතව තබා ගැනීමට කරුණාකර ලොග් වන්න හෝ අලුත් ගිණුමක් සාදා ගන්න.")
    
    auth_tab1, auth_tab2 = st.tabs(["🔑 ලොග් වීම (Login)", "📝 ගිණුමක් තැනීම (Sign Up)"])
    
    with auth_tab1:
        st.subheader("පවතින ගිණුමකට පිවිසෙන්න")
        with st.form("login_form"):
            login_user = st.text_input("පරිශීලක නම (Username):").strip()
            login_pass = st.text_input("මුරපදය (Password):", type="password")
            login_btn = st.form_submit_button("ලොග් වන්න (Login)")
            
            if login_btn:
                if login_user in st.session_state.users_db and st.session_state.users_db[login_user]["password"] == login_pass:
                    st.session_state.logged_in_user = login_user
                    st.session_state.step = "app_dashboard"
                    st.success(f"සාර්ථකයි! සාදරයෙන් පිළිගනිමු, {login_user}!")
                    st.rerun()
                else:
                    st.error("❌ වැරදි පරිශීලක නමක් හෝ මුරපදයකි. කරුණාකර පරීක්ෂා කරන්න.")

    with auth_tab2:
        st.subheader("නව ගිණුමක් සාදාගන්න")
        with st.form("signup_form"):
            new_user = st.text_input("නව පරිශීලක නමක් (Username):").strip()
            new_pass = st.text_input("මුරපදයක් (Password):", type="password")
            signup_btn = st.form_submit_button("ගිණුම සාදන්න (Register)")
            
            if signup_btn:
                if new_user == "" or new_pass == "":
                    st.warning("⚠️ කරුණාකර නම සහ මුරපදය ඇතුළත් කරන්න.")
                elif new_user in st.session_state.users_db:
                    st.warning("⚠️ මෙම පරිශීලක නම දැනටමත් භාවිතා කර ඇත. වෙනත් නමක් තෝරන්න.")
                else:
                    st.session_state.users_db[new_user] = {
                        "password": new_pass,
                        "vehicles": [],
                        "expenses": []
                    }
                    st.success("✅ ගිණුම සාර්ථකව සාදන ලදී! දැන් 'Login' ටැබ් එකට ගොස් ලොග් වන්න.")

# ==========================================
# STEP 3: MAIN APP MANAGEMENT PORTAL
# ==========================================
elif st.session_state.step == "app_dashboard":
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

    # --- HIDDEN ADMIN PANEL (අනෙක් අයට නොපෙනෙන, ඔබට පමණක් පාලනය කළ හැකි කොටස) ---
    # ඔබගේ පරිශීලක නම "admin_boss" නම් පමණක් මෙම රහස් පාලක පුවරුව දිස්වේ.
    if current_user == "admin_boss":
        with st.expander("🛠️ [ADMIN ONLY] සියලුම පරිශීලක ගිණුම් සහ දත්ත පරීක්ෂා කිරීම"):
            st.warning("⚠️ ඔබ විශේෂ පරිපාලක (Admin) බලතල යටතේ සිටී. මෙහි සියලු ගිණුම් දත්ත පෙනේ.")
            for u_name, u_info in st.session_state.users_db.items():
                st.markdown(f"👤 **පරිශීලකයා:** `{u_name}` | **මුරපදය:** `{u_info['password']}`")
                st.write(f"🚗 වාහන: {u_info['vehicles']}")
                st.write(f"💰 වියදම් ගණන: {len(u_info['expenses'])}")
                st.markdown("---")

    # Get user specific data references
    user_data = st.session_state.users_db[current_user]

    st.subheader("🚗 1. නව වාහනයක් ලියාපදිංචි කිරීම හෝ මැකීම")
    
    # Vehicle registration form
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
                # Remove vehicle from list
                user_data["vehicles"].remove(del_vehicle)
                # Also remove associated expenses for this vehicle
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
            
            # Filter expenses for selected vehicle
            v_expenses = [i for i, exp in enumerate(user_data["expenses"]) if exp["Vehicle"] == selected_vehicle]
            
            if len(v_expenses) > 0:
                # Display table with index for identification
                display_data = []
                for idx in v_expenses:
                    item = user_data["expenses"][idx].copy()
                    item["ID"] = idx  # Keep track of original index
                    display_data.append(item)
                
                df = pd.DataFrame(display_data)
                total_spent = df["Cost (LKR)"].sum()
                st.metric(label="මෙම වාහනය සඳහා දැරූ මුළු වියදම", value=f"Rs. {total_spent:,.2f}")
                
                st.dataframe(df[["ID", "Category", "Cost (LKR)", "Details", "Date"]], use_container_width=True)
                
                # Delete specific expense entry form
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
