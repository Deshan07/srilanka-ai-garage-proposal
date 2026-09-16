import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Sri Lanka AI Garage - Proposal & Manager",
    page_icon="🚗",
    layout="wide"
)

# --- Session State for Step Navigation & App Data ---
if "step" not in st.session_state:
    st.session_state.step = "proposal"
if "vehicles" not in st.session_state:
    st.session_state.vehicles = []
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ==========================================
# STEP 1: PROJECT PROPOSAL PAGE
# ==========================================
if st.session_state.step == "proposal":
    st.title("🚗 Sri Lanka AI Garage: Project Proposal")
    st.markdown("අපගේ ව්‍යාපෘතියේ ව්‍යාපාරික යෝජනාව (Proposal) පහත දැක්වේ. විස්තර බැලීමට මාතෘකා මත ක්ලික් කරන්න:")
    st.markdown("---")
    
    # Folder / Expander 1: Introduction
    with st.expander("📌 1. හැඳින්වීම (Introduction)", expanded=True):
        st.write(
            "**Sri Lanka AI Garage** යනු ශ්‍රී ලංකාවේ වාහන හිමිකරුවන්ට තම වාහනවල ඉන්ධන පරිභෝජනය, "
            "නඩත්තු වියදම් සහ සේවා කාලසටහන් පහසුවෙන් කළමනාකරණය කරගැනීමට සහය වන ඩිජිටල් වේදිකාවකි. "
            "මෙය නවීන කෘත්‍රිම බුද්ධිය (AI) සහ දත්ත විශ්ලේෂණ තාක්ෂණය භාවිතයෙන් සකස් කරන ලද්දකි."
        )
    
    # Folder / Expander 2: Objectives
    with st.expander("🎯 2. ව්‍යාපෘතියේ අරමුණු (Objectives)"):
        st.markdown("""
        * 🚗 වාහන නඩත්තු වියදම් නිවැරදිව වාර්තා කරගැනීම සහ විශ්ලේෂණය කිරීම.
        * ⛽ ඉන්ධන කාර්යක්ෂමතාව (Fuel Efficiency) පාලනය කරගැනීම.
        * 📉 අනපේක්ෂිත අලුත්වැඩියා වියදම් අවම කරගැනීම සඳහා පූර්ව දැනුම්දීම් ලබා දීම.
        * 🌐 ශ්‍රී ලංකේය වාහන ප්‍රජාව සඳහා ඩිජිටල් ප්‍රජා මධ්‍යස්ථානයක් (Community Hub) නිර්මාණය කිරීම.
        """)

    # Folder / Expander 3: Expected Benefits
    with st.expander("💡 3. අපේක්ෂිත ප්‍රතිලාභ (Expected Benefits)"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**මූල්‍ය පාලනය**\n\nමාසිකව වාහනය සඳහා වැයවන මුදල් පිළිබඳ පැහැදිලි චිත්‍රයක් ලබා ගැනීම.")
        with col2:
            st.info("**කාලය ඉතිරිකිරීම**\n\nසේවා කළ යුතු දින සහ බලපත්‍ර අලුත් කළ යුතු දින කලින්ම දැන ගැනීම.")
        with col3:
            st.info("**විනිවිදභාවය**\n\nසියලුම වාහන දත්ත එකම තැනක සුරක්ෂිතව තබා ගැනීම.")

    # Folder / Expander 4: Contact & Social Media
    with st.expander("🌐 4. සම්බන්ධ වීමට සහ අනුග්‍රහය දැක්වීමට (Contact & Sponsorship)"):
        st.write("මෙම ව්‍යාපෘතිය හා සම්බන්ධ වීමට හෝ වැඩි විස්තර දැනගැනීමට අපගේ නිල ෆේස්බුක් පිටුව වෙත පිවිසෙන්න:")
        facebook_link = "https://www.facebook.com/share/1CmkuWayeL/"
        st.markdown(f"👉 **[Sri Lanka AI Garage Facebook Page වෙත පිවිසෙන්න]({facebook_link})**", unsafe_allow_html=True)

    st.markdown("---")
    
    # Next Button to go to the App
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Next ➡️ (Go to Vehicle App Dashboard)", use_container_width=True, type="primary"):
            st.session_state.step = "app"
            st.rerun()

# ==========================================
# STEP 2: APP DASHBOARD & MANAGEMENT SECTION
# ==========================================
elif st.session_state.step == "app":
    # Back button to return to Proposal
    if st.button("⬅️ Back to Project Proposal"):
        st.session_state.step = "proposal"
        st.rerun()
        
    st.title("🚗 Sri Lanka AI Garage: Management Portal")
    st.markdown("---")

    # If no vehicles registered yet, show Add Vehicle form directly in the center
    if len(st.session_state.vehicles) == 0:
        st.warning("⚠️ කරුණාකර ඔබගේ පළමු වාහනය මෙහි පහතින් ලියාපදිංචි කරන්න:")
        with st.form("initial_vehicle_form"):
            v_name = st.text_input("වාහනයේ නම / අංකය (උදා: WP CAB-1234):")
            v_type = st.selectbox("වාහන වර්ගය:", ["Car", "SUV", "Bike", "Three-Wheeler", "Van"])
            submitted = st.form_submit_button("වාහනය එකතු කරන්න")
            
            if submitted and v_name.strip() != "":
                st.session_state.vehicles.append(v_name)
                st.success(f"'{v_name}' සාර්ථකව එකතු කරන ලදී! ඇප් එක ක්‍රියාත්මක වේ...")
                st.rerun()
    else:
        # --- Sidebar Menu for App (Once vehicle exists) ---
        st.sidebar.header("📂 ඇප් මෙනුව (App Navigation)")
        menu = st.sidebar.selectbox(
            "පිටුව තෝරන්න:", 
            ["📊 Vehicle Expense Dashboard", "➕ Add Another Vehicle", "⛽ Add Fuel/Service Log"]
        )

        # 1. Add Another Vehicle Section
        if menu == "➕ Add Another Vehicle":
            st.subheader("🚗 තවත් වාහනයක් එකතු කිරීම")
            with st.form("vehicle_form_extra"):
                v_name = st.text_input("වාහනයේ නම / අංකය:")
                v_type = st.selectbox("වාහන වර්ගය:", ["Car", "SUV", "Bike", "Three-Wheeler", "Van"])
                submitted = st.form_submit_button("වාහනය එකතු කරන්න")
                
                if submitted and v_name.strip() != "":
                    if v_name not in st.session_state.vehicles:
                        st.session_state.vehicles.append(v_name)
                        st.success(f"'{v_name}' සාර්ථකව එකතු කරන ලදී!")
                    else:
                        st.warning("මෙම වාහනය දැනටමත් ලියාපදිංචි කර ඇත.")

        selected_vehicle = st.sidebar.selectbox("වාහනය තෝරන්න:", st.session_state.vehicles)

        # 2. Add Fuel / Expense Log
        if menu == "⛽ Add Fuel/Service Log":
            st.subheader(f"⛽ {selected_vehicle} - දත්ත ඇතුළත් කිරීම")
            with st.form("expense_form"):
                category = st.selectbox("වර්ගය:", ["Fuel", "Full Service", "Tyre Change", "Repairs", "Other"])
                cost = st.number_input("මුළු මුදල (LKR):", min_value=0.0, value=2500.0)
                details = st.text_input("විස්තර:")
                log_date = st.date_input("දිනය:")
                
                exp_submitted = st.form_submit_button("දත්ත සුරකින්න")
                if exp_submitted:
                    st.session_state.expenses.append({
                        "Vehicle": selected_vehicle,
                        "Category": category,
                        "Cost (LKR)": cost,
                        "Details": details,
                        "Date": str(log_date)
                    })
                    st.success("දත්ත සාර්ථකව සුරකින ලදී!")

        # 3. Dashboard Section
        elif menu == "📊 Vehicle Expense Dashboard" or menu == "➕ Add Another Vehicle":
            st.subheader(f"📊 {selected_vehicle} - වියදම් සාරාංශය")
            
            if len(st.session_state.expenses) > 0:
                df = pd.DataFrame(st.session_state.expenses)
                v_df = df[df["Vehicle"] == selected_vehicle]
                
                if not v_df.empty:
                    total_spent = v_df["Cost (LKR)"].sum()
                    st.metric(label="මුළු වියදම", value=f"Rs. {total_spent:,.2f}")
                    st.dataframe(v_df, use_container_width=True)
                else:
                    st.info("මෙම වාහනය සඳහා තවම වියදම් ඇතුළත් කර නැත.")
            else:
                st.info("තවම කිසිදු දත්තයක් ඇතුළත් කර නැත. වම්පස මෙනුවෙන් 'Add Fuel/Service Log' වෙත ගොස් වියදම් එකතු කරන්න.")
