import pandas as pd

def standardise(raw, date_col, desc_col, debit_col, credit_col, spending_is_negative):
    """Parse Bank CSV transaction logs into fixed columns"""
    out = pd.DataFrame({
        "date": pd.to_datetime(raw[date_col], dayfirst = True).dt.strftime("%Y-%m-%d"),
        "description": raw[desc_col].astype(str),
        "amount": pd.to_numeric((raw[credit_col] - raw[debit_col]).astype(str).str.replace(",",""), errors="coerce")
    })
    if spending_is_negative:
        out["amount"] = -out["amount"]
    return out.dropna(subset=["amount"])