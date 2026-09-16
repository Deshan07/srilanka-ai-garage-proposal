import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Sri Lanka AI Garage - Proposal & Manager",
    page_icon="🚗",
    layout="centered"
)

# --- Session State Initialization ---
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
        st.info("**මූල්‍ය පාලනය:** මාසිකව වාහනය සඳහා වැයවන මුදල් පිළිබඳ පැහැදිලි චිත්‍රයක් ලබා ගැනීම.")
        st.info("**කාලය ඉතිරිකිරීම:** සේවා කළ යුතු දින සහ බලපත්‍ර අලුත් කළ යුතු දින කලින්ම දැන ගැනීම.")
        st.info("**විනිවිදභාවය:** සියලුම වාහන දත්ත එකම තැනක සුරක්ෂිතව තබා ගැනීම.")

    # Folder / Expander 4: Contact & Social Media
    with st.expander("🌐 4. සම්බන්ධ වීමට සහ අනුග්‍රහය දැක්වීමට (Contact & Sponsorship)"):
        st.write("මෙම ව්‍යාපෘතිය හා සම්බන්ධ වීමට හෝ වැඩි විස්තර දැනගැනීමට අපගේ නිල ෆේස්බුක් පිටුව වෙත පිවිසෙන්න:")
        facebook_link = "https://www.facebook.com/share/1CmkuWayeL/"
        st.markdown(f"👉 **[Sri Lanka AI Garage Facebook Page වෙත පිවිසෙන්න]({facebook_link})**", unsafe_allow_html=True)

    st.markdown("---")
    
    # Next Button to go to the App
    if st.button("Next ➡️ (Go to Vehicle App Dashboard)", use_container_width=True, type="primary"):
        st.session_state.step = "app"
        st.rerun()

# ==========================================
# STEP 2: APP MANAGEMENT PORTAL (Center Flow)
# ==========================================
elif st.session_state.step == "app":
    # Back button to return to Proposal
    if st.button("⬅️ Back to Project Proposal"):
        st.session_state.step = "proposal"
        st.rerun()
        
    st.title("🚗 Sri Lanka AI Garage: Management Portal")
    st.markdown("---")

    # 1. Add Vehicle Section
    st.subheader("🚗 1. වාහනයක් ලියාපදිංචි කිරීම / තෝරා ගැනීම")
    
    with st.form("vehicle_form_center"):
        v_name = st.text_input("වාහනයේ නම / අංකය (උදා: WP CAB-1234):")
        v_type = st.selectbox("වාහන වර්ගය:", ["Car", "SUV", "Bike", "Three-Wheeler", "Van"])
        add_submitted = st.form_submit_button("වාහනය එකතු කරන්න")
        
        if add_submitted and v_name.strip() != "":
            if v_name not in st.session_state.vehicles:
                st.session_state.vehicles.append(v_name)
                st.success(f"'{v_name}' සාර්ථකව එකතු කරන ලදී!")
            else:
                st.warning("මෙම වාහනය දැනටමත් ලියාපදිංචි කර ඇත.")

    # If vehicles exist
    if len(st.session_state.vehicles) > 0:
        st.markdown("---")
        st.subheader("⚙️ 2. වාහනය තෝරා දත්ත ඇතුළත් කිරීම")
        
        selected_vehicle = st.selectbox("පාලනය කිරීමට අවශ්‍ය වාහනය තෝරන්න:", st.session_state.vehicles)

        action_choice = st.radio("කරන් අවශ්‍ය දේ තෝරන්න:", ["⛽ ඉන්ධන හෝ සේවා වියදම් ඇතුළත් කරන්න (Add Expense)", "📊 වියදම් සාරාංශය බලන්න (Dashboard)"])
        
        if action_choice == "⛽ ඉන්ධන හෝ සේවා වියදම් ඇතුළත් කරන්න (Add Expense)":
            with st.form("expense_form_center"):
                category = st.selectbox("වියදම් වර්ගය:", ["Fuel", "Full Service", "Tyre Change", "Repairs", "Other"])
                cost = st.number_input("මුළු මුදල (LKR):", min_value=0.0, value=3000.0)
                
                # If fuel is selected, calculate litres automatically based on standard SL fuel prices
                fuel_info = ""
                if category == "Fuel":
                    fuel_type = st.selectbox("ඉන්ධන වර්ගය:", ["Petrol 92", "Petrol 95", "Auto Diesel", "Super Diesel"])
                    # Approximate standard prices per litre in LKR
                    price_dict = {
                        "Petrol 92": 370.0,
                        "Petrol 95": 410.0,
                        "Auto Diesel": 360.0,
                        "Super Diesel": 410.0
                    }
                    unit_price = price_dict.get(fuel_type, 370.0)
                    calculated_litres = cost / unit_price if unit_price > 0 else 0
                    st.caption(f"💡 ඇස්තමේන්තුගත ලීටර් ප්‍රමාණය: **{calculated_litres:.2f} L** (මිල ලීටරයකට රු. {unit_price} ලෙස)")
                    fuel_info = f" [{fuel_type}: {calculated_litres:.2f}L]"

                details = st.text_input("අතිරේක විස්තර (අවශ්‍ය නම්):")
                log_date = st.date_input("දිනය:")
                
                exp_submitted = st.form_submit_button("වියදම සුරකින්න")
                if exp_submitted:
                    final_details = details + fuel_info if category == "Fuel" else details
                    st.session_state.expenses.append({
                        "Vehicle": selected_vehicle,
                        "Category": category,
                        "Cost (LKR)": cost,
                        "Details": final_details,
                        "Date": str(log_date)
                    })
                    st.success("දත්ත සාර්ථකව සුරකින ලදී!")
                    
        elif action_choice == "📊 වියදම් සාරාංශය බලන්න (Dashboard)":
            st.markdown(f"### 📊 {selected_vehicle} - වියදම් වාර්තාව")
            
            if len(st.session_state.expenses) > 0:
                df = pd.DataFrame(st.session_state.expenses)
                v_df = df[df["Vehicle"] == selected_vehicle]
                
                if not v_df.empty:
                    total_spent = v_df["Cost (LKR)"].sum()
                    st.metric(label="මෙම වාහනය සඳහා දැරූ මුළු වියදම", value=f"Rs. {total_spent:,.2f}")
                    st.dataframe(v_df, use_container_width=True)
                else:
                    st.info("මෙම වාහනය සඳහා තවම වියදම් ඇතුළත් කර නැත.")
            else:
                st.info("තවම කිසිදු වියදම් දත්තයක් ඇතුළත් කර නැත.")
    else:
        st.info("💡 කරුණාකර ඉහත පෝරමයෙන් ඔබගේ පළමු වාහනය එකතු කරන්න.")
