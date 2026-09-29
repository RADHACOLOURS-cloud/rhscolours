import streamlit as st
import pandas as pd
import openpyxl

# Page Configuration
st.set_page_config(
    page_title="RHS Colours - Dealer & Scheme Portal",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- FLIPKART STYLE 3D CUSTOM CSS -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background subtle gradient */
    .stApp {
        background-color: #F1F3F6;
    }

    /* Top E-commerce Style Navbar */
    .fk-navbar {
        background: linear-gradient(135deg, #2874F0 0%, #1A56B8 100%);
        padding: 14px 22px;
        border-radius: 12px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 8px 20px rgba(40, 116, 240, 0.25);
        margin-bottom: 20px;
    }
    .fk-navbar h2 {
        margin: 0;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    /* 3D Elevated Cards */
    .fk-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
        border: 1px solid #E2E8F0;
        margin-bottom: 18px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .fk-card:hover {
        box-shadow: 0 16px 32px -4px rgba(0, 0, 0, 0.12);
    }

    /* Badge Tags */
    .badge-admin {
        background: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
        border: 1px solid #FDE68A;
    }
    .badge-public {
        background: #ECFDF5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
        border: 1px solid #A7F3D0;
    }

    /* Search Input Styling */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
        border: 2px solid #E2E8F0 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04) !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #2874F0 !important;
    }

    /* Custom Buttons */
    .stButton>button {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.2s;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- ADMIN CREDENTIALS -----------------
ADMIN_USERS = {
    "admin": "rhspaint2026",
    "owner": "radha@sagar"
}

# ----------------- SESSION STATE -----------------
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "gst_rate" not in st.session_state:
    st.session_state.gst_rate = 14.0

if "scheme_val" not in st.session_state:
    st.session_state.scheme_val = 10.0

if "data_items" not in st.session_state:
    st.session_state.data_items = [
        {"name": "FIROZA", "pack": 0.1, "rate": 40.0},
        {"name": "FIROZA", "pack": 0.2, "rate": 70.0},
        {"name": "FIROZA", "pack": 0.5, "rate": 130.0},
        {"name": "FIROZA", "pack": 1.0, "rate": 250.0},
        {"name": "FIROZA", "pack": 4.0, "rate": 900.0},
        {"name": "FIROZA", "pack": 10.0, "rate": 2000.0},
        {"name": "WHITE",  "pack": 0.1, "rate": 50.0},
        {"name": "WHITE",  "pack": 0.2, "rate": 90.0},
        {"name": "WHITE",  "pack": 0.5, "rate": 160.0},
        {"name": "WHITE",  "pack": 1.0, "rate": 290.0},
        {"name": "WHITE",  "pack": 4.0, "rate": 1100.0},
        {"name": "WHITE",  "pack": 10.0, "rate": 2300.0},
        {"name": "BLACK",  "pack": 0.1, "rate": 35.0},
        {"name": "BLACK",  "pack": 0.2, "rate": 65.0},
        {"name": "BLACK",  "pack": 0.5, "rate": 120.0},
        {"name": "BLACK",  "pack": 1.0, "rate": 240.0},
        {"name": "BLACK",  "pack": 4.0, "rate": 850.0},
        {"name": "BLACK",  "pack": 10.0, "rate": 1900.0},
    ]

# ----------------- SIDEBAR (ADMIN AUTH & RESTRICTED ACTIONS) -----------------
with st.sidebar:
    st.markdown("### 🔐 Admin Controls")
    
    if not st.session_state.is_admin:
        u_name = st.text_input("Admin Username")
        u_pass = st.text_input("Password", type="password")
        if st.button("Unlock Admin Access", use_container_width=True):
            if u_name in ADMIN_USERS and ADMIN_USERS[u_name] == u_pass:
                st.session_state.is_admin = True
                st.success("Admin Logged In!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")
    else:
        st.markdown('<span class="badge-admin">Admin Mode Active</span>', unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state.is_admin = False
            st.rerun()

        st.markdown("---")
        st.subheader("⚙️ Global Rates")
        n_gst = st.number_input("GST Rate (%)", value=st.session_state.gst_rate, step=1.0)
        n_scheme = st.number_input("Scheme Per Litre (₹)", value=st.session_state.scheme_val, step=1.0)

        if st.button("Update Rates", use_container_width=True):
            st.session_state.gst_rate = float(n_gst)
            st.session_state.scheme_val = float(n_scheme)
            st.success("Rates Updated!")
            st.rerun()

        st.markdown("---")
        st.subheader("📁 Upload New Price List")
        uploaded_file = st.file_uploader("Upload Excel Sheet (.xlsx)", type=["xlsx"])
        
        if uploaded_file is not None:
            if st.button("Import & Skip Duplicates", use_container_width=True):
                try:
                    wb = openpyxl.load_workbook(uploaded_file, data_only=True)
                    ws = wb.active

                    # Auto read E5 & F5 if present
                    val_e5 = ws["E5"].value
                    val_f5 = ws["F5"].value
                    if val_e5 is not None:
                        try:
                            e5_flt = float(str(val_e5).replace("%", "").strip())
                            if 0 < e5_flt < 1:
                                e5_flt *= 100
                            st.session_state.gst_rate = e5_flt
                        except:
                            pass
                    if val_f5 is not None:
                        try:
                            st.session_state.scheme_val = float(str(val_f5).strip())
                        except:
                            pass

                    # Auto detect start row
                    start_row = 1
                    for r in range(1, 15):
                        row_vals = [str(ws.cell(row=r, column=c).value or "").strip().upper() for c in range(1, 6)]
                        if any("NAME" in x for x in row_vals) and any("PACK" in x for x in row_vals):
                            start_row = r + 1
                            break

                    existing_map = {(i["name"], i["pack"]): i for i in st.session_state.data_items}
                    added, updated, skipped = 0, 0, 0

                    for r in range(start_row, ws.max_row + 1):
                        b = ws.cell(row=r, column=2).value
                        c = ws.cell(row=r, column=3).value
                        d = ws.cell(row=r, column=4).value

                        if b and c and d:
                            n_str = str(b).strip().upper()
                            if n_str in ["NAME", "COLOUR NAME", "TOTAL", ""]:
                                continue
                            try:
                                p_num = float(str(c).strip())
                                r_num = float(str(d).strip())
                                key = (n_str, p_num)

                                if key in existing_map:
                                    if existing_map[key]["rate"] != r_num:
                                        existing_map[key]["rate"] = r_num
                                        updated += 1
                                    else:
                                        skipped += 1
                                else:
                                    existing_map[key] = {"name": n_str, "pack": p_num, "rate": r_num}
                                    added += 1
                            except ValueError:
                                continue

                    st.session_state.data_items = list(existing_map.values())
                    st.success(f"Added: {added} | Updated: {updated} | Skipped: {skipped}")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error parsing file: {e}")

# ----------------- TOP NAVBAR HEADER -----------------
role_badge = '<span class="badge-admin">ADMINISTRATOR</span>' if st.session_state.is_admin else '<span class="badge-public">COUNTER USER</span>'
st.markdown(f"""
<div class="fk-navbar">
    <div>
        <h2>🎨 RHS COLOURS & PAINTS RATE PORTAL</h2>
        <small style="opacity: 0.9;">Real-Time GST & Per Litre Scheme Engine</small>
    </div>
    <div>{role_badge}</div>
</div>
""", unsafe_allow_html=True)

# ----------------- SEARCH & METRICS CARD -----------------
st.markdown('<div class="fk-card">', unsafe_allow_html=True)
col_s1, col_s2 = st.columns([3, 1])
with col_s1:
    search_query = st.text_input("🔍 Quick Colour Search", placeholder="Type colour name (e.g. FIROZA, WHITE, BLACK)...").strip().upper()
with col_s2:
    if st.session_state.is_admin:
        st.markdown(f"**GST:** `{st.session_state.gst_rate}%` | **Scheme:** `₹{st.session_state.scheme_val}/L`")
    else:
        st.markdown("**Status:** `Rates Final (Inc. Scheme)`")
st.markdown('</div>', unsafe_allow_html=True)

# ----------------- DATA PREPARATION -----------------
calc_rows = []
for item in st.session_state.data_items:
    rate_gst = round(item["rate"] * (1 + (st.session_state.gst_rate / 100)), 2)
    final_rate = round(rate_gst - (item["pack"] * st.session_state.scheme_val), 2)
    
    row = {
        "COLOUR NAME": item["name"],
        "PACK (L/Kg)": item["pack"],
        "FINAL SCHEME RATE (₹)": final_rate
    }
    if st.session_state.is_admin:
        row["DEALER PRIZE (₹)"] = item["rate"]
        row["RATE WITH GST (₹)"] = rate_gst

    calc_rows.append(row)

df_all = pd.DataFrame(calc_rows)

if search_query:
    df_filtered = df_all[df_all["COLOUR NAME"].str.contains(search_query, case=False, na=False)]
else:
    df_filtered = df_all

# ----------------- 3D EXPANDABLE SECTION 1: SHOP PRINT GRID -----------------
with st.expander("🏪 SHOP PRINT MATRIX GRID (TOUCH TO EXPAND / COLLAPSE)", expanded=True):
    if not df_filtered.empty:
        pivot_df = df_filtered.pivot_table(index="COLOUR NAME", columns="PACK (L/Kg)", values="FINAL SCHEME RATE (₹)", aggfunc="first")
        pivot_df = pivot_df.round(2).fillna("-")

        # Visual Table Display
        st.dataframe(
            pivot_df.style.format(precision=2, na_rep="-").set_properties(**{
                'font-weight': '600',
                'color': '#1E293B',
                'background-color': '#FFFDF7'
            }),
            use_container_width=True,
            height=300
        )

        csv_grid = pivot_df.to_csv().encode('utf-8')
        st.download_button("📥 Download Shop Matrix (CSV)", data=csv_grid, file_name="RHS_Shop_Matrix.csv", mime="text/csv")
    else:
        st.warning("Koi match nahi mila.")

# ----------------- 3D EXPANDABLE SECTION 2: ITEM REPORT -----------------
with st.expander("📋 ITEM WISE BREAKDOWN (TOUCH TO EXPAND / COLLAPSE)", expanded=False):
    if not df_filtered.empty:
        if st.session_state.is_admin:
            display_cols = ["COLOUR NAME", "PACK (L/Kg)", "DEALER PRIZE (₹)", "RATE WITH GST (₹)", "FINAL SCHEME RATE (₹)"]
        else:
            display_cols = ["COLOUR NAME", "PACK (L/Kg)", "FINAL SCHEME RATE (₹)"]

        st.dataframe(
            df_filtered[display_cols].style.set_properties(**{
                'background-color': '#FFFFFF'
            }),
            use_container_width=True,
            height=320
        )

        csv_item = df_filtered[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Breakdown Report (CSV)", data=csv_item, file_name="RHS_Item_Report.csv", mime="text/csv")
    else:
        st.warning("Koi data uplabdh nahi hai.")
