import streamlit as st
import pandas as pd
import sqlite3
import uuid

# Initialize database connection
conn = sqlite3.connect('todotask.db', check_same_thread=False)
cur = conn.cursor()

# Set page configuration
st.set_page_config(page_title="To Do List", page_icon="✅", layout="wide")

# Generate or retrieve device UUID from session state
if 'device_uuid' not in st.session_state:
    # Try to get from query params first (for sharing links)
    query_params = st.query_params
    if 'user_id' in query_params:
        st.session_state.device_uuid = query_params['user_id']
    else:
        # Generate new UUID
        st.session_state.device_uuid = str(uuid.uuid4())
        # Store in query params for persistence
        st.query_params['user_id'] = st.session_state.device_uuid

tab = st.session_state.device_uuid

# Title and user info
st.title("✅ Personal To Do List")
st.markdown(f"**Your ID:** `{tab[:8]}...`")
st.markdown("---")

# Initialize table for this user
cur.execute(
    f'CREATE TABLE IF NOT EXISTS "todotask_{tab}"('
    'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, '
    'status VARCHAR(2) NOT NULL, '
    'task VARCHAR(2000) NOT NULL, '
    'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'
)
conn.commit()

# Share functionality
st.sidebar.title("Options")
if st.sidebar.button("Copy Shareable Link"):
    share_url = f"{st.get_option('server.baseUrlPath')}?user_id={tab}"
    st.sidebar.code(share_url)
    st.sidebar.info("Share this URL to access your tasks from any device")

# Main app functionality
def load_tasks():
    """Load tasks from database"""
    try:
        df = pd.read_sql(f'SELECT * FROM "todotask_{tab}" ORDER BY created_at DESC;', con=conn)
        return df
    except:
        return pd.DataFrame(columns=['id', 'status', 'task', 'created_at'])

# Display tasks
df = load_tasks()

if len(df) > 0:
    # Task counters
    completed = df[df['status'] == '✅'].shape[0]
    total = len(df)
    
    st.subheader(f"Tasks ({completed}/{total} completed)")
    
    # Display each task - FIXED: checkbox and task text side by side
# In the task display section, replace with:
for index, row in df.iterrows():
    col1, col2, col3 = st.columns([0.25, 8, 1])  # Adjust these numbers as needed
    
    with col1:
        new_status = st.checkbox("", value=(row['status'] == "✅"), key=f"cb_{row['id']}")
    
    with col2:
        task_display = f"~~{row['task']}~~" if row['status'] == "✅" else row['task']
        st.write(task_display)
    
    with col3:
        if st.button("🗑️", key=f"del_{row['id']}"):
            cur.execute(f'DELETE FROM "todotask_{tab}" WHERE id = ?;', (row['id'],))
            conn.commit()
            st.rerun()
    
    # Update status
    if new_status != (row['status'] == "✅"):
        status = "✅" if new_status else "❌"
        cur.execute(f'UPDATE "todotask_{tab}" SET status = ? WHERE id = ?;', (status, row['id']))
        conn.commit()
        st.rerun()
    
    st.markdown("---")
else:
    st.info("No tasks yet! Add your first task below.")

# Clear all button
if len(df) > 0:
    if st.button("Clear All Tasks", type="secondary"):
        if st.checkbox("Are you sure? This cannot be undone!"):
            cur.execute(f'DELETE FROM "todotask_{tab}"')
            conn.commit()
            st.success("All tasks cleared!")
            st.rerun()

# Add new task
st.subheader("Add New Task")
with st.form("add_task", clear_on_submit=True):
    task_input = st.text_input("Enter your task:", placeholder="What needs to be done?")
    col1, col2 = st.columns([1, 4])
    
    with col1:
        submitted = st.form_submit_button("➕ Add Task")
    
    if submitted and task_input.strip() != "":
        cur.execute(f'INSERT INTO "todotask_{tab}"(status, task) VALUES(?, ?);', ('❌', task_input.strip()))
        conn.commit()
        st.success("Task added!")
        st.rerun()
    elif submitted and task_input.strip() == "":
        st.warning("Please enter a task!")

# Statistics in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Statistics")
st.sidebar.metric("Total Tasks", total if 'total' in locals() else 0)
st.sidebar.metric("Completed", completed if 'completed' in locals() else 0)
if 'total' in locals() and total > 0:
    progress = (completed / total) * 100
    st.sidebar.progress(int(progress))
    st.sidebar.caption(f"{progress:.1f}% complete")

# Close database connection when done
conn.close()



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






















