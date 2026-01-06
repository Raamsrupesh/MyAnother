import streamlit as st
import pandas as pd 
import sqlite3 
import uuid

conn = sqlite3.connect('todotask.db')
cur = conn.cursor()
import streamlit as st
import pandas as pd

glass_css = """
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.todo-wrapper {
    max-width: 500px;
    margin: 40px auto;
    padding: 24px 28px;
    border-radius: 24px;
    background: rgba(15, 23, 42, 0.45);
    box-shadow: 0 20px 60px rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.4);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    color: #e5e7eb;
}
.todo-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
}
.todo-title {
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.todo-pill {
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.7);
    color: #7dd3fc;
}
.todo-list {
    list-style: none;
    padding: 0;
    margin: 0;
}
.todo-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 12px;
    margin-bottom: 8px;
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(30, 64, 175, 0.6);
}
.todo-left {
    display: flex;
    align-items: center;
    gap: 10px;
}
.todo-checkbox {
    width: 18px;
    height: 18px;
    border-radius: 6px;
    border: 1px solid rgba(148, 163, 184, 0.8);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: #22c55e;
}
.todo-text {
    font-size: 14px;
}
.todo-text.done {
    text-decoration: line-through;
    color: #6b7280;
}
.todo-badge {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 999px;
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.4);
    color: #bae6fd;
}
</style>
"""
st.markdown(glass_css, unsafe_allow_html=True)

# UUID that you decided for this device (from cookie / input / etc.)
# Example: using a fixed one for now; replace this with your own logic
if 'device_uuid' not in st.session_state:
    st.session_state['device_uuid'] = str(uuid.uuid4())

tab = st.session_state['device_uuid']

if tab != "":
            cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
            tables = cur.fetchall()
            # st.write(tables)
            cur.execute(f'CREATE TABLE IF NOT EXISTS "todotask{tab}"(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status VARCHAR(2) NOT NULL, task VARCHAR(2000) NOT NULL);')
            conn.commit()
else:
            st.warning("It's EMPTY!")

st.title("To do List/ Groceries list: ")
st.write("---")

df = pd.read_sql(f'SELECT * FROM "todotask{tab}";', con=conn)
try:
    for j,i in df.iterrows():
        a, b = st.columns([12,1])
        with a:
            if i['status'] == "❌":
                choice = st.checkbox(f"{i['task']}", value=False, key = f"cb_{i['id']}")
            elif i['status'] == "✅":
                choice = st.checkbox(f"{i['task']}", value=True, key = f"cb_{i['id']}")
            if choice:
                cur.execute(f'UPDATE "todotask{tab}" SET status = \'✅\' WHERE id = ?;', (i['id'],))
                conn.commit()
            elif not choice:
                cur.execute(f'UPDATE "todotask{tab}" SET status = \'❌\' WHERE id = ?;', (i['id'],))
                conn.commit()
        with b:
            if st.button("🗑️", key = f"{j}{i}keytodotask{tab}{str(uuid.uuid1())}"):
                cur.execute(f'DELETE FROM "todotask{tab}" WHERE id = ?;', (i['id'],))
                conn.commit()
                st.rerun()
        if st.button("Clear ALL"):
            cur.execute(f'DELETE FROM "todotask{tab}"')
            conn.commit()
            st.rerun()
except st.errors.StreamlitDuplicateElementId:
    st.error("There are some duplicate elements.")
    
st.write("---")
with st.form(f"TASK", clear_on_submit=True):
    abc = st.text_input("Enter Task/item: ")
    if st.form_submit_button("ADD"):
        if abc != "":
            cur.execute(f'INSERT INTO "todotask{tab}"(status, task) VALUES(?, ?);', ('❌',abc))
            conn.commit()
            st.rerun()

# import streamlit as st
# import pandas as pd 
# import sqlite3 
# # import uuid
# conn = sqlite3.connect('todotask.db')
# cur = conn.cursor()
# tab = st.text_input("Enter the table name: ")
# if st.button("GO"):
#     if tab != "":
#         cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
#         tables = cur.fetchall()
#         st.write(tables)
#         cur.execute(f"CREATE TABLE IF NOT EXISTS todotask{tab}(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status VARCHAR(2) NOT NULL, task VARCHAR(2000) NOT NULL);")
#         conn.commit()
#     else:
#         st.warning("It's EMPTY!")
# st.title("To do List: ")
# st.write("---")

# df = pd.read_sql(f"SELECT * FROM todotask{tab};", con=conn)
# try:
#     for j,i in df.iterrows():
#         a, b = st.columns([12,1])
#         with a:
#             if i['status'] == "❌":
#                 choice = st.checkbox(f"{i['task']}", value=False)
#             elif i['status'] == "✅":
#                 choice = st.checkbox(f"{i['task']}", value=True)
#             if choice:
#                 cur.execute(f"UPDATE todotask{tab} SET status = '✅' WHERE id = ?;", (i['id'],))
#                 conn.commit()
#             elif not choice:
#                 cur.execute(f"UPDATE todotask{tab} SET status = '❌' WHERE id = ?;", (i['id'],))
#                 conn.commit()
#         with b:
#             if st.button("🗑️", key = f"{j}{i}key"):
#                 cur.execute(f"DELETE FROM todotask{tab} WHERE id = ?;", (i['id'],))
#                 conn.commit()
#                 st.rerun()
#         if st.button("Clear ALL"):
#             cur.execute(f"DELETE FROM todotask{tab}")
#             conn.commit()
#             st.rerun()
# except st.errors.StreamlitDuplicateElementId:
#     st.error("There are some duplicate elements.")
    
# st.write("---")
# with st.form(f"TASK", clear_on_submit=True):
#     abc = st.text_input("Enter Task: ")
#     if st.form_submit_button("ADD"):
#         if abc != "":
#             cur.execute(f"INSERT INTO todotask{tab}(status, task) VALUES(?, ?);", ('❌',abc))
#             conn.commit()



















