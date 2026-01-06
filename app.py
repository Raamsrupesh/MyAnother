import streamlit as st
import pandas as pd 
import sqlite3 
conn = sqlite3.connect('todotask.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS todotask(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status VARCHAR(2) NOT NULL, task VARCHAR(2000) NOT NULL);")
conn.commit()
st.title("To do List: ")

st.write("---")

df = pd.read_sql("SELECT * FROM todotask;", con=conn)
try:
    for j,i in df.iterrows():
        a, b = st.columns([12,1])
        with a:
            if i['status'] == "❌":
                choice = st.checkbox(f"{i['task']}", value=False)
            elif i['status'] == "✅":
                choice = st.checkbox(f"{i['task']}", value=True)
            if choice:
                cur.execute("UPDATE todotask SET status = '✅' WHERE id = ?;", (i['id'],))
                conn.commit()
            elif not choice:
                cur.execute("UPDATE todotask SET status = '❌' WHERE id = ?;", (i['id'],))
                conn.commit()
        with b:
            if st.button("🗑️", key = f"{j}{i}key"):
                cur.execute("DELETE FROM todotask WHERE id = ?;", (i['id'],))
                conn.commit()
                st.rerun()
except st.errors.StreamlitDuplicateElementId:
    st.error("There are some duplicate elements.")
    
st.write("---")
with st.form(f"TASK", clear_on_submit=True):
    abc = st.text_input("Enter Task: ")
    if st.form_submit_button("ADD"):
        if abc != "":
            cur.execute(f"INSERT INTO todotask(status, task) VALUES(?, ?);", ('❌',abc))
            conn.commit()



