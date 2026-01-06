import streamlit as st
import pandas as pd 
import sqlite3 
import uuid

conn = sqlite3.connect('todotask.db')
cur = conn.cursor()

# UUID that you decided for this device (from cookie / input / etc.)
# Example: using a fixed one for now; replace this with your own logic
if 'device_uuid' not in st.session_state:
    st.session_state['device_uuid'] = str(uuid.uuid4())

tab = st.session_state['device_uuid']

if tab != "":
            cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
            tables = cur.fetchall()
            st.write(tables)
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
                choice = st.checkbox(f"{i['task']}", value=False)
            elif i['status'] == "✅":
                choice = st.checkbox(f"{i['task']}", value=True)
            if choice:
                cur.execute(f'UPDATE "todotask{tab}" SET status = \'✅\' WHERE id = ?;', (i['id'],))
                conn.commit()
            elif not choice:
                cur.execute(f'UPDATE "todotask{tab}" SET status = \'❌\' WHERE id = ?;', (i['id'],))
                conn.commit()
        with b:
            if st.button("🗑️", key = f"{j}{i}key"):
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
    abc = st.text_input("Enter Task: ")
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











