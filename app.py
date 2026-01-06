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
    
    # Use a custom layout with session state for delete operations
    for index, row in df.iterrows():
        # Create a unique key for each task row
        task_key = f"task_{row['id']}"
        
        # Store task info in session state if not present
        if task_key not in st.session_state:
            st.session_state[task_key] = {
                'id': row['id'],
                'task': row['task'],
                'status': row['status'],
                'delete_clicked': False
            }
        
        # Check if delete was clicked
        if st.session_state[task_key]['delete_clicked']:
            cur.execute(f'DELETE FROM "todotask_{tab}" WHERE id = ?;', (row['id'],))
            conn.commit()
            del st.session_state[task_key]  # Remove from session state
            st.rerun()
        
        # Create the horizontal layout
        col1, col2, col3, col4 = st.columns([0.5, 8, 1, 0.5])
        
        with col1:
            # Display status indicator
            if row['status'] == "✅":
                st.write("✅")
            else:
                st.write("⬜")
        
        with col2:
            # Display task text
            if row['status'] == "✅":
                st.markdown(f"<span style='color: gray; text-decoration: line-through;'>{row['task']}</span>", 
                           unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='font-weight: bold;'>{row['task']}</span>", 
                           unsafe_allow_html=True)
        
        with col3:
            # Toggle status button
            if row['status'] == "✅":
                if st.button("Mark ❌", key=f"mark_undone_{row['id']}"):
                    cur.execute(f'UPDATE "todotask_{tab}" SET status = "❌" WHERE id = ?;', (row['id'],))
                    conn.commit()
                    st.rerun()
            else:
                if st.button("Mark ✅", key=f"mark_done_{row['id']}"):
                    cur.execute(f'UPDATE "todotask_{tab}" SET status = "✅" WHERE id = ?;', (row['id'],))
                    conn.commit()
                    st.rerun()
        
        with col4:
            # Delete button with confirmation
            if st.button("🗑️", key=f"delete_{row['id']}"):
                st.session_state[task_key]['delete_clicked'] = True
                st.rerun()
        
        # st.markdown("---")
else:
    st.info("No tasks yet! Add your first task below.")

# Add new task
st.write("---")
st.subheader("Add New Task")
with st.form("add_task", clear_on_submit=True):
    task_input = st.text_input("Enter your task:", placeholder="What needs to be done?")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        submitted = st.form_submit_button("➕ Add Task")
    
    if submitted and task_input.strip() != "":
        cur.execute(f'INSERT INTO "todotask_{tab}"(status, task) VALUES(?, ?);', ('❌', task_input.strip()))
        conn.commit()
        st.rerun()
    elif submitted and task_input.strip() == "":
        st.warning("Please enter a task!")

# Clear all button with confirmation
if len(df) > 0:
    st.subheader("Manage Tasks")
    
    # Initialize clear confirmation in session state
    if 'show_clear_confirmation' not in st.session_state:
        st.session_state.show_clear_confirmation = False
    
    if not st.session_state.show_clear_confirmation:
        if st.button("🗑️ Clear All Tasks", type="secondary"):
            st.session_state.show_clear_confirmation = True
            st.rerun()
    else:
        st.warning("Are you sure you want to delete ALL tasks? This cannot be undone!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete All"):
                cur.execute(f'DELETE FROM "todotask_{tab}"')
                conn.commit()
                st.session_state.show_clear_confirmation = False
                st.rerun()
        with col2:
            if st.button("❌ No, Cancel"):
                st.session_state.show_clear_confirmation = False
                st.rerun()

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























