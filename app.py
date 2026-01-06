# Add this once near the top of the file (after set_page_config)
import streamlit as st
import pandas as pd
import sqlite3
import uuid

# Initialize database connection
conn = sqlite3.connect('todotask.db', check_same_thread=False)
cur = conn.cursor()

# Set page configuration
st.set_page_config(
    page_title="To Do List",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
.task-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    padding: 6px 4px;
    border-bottom: 1px solid #eee;
    font-size: 15px;
}
.task-left {
    display: flex;
    align-items: center;
    gap: 8px;
    flex: 1;
    min-width: 0; /* allow text to shrink */
}
.task-status {
    flex-shrink: 0;
}
.task-text {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.task-text-done {
    color: gray;
    text-decoration: line-through;
}
.task-actions {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-shrink: 0;
}
.task-btn {
    padding: 2px 6px;
    border-radius: 4px;
    background-color: #f0f0f0;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)
# Generate or retrieve device UUID
if 'device_uuid' not in st.session_state:
    query_params = st.query_params
    if 'user_id' in query_params:
        st.session_state.device_uuid = query_params['user_id']
    else:
        st.session_state.device_uuid = str(uuid.uuid4())
        st.query_params['user_id'] = st.session_state.device_uuid

tab = st.session_state.device_uuid

# Simple CSS for mobile optimization
st.markdown("""
<style>
/* Mobile-first design */
.task-container {
    background: white;
    border-radius: 10px;
    padding: 12px;
    margin: 8px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border: 1px solid #e0e0e0;
}

.completed-task {
    background: #f8f9fa;
    opacity: 0.9;
}

.stButton > button {
    min-height: 36px;
    padding: 0 12px;
    font-size: 14px;
}

/* Ensure buttons don't wrap on mobile */
[data-testid="column"] {
    min-width: fit-content !important;
}

.task-row {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center;
    width: 100%;
    margin: 8px 0;
    padding: 8px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border: 1px solid #e0e0e0;
}

.task-row > div {
    flex-shrink: 0 !important;
}

@media (max-width: 768px) {
    .task-container {
        padding: 10px;
        margin: 6px 0;
    }
    
    .mobile-compact .stButton > button {
        min-width: 40px;
        padding: 0 8px;
        font-size: 12px;
    }
    
    /* Make task text compact on mobile */
    .task-text {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 150px; /* Adjusted for tighter mobile fit */
    }
    
    .task-row {
        padding: 6px;
        margin: 6px 0;
    }
}

/* Checkbox styling */
.checkbox-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.task-checkbox {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 2px solid #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
}

.checked {
    background: #4CAF50;
    border-color: #4CAF50;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 16px; border-radius: 10px; margin-bottom: 16px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 22px;">✅ To Do List</h1>
            <p style="margin: 5px 0 0 0; font-size: 13px; opacity: 0.9;">
                ID: {tab[:8]}...
            </p>
        </div>
        <button onclick="navigator.clipboard.writeText('{st.get_option('server.baseUrlPath') or ''}?user_id={tab}')" 
                style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); 
                       padding: 6px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;">
            📋 Share
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize table
cur.execute(
    f'CREATE TABLE IF NOT EXISTS "todotask_{tab}"('
    'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, '
    'status VARCHAR(2) NOT NULL, '
    'task VARCHAR(2000) NOT NULL, '
    'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'
)
conn.commit()

# Load tasks
def load_tasks():
    try:
        df = pd.read_sql(f'SELECT * FROM "todotask_{tab}" ORDER BY created_at DESC;', con=conn)
        return df
    except:
        return pd.DataFrame(columns=['id', 'status', 'task', 'created_at'])

df = load_tasks()

# PROGRESS SECTION
if len(df) > 0:
    completed = df[df['status'] == '✅'].shape[0]
    total = len(df)
    progress_percent = (completed / total * 100) if total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total", total)
    with col2:
        st.metric("Done", completed)
    with col3:
        st.metric("Progress", f"{progress_percent:.0f}%")
    
    st.progress(progress_percent / 100)

# TASKS SECTION - USING FLEX ROW FOR HORIZONTAL ALIGNMENT
if len(df) > 0:
    st.markdown("### 📝 Your Tasks")
    
    for index, row in df.iterrows():
        is_completed = row['status'] == "✅"
        
        # Use a flex row container for horizontal layout
        st.markdown('<div class="task-row">', unsafe_allow_html=True)
        
        # Create 4 columns inside the flex row
# BUTTON LOGIC (kept as real buttons so Python can run)
c1, c2, c3 = st.columns([1, 1, 1])

with c2:
    # DONE / Undo
    if row['status'] == "✅":
        if st.button("Undo", key=f"mark_undone_{row['id']}"):
            cur.execute(f'UPDATE "todotask_{tab}" SET status = "❌" WHERE id = ?;', (row['id'],))
            conn.commit()
            st.rerun()
    else:
        if st.button("DONE", key=f"mark_done_{row['id']}"):
            cur.execute(f'UPDATE "todotask_{tab}" SET status = "✅" WHERE id = ?;', (row['id'],))
            conn.commit()
            st.rerun()

with c3:
    if st.button("🗑️", key=f"delete_{row['id']}"):
        st.session_state[task_key]['delete_clicked'] = True
        st.rerun()

# VISUAL ROW (always one line on mobile)
status_icon = "✅" if row['status'] == "✅" else "⬜"
task_class = "task-text task-text-done" if row['status'] == "✅" else "task-text"

st.markdown(
    f"""
    <div class="task-row">
        <div class="task-left">
            <span class="task-status">{status_icon}</span>
            <span class="{task_class}">{row['task']}</span>
        </div>
        <div class="task-actions">
            <span class="task-btn">{'Undo' if row['status'] == '✅' else 'DONE'}</span>
            <span class="task-btn">🗑️</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("")  # tiny spacer

# import streamlit as st
# import pandas as pd
# import sqlite3
# import uuid

# # Initialize database connection
# conn = sqlite3.connect('todotask.db', check_same_thread=False)
# cur = conn.cursor()

# # Set page configuration
# st.set_page_config(page_title="To Do List", page_icon="✅", layout="wide")

# # Generate or retrieve device UUID from session state
# if 'device_uuid' not in st.session_state:
#     # Try to get from query params first (for sharing links)
#     query_params = st.query_params
#     if 'user_id' in query_params:
#         st.session_state.device_uuid = query_params['user_id']
#     else:
#         # Generate new UUID
#         st.session_state.device_uuid = str(uuid.uuid4())
#         # Store in query params for persistence
#         st.query_params['user_id'] = st.session_state.device_uuid

# tab = st.session_state.device_uuid

# # Title and user info
# st.title("✅ Personal To Do List")
# st.markdown(f"**Your ID:** `{tab[:8]}...`")

# # Sidebar for options
# with st.sidebar:
#     st.title("📊 Options")
    
#     # Share link functionality
#     st.subheader("Share Your List")
#     share_url = f"{st.get_option('server.baseUrlPath') or ''}?user_id={tab}"
    
#     if st.button("📋 Copy Share Link"):
#         st.code(share_url, language="text")
#         st.info("Share this URL with someone to let them view/edit your tasks")
    
#     st.markdown("---")
    
#     # Progress statistics
#     st.subheader("📈 Progress")

# # Initialize table for this user
# cur.execute(
#     f'CREATE TABLE IF NOT EXISTS "todotask_{tab}"('
#     'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, '
#     'status VARCHAR(2) NOT NULL, '
#     'task VARCHAR(2000) NOT NULL, '
#     'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'
# )
# conn.commit()

# # Main app functionality
# def load_tasks():
#     """Load tasks from database"""
#     try:
#         df = pd.read_sql(f'SELECT * FROM "todotask_{tab}" ORDER BY created_at DESC;', con=conn)
#         return df
#     except:
#         return pd.DataFrame(columns=['id', 'status', 'task', 'created_at'])

# # Display tasks
# df = load_tasks()
# st.markdown("---")

# if len(df) > 0:
#     # Task counters
#     completed = df[df['status'] == '✅'].shape[0]
#     total = len(df)
    
#     # Calculate progress percentage
#     progress_percent = (completed / total * 100) if total > 0 else 0
    
#     # Display progress in main area and sidebar
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Total Tasks", total)
#     with col2:
#         st.metric("Completed", completed)
#     with col3:
#         st.metric("Progress", f"{progress_percent:.1f}%")
    
#     # Progress bar
#     st.progress(progress_percent / 100)
    
#     st.subheader(f"Your Tasks")
    
#     # Use a custom layout with session state for delete operations
#     for index, row in df.iterrows():
#         # Create a unique key for each task row
#         task_key = f"task_{row['id']}"
        
#         # Store task info in session state if not present
#         if task_key not in st.session_state:
#             st.session_state[task_key] = {
#                 'id': row['id'],
#                 'task': row['task'],
#                 'status': row['status'],
#                 'delete_clicked': False
#             }
        
#         # Check if delete was clicked
#         if st.session_state[task_key]['delete_clicked']:
#             cur.execute(f'DELETE FROM "todotask_{tab}" WHERE id = ?;', (row['id'],))
#             conn.commit()
#             del st.session_state[task_key]  # Remove from session state
#             st.rerun()
        
#         # Create the horizontal layout - Checkbox, Task, Action Buttons
#         col1, col2, col3, col4 = st.columns([0.5, 4, 1, 0.5])
        
#         with col1:
#             # Display status indicator
#             if row['status'] == "✅":
#                 st.markdown("<div style='text-align: center;'>✅</div>", unsafe_allow_html=True)
#             else:
#                 st.markdown("<div style='text-align: center;'>⬜</div>", unsafe_allow_html=True)
        
#         with col2:
#             # Display task text
#             if row['status'] == "✅":
#                 st.markdown(f"<div style='color: gray; text-decoration: line-through; padding: 5px;'>{row['task']}</div>", 
#                            unsafe_allow_html=True)
#             else:
#                 st.markdown(f"<div style='font-weight: bold; padding: 5px;'>{row['task']}</div>", 
#                            unsafe_allow_html=True)
        
#         with col3:
#             # Toggle status button
#             if row['status'] == "✅":
#                 if st.button("Undo", key=f"mark_undone_{row['id']}", use_container_width=True):
#                     cur.execute(f'UPDATE "todotask_{tab}" SET status = "❌" WHERE id = ?;', (row['id'],))
#                     conn.commit()
#                     st.rerun()
#             else:
#                 if st.button("DONE", key=f"mark_done_{row['id']}", use_container_width=True):
#                     cur.execute(f'UPDATE "todotask_{tab}" SET status = "✅" WHERE id = ?;', (row['id'],))
#                     conn.commit()
#                     st.rerun()
        
#         with col4:
#             # Delete button with confirmation
#             if st.button("🗑️", key=f"delete_{row['id']}", use_container_width=True):
#                 st.session_state[task_key]['delete_clicked'] = True
#                 st.rerun()
        
#         st.markdown("---")
# else:
#     st.info("✨ No tasks yet! Add your first task below.")

# # Add new task section
# st.subheader("➕ Add New Task")
# with st.form("add_task", clear_on_submit=True):
#     task_input = st.text_input("Enter your task:", placeholder="What needs to be done?")
    
#     col1, col2 = st.columns([1, 4])
#     with col1:
#         submitted = st.form_submit_button("Add Task", use_container_width=True)
    
#     if submitted and task_input.strip() != "":
#         cur.execute(f'INSERT INTO "todotask_{tab}"(status, task) VALUES(?, ?);', ('❌', task_input.strip()))
#         conn.commit()
#         st.success("Task added successfully!")
#         st.rerun()
#     elif submitted and task_input.strip() == "":
#         st.warning("Please enter a task description!")

# # Clear all tasks button with confirmation
# if len(df) > 0:
#     st.markdown("---")
#     st.subheader("⚙️ Manage Tasks")
    
#     # Initialize clear confirmation in session state
#     if 'show_clear_confirmation' not in st.session_state:
#         st.session_state.show_clear_confirmation = False
    
#     if not st.session_state.show_clear_confirmation:
#         if st.button("🗑️ Clear All Tasks", type="secondary", use_container_width=True):
#             st.session_state.show_clear_confirmation = True
#             st.rerun()
#     else:
#         st.warning("⚠️ Are you sure you want to delete ALL tasks? This action cannot be undone!")
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("✅ Yes, Delete All", type="primary", use_container_width=True):
#                 cur.execute(f'DELETE FROM "todotask_{tab}"')
#                 conn.commit()
#                 st.session_state.show_clear_confirmation = False
#                 st.success("All tasks have been cleared!")
#                 st.rerun()
#         with col2:
#             if st.button("❌ No, Cancel", type="secondary", use_container_width=True):
#                 st.session_state.show_clear_confirmation = False
#                 st.rerun()

# # Update sidebar statistics after all operations
# with st.sidebar:
#     # Reload data for accurate stats
#     df_updated = load_tasks()
#     completed_updated = df_updated[df_updated['status'] == '✅'].shape[0] if len(df_updated) > 0 else 0
#     total_updated = len(df_updated)
    
#     if total_updated > 0:
#         progress_updated = (completed_updated / total_updated * 100)
        
#         # Progress circle visualization
#         st.markdown(f"""
#         <div style="text-align: center;">
#             <div style="font-size: 24px; font-weight: bold;">{progress_updated:.0f}%</div>
#             <div style="font-size: 14px; color: #666;">Complete</div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"**Completed:** {completed_updated}/{total_updated}")
        
#         # Mini progress bar
#         st.progress(progress_updated / 100)
        
#         # Stats
#         col_sb1, col_sb2 = st.columns(2)
#         with col_sb1:
#             st.metric("Total", total_updated)
#         with col_sb2:
#             st.metric("Done", completed_updated)
#     else:
#         st.info("No tasks yet")

# # Close database connection
# conn.close()

# # Footer
# st.markdown("---")
# st.caption("🔒 Your tasks are stored locally and accessible only with your unique ID")

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










































