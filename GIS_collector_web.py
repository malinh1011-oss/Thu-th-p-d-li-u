"""
GIS Collector Web App (Streamlit)
Author: Linh + GPT-5
Version: 1.0

Usage:
1. Install dependencies:
   pip install streamlit pandas openpyxl
2. Run app:
   streamlit run GIS_collector_web.py
"""

import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime

DEFAULT_COLLECTED_COL = "Collected"

st.set_page_config(page_title="GIS Data Collector (Web)", layout="wide")
st.title("📊 GIS Data Collector — Web App")

# --- SIDEBAR ---
st.sidebar.header("Workbook Source")
mode = st.sidebar.radio("Load from:", ("Upload Excel file", "Enter local file path"))

uploaded_file, file_path_input = None, None
if mode == "Upload Excel file":
    uploaded_file = st.sidebar.file_uploader("Upload .xlsx or .xls", type=["xlsx", "xls"])
else:
    file_path_input = st.sidebar.text_input("Full path to Excel file (server-local)")

# --- Helper functions ---
@st.cache_data
def list_sheets(source, sheet_source_type):
    try:
        if sheet_source_type == "upload":
            xls = pd.ExcelFile(io.BytesIO(source))
        else:
            xls = pd.ExcelFile(source)
        return xls.sheet_names
    except Exception:
        return []

@st.cache_data
def load_sheet(source, sheet_name, source_type):
    if source_type == "upload":
        df = pd.read_excel(io.BytesIO(source), sheet_name=sheet_name)
    else:
        df = pd.read_excel(source, sheet_name=sheet_name)
    return df

# --- Load workbook ---
if uploaded_file:
    file_bytes = uploaded_file.read()
    sheets = list_sheets(file_bytes, "upload")
    source_type = "upload"
elif file_path_input:
    sheets = list_sheets(file_path_input, "path")
    source_type = "path"
else:
    sheets, source_type = [], None

if not sheets:
    st.info("⬆️ Upload hoặc nhập đường dẫn đến file Excel để bắt đầu.")
    st.stop()

sheet = st.sidebar.selectbox("Chọn Sheet", sheets)
df = load_sheet(file_bytes if source_type == "upload" else file_path_input, sheet, source_type)

if DEFAULT_COLLECTED_COL not in df.columns:
    df[DEFAULT_COLLECTED_COL] = False

# --- Filter ---
st.sidebar.header("Filter")
search = st.sidebar.text_input("Search text")
filter_choice = st.sidebar.selectbox("Show", ("All", "Collected", "Not collected"))

filtered = df.copy()
if search:
    mask = pd.Series(False, index=filtered.index)
    for c in filtered.columns:
        mask |= filtered[c].astype(str).str.contains(search, case=False, na=False)
    filtered = filtered[mask]

if filter_choice == "Collected":
    filtered = filtered[filtered[DEFAULT_COLLECTED_COL] == True]
elif filter_choice == "Not collected":
    filtered = filtered[filtered[DEFAULT_COLLECTED_COL] == False]

# --- Summary ---
col1, col2, col3 = st.columns([1,1,2])
with col1:
    st.metric("Total Rows", len(df))
with col2:
    st.metric("Collected", int(df[DEFAULT_COLLECTED_COL].sum()))
with col3:
    pct = 0 if len(df)==0 else int(100*df[DEFAULT_COLLECTED_COL].sum()/len(df))
    st.progress(pct/100)
    st.caption(f"{pct}% collected")

st.markdown("---")

# --- Data Table ---
st.subheader(f"Sheet: {sheet}")
MAX_ROWS_PER_PAGE = 500
page = st.number_input("Page", min_value=1, value=1, step=1)
start, end = (page-1)*MAX_ROWS_PER_PAGE, (page)*MAX_ROWS_PER_PAGE
page_df = filtered.iloc[start:end]

st.write(f"Rows {start+1}-{min(end, len(filtered))} / {len(filtered)}")
selected = st.multiselect("Select indices", list(page_df.index.astype(str)))

col_a, col_b = st.columns(2)
with col_a:
    if st.button("✅ Mark selected as Collected"):
        if selected:
            df.loc[selected, DEFAULT_COLLECTED_COL] = True
            st.success(f"Marked {len(selected)} rows.")
        else:
            st.warning("No rows selected.")
with col_b:
    if st.button("❌ Unmark selected"):
        if selected:
            df.loc[selected, DEFAULT_COLLECTED_COL] = False
            st.info(f"Unmarked {len(selected)} rows.")

st.dataframe(page_df)

# --- Export ---
st.markdown("---")
st.subheader("Save / Export")

if source_type == "path" and file_path_input:
    if st.button("💾 Save back to Excel file"):
        try:
            xls = pd.ExcelFile(file_path_input)
            with pd.ExcelWriter(file_path_input, engine="openpyxl") as writer:
                for s in xls.sheet_names:
                    if s == sheet:
                        df.to_excel(writer, sheet_name=s, index=False)
                    else:
                        pd.read_excel(file_path_input, sheet_name=s).to_excel(writer, sheet_name=s, index=False)
            st.success(f"Saved to {file_path_input}")
        except Exception as e:
            st.error(f"Save failed: {e}")

csv_bytes = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", data=csv_bytes, file_name=f"{sheet}_export.csv")

if source_type == "upload":
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet)
    st.download_button("📘 Download modified workbook", data=buffer.getvalue(), file_name=f"modified_{sheet}.xlsx")

st.caption("App by GPT-5 — Streamlit UI for GIS Excel data collection.")
