import streamlit as st
import sqlite3
import uuid

# Setup
conn = sqlite3.connect('todo.db', check_same_thread=False)
cur = conn.cursor()

# User ID in session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

user = st.session_state.user_id

# Create table
cur.execute(f"""
    CREATE TABLE IF NOT EXISTS todo_{user} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        done INTEGER DEFAULT 0
    )
""")
conn.commit()

# CSS for one-line layout
st.markdown("""
<style>
.task-row {
    display: flex;
    align-items: center;
    background: white;
    border-radius: 8px;
    padding: 10px 15px;
    margin: 8px 0;
    border: 1px solid #e0e0e0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.task-status {
    width: 24px;
    text-align: center;
    font-size: 16px;
}

.task-text {
    flex: 1;
    padding: 0 10px;
    font-size: 16px;
}

.task-completed {
    text-decoration: line-through;
    color: #888;
}

.task-actions {
    display: flex;
    gap: 8px;
}

.action-btn {
    background: #4CAF50;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.delete-btn {
    background: #f44336;
}
</style>
""", unsafe_allow_html=True)

st.title("✅ To Do List")
st.caption(f"Your ID: {user}")

# Add task
with st.form("add_form"):
    new_task = st.text_input("Add new task:")
    if st.form_submit_button("Add Task") and new_task.strip():
        cur.execute(f"INSERT INTO todo_{user}(task) VALUES(?)", (new_task.strip(),))
        conn.commit()
        st.rerun()

# Handle actions via session state
if 'action_type' in st.session_state and 'task_id' in st.session_state:
    if st.session_state.action_type == 'toggle':
        cur.execute(f"UPDATE todo_{user} SET done = NOT done WHERE id=?", (st.session_state.task_id,))
    elif st.session_state.action_type == 'delete':
        cur.execute(f"DELETE FROM todo_{user} WHERE id=?", (st.session_state.task_id,))
    conn.commit()
    # Clear the action
    del st.session_state.action_type
    del st.session_state.task_id
    st.rerun()

# Display tasks
tasks = cur.execute(f"SELECT * FROM todo_{user} ORDER BY id DESC").fetchall()

if tasks:
    # Progress
    completed = sum(1 for _, _, done in tasks if done)
    total = len(tasks)
    if total > 0:
        st.progress(completed/total)
        st.write(f"**Progress:** {completed}/{total} completed")
    
    # Display each task
    for task_id, task_text, task_done in tasks:
        # Create HTML for one line
        status_icon = "✅" if task_done else "⬜"
        text_class = "task-text task-completed" if task_done else "task-text"
        toggle_text = "❌" if task_done else "✅"
        
        html = f"""
        <div class="task-row">
            <div class="task-status">{status_icon}</div>
            <div class="{text_class}">{task_text}</div>
            <div class="task-actions">
                <button class="action-btn" onclick="window.location.href='?action=toggle&id={task_id}'">{toggle_text}</button>
                <button class="action-btn delete-btn" onclick="window.location.href='?action=delete&id={task_id}'">🗑️</button>
            </div>
        </div>
        """
        
        st.markdown(html, unsafe_allow_html=True)
    
    # Handle URL parameters
    params = st.query_params
    if 'action' in params and 'id' in params:
        st.session_state.action_type = params['action']
        st.session_state.task_id = params['id']
        st.query_params.clear()
        st.rerun()
    
    # Clear all
    if st.button("Clear All Tasks"):
        cur.execute(f"DELETE FROM todo_{user}")
        conn.commit()
        st.rerun()
else:
    st.info("No tasks yet. Add one above!")

# Share
st.markdown("---")
st.write("**Share your list:**")
st.code(f"{st.get_option('server.baseUrlPath') or ''}?user={user}")

conn.close()

# Footer
st.markdown("---")
st.caption("🔒 Your tasks are stored locally and accessible only with your unique ID")

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




















































