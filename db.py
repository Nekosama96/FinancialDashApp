#This will be the backend of the app
import sqlite3
import pandas as pd

DB_PATH = "finance.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

#UNIQUE col will prevent dups
def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS transacations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL, 
            category TEXT NOT NULL,
            source TEXT,
            UNIQUE(date, description, amount)
        );
        CREATE TABLE IF NOT EXISTS rules (
            keyword TEXT PRIMARY KEY,
            category TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS budgets(
            category TEXT PRIMARY KEY,
            amount REAL NOT NULL
        );
        """)

def seed_rules(rules):
    with get_conn() as conn:
        conn.executemany("INSERT OR IGNORE INTO rules VALUES (?,?)", list(rules.items()))

def get_rules():
    with get_conn as conn:
        return dict(conn.execute("SELECT keyword, category FROM rules").fetchall())

def save_rule(keyword, category):
    with get_conn as conn:
        conn.execute("INSERT OR REPLACE INTO rules VALUES(?,?)", (keyword, category))

def add_transactions(df):
    cols = ["date","description","amount","category","source"]
    with get_conn as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO transactions (date, description, amount, category, source) ",
            "VALUES (?,?,?,?,?)",
            df[cols].values.tolist(),
        )

def load_transactions():
    with get_conn as conn:
        return pd.read_sql("SELECT * FROM transactions", conn, parse_dates=["date"])