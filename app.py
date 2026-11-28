# Installed Streamlit, pandas and pdfplumber - pip install
# streamlit is for the front end
# pandas is for dataframes - reading csv
# pdfplumber is to read uploaded PDF files

import streamlit as st
import pandas as pd
import db, parsers
from categorise import DEFAULT_RULES, categorise, keyword_from

st.set_page_config(page_title="Personal Cashflow", layout = "wide")
db.init_db()
db.seed_rules(DEFAULT_RULES)

CATEGORIES = ["Driving","Family","Food","Health","Income","Insurance","Interest","Investments","Leisure",
              "Muay Thai","Savings","Shopping","Studies","Fitness","Subscriptions","Transport","Travel","HDB"]
NOT_SPENDING = ["Savings", "Income", "Investments", "Interest"]

page = st.sidebar.radio("Go to", ["Import", "Dashboard"])

if page == "Import":
    st.header("Import transactions")
    file = st.file_uploader("Upload a bank CSV file", type = "csv")
    if file:
        file.seek(0)
        raw = pd.read_csv(file)
        cols = list(raw.columns)
        c1,c2,c3 = st.columns(3)
        date_col = c1.selectbox("Transaction Date", cols)
        desc_col = c2. selectbox("Description", cols)
        amt_col = c3.selectbox("Credit Amount", cols)
        neg = st.checkbox("Row item has more debit than credit", value = True)

    df = parsers.standardise(raw, date_col, desc_col, amt_col, neg)
    rules = db.get_rules()
    df["category"] = [
        "Income" if a < 0 else categorise(d,rules)
        for d,a in zip(df["description"], df["amount"])
    ]
    df["source"] = file.name
    original = df["category"].copy()
    #REVISIT FROM HERE
    st.caption("Fix any wrong categories below, then save. Fixes will be persisted.")
    edited = st.data_editor(
        df,
        column_config={"category": st.column_config.SelectboxColumn(options = CATEGORIES)}
    )
    if st.button("Save to history"):
        for _, row in edited[edited["category"] != original].iterrows():
            kw = keyword_from(row["description"])
            if kw:
                db.save_rule(kw, row["category"])
            db.add_transactions(edited)
            st.success(f"Saved {len(edited)} transactions.")

else: 
    st.header("Dashboard")
    tx = db.load_transactions()
    if tx.empty:
        st.info("No data yet. Import something first.")
    else:
        spend = tx[~tx["category"].isin(NOT_SPENDING)].copy()
        spend["month"] = spend["date"].dt.to_period("M").astype(str)
        pivot = spend.pivot_table(index = "category", columns = "month", 
                                  values = "amount", aggfunc="sum", fill_value=0)
        st.subheader("Spending by category and month")
        st.dataframe(pivot.round(0))
        st.bar_chart(pivot.T)

