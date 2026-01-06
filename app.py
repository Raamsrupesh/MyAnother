import streamlit as st
import pandas as pd
import sqlite3
import uuid

# Initialize database connection
conn = sqlite3.connect('todotask.db', check_same_thread=False)
cur = conn.cursor()

# Set page configuration for mobile
st.set_page_config(
    page_title="To Do List",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Generate or retrieve device UUID
if 'device_uuid' not in st.session_state:
    query_params = st.query_params
    if 'user_id' in query_params:
        st.session_state.device_uuid = query_params['user_id']
    else:
        st.session_state.device_uuid = str(uuid.uuid4())
        st.query_params['user_id'] = st.session_state.device_uuid

tab = st.session_state.device_uuid

# MOBILE-FIRST CSS with horizontal layout
st.markdown("""
<style>
/* ===== MOBILE FIRST ===== */
/* Base styles */
* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 0;
    padding: 0;
}

/* Main container */
.main-wrapper {
    width: 100%;
    max-width: 100%;
    padding: 10px;
    margin: 0 auto;
}

/* Header */
.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Task card - HORIZONTAL LAYOUT */
.task-row {
    display: flex;
    align-items: center;
    background: white;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid #e8e8e8;
    gap: 8px;
    flex-wrap: nowrap;
    min-height: 60px;
}

.task-row.completed {
    background: #f8f9fa;
    border-left: 4px solid #4CAF50;
}

/* Checkbox container */
.checkbox-container {
    flex: 0 0 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Checkbox styling */
.task-checkbox {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 2px solid #ddd;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
}

.task-checkbox.checked {
    background: #4CAF50;
    border-color: #4CAF50;
}

.task-checkbox.checked::after {
    content: "✓";
    color: white;
    font-size: 14px;
    font-weight: bold;
}

/* Task text - takes available space */
.task-content {
    flex: 1;
    min-width: 0; /* Important for text truncation */
    padding: 0 8px;
}

.task-text {
    font-size: 16px;
    color: #333;
    margin: 0;
    line-height: 1.4;
    word-break: break-word;
}

.task-text.completed {
    color: #6c757d;
    text-decoration: line-through;
}

/* Action buttons - fixed width */
.action-buttons {
    flex: 0 0 auto;
    display: flex;
    gap: 6px;
    align-items: center;
}

/* Small buttons for mobile */
.action-btn {
    min-width: 40px !important;
    height: 36px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 8px !important;
    font-size: 12px !important;
}

.mark-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
}

.delete-btn {
    background: #ff4444 !important;
    color: white !important;
    border: none !important;
}

/* Progress section */
.progress-section {
    background: white;
    border-radius: 12px;
    padding: 16px;
    margin: 16px 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.stats-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
}

.stat-box {
    flex: 1;
    text-align: center;
    padding: 8px;
}

.stat-value {
    font-size: 20px;
    font-weight: bold;
    color: #333;
    display: block;
}

.stat-label {
    font-size: 11px;
    color: #666;
    display: block;
    margin-top: 4px;
}

/* Add task form */
.add-form {
    background: white;
    border-radius: 12px;
    padding: 16px;
    margin: 16px 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.form-row {
    display: flex;
    gap: 8px;
    align-items: center;
}

.task-input {
    flex: 1;
    min-width: 0;
}

.add-btn {
    flex: 0 0 60px;
    height: 44px !important;
}

/* Empty state */
.empty-state {
    background: white;
    border-radius: 12px;
    padding: 40px 20px;
    margin: 20px 0;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* Clear button */
.clear-section {
    text-align: center;
    margin: 20px 0;
}

/* ===== TABLET ===== */
@media (min-width: 768px) {
    .main-wrapper {
        max-width: 90%;
        padding: 20px;
    }
    
    .task-row {
        padding: 15px;
        gap: 12px;
    }
    
    .action-btn {
        min-width: 50px !important;
        height: 40px !important;
        font-size: 14px !important;
    }
}

/* ===== DESKTOP ===== */
@media (min-width: 1024px) {
    .main-wrapper {
        max-width: 800px;
        padding: 30px 20px;
    }
    
    .task-row {
        padding: 18px;
    }
    
    .action-buttons {
        gap: 10px;
    }
    
    .action-btn {
        min-width: 60px !important;
        height: 44px !important;
    }
}

/* Streamlit overrides */
.stButton > button {
    margin: 0 !important;
}

.stTextInput > div > div > input {
    font-size: 16px !important;
    height: 44px !important;
    border-radius: 8px !important;
}

/* Hide scrollbar but keep functionality */
::-webkit-scrollbar {
    display: none;
}

/* Force horizontal layout even on smallest screens */
@media (max-width: 320px) {
    .task-row {
        flex-wrap: nowrap !important;
        overflow-x: auto;
        padding: 10px;
    }
    
    .task-content {
        min-width: 120px;
    }
    
    .action-buttons {
        flex-shrink: 0;
    }
    
    .action-btn {
        min-width: 35px !important;
        height: 32px !important;
        font-size: 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Start main wrapper
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# HEADER
st.markdown(f"""
<div class="app-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 22px; display: flex; align-items: center; gap: 8px;">
                <span>✅</span>
                <span>To Do List</span>
            </h1>
            <p style="margin: 5px 0 0 0; font-size: 13px; opacity: 0.9;">
                ID: {tab[:8]}...
            </p>
        </div>
        <button onclick="navigator.clipboard.writeText('{st.get_option('server.baseUrlPath') or ''}?user_id={tab}')" 
                style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); 
                       padding: 6px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;">
            📋 Copy Link
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
    
    st.markdown('<div class="progress-section">', unsafe_allow_html=True)
    
    # Stats in horizontal row
    st.markdown('<div class="stats-row">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="stat-box"><span class="stat-value">{total}</span><span class="stat-label">Total Tasks</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><span class="stat-value">{completed}</span><span class="stat-label">Completed</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-box"><span class="stat-value">{progress_percent:.0f}%</span><span class="stat-label">Progress</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress_percent / 100)
    st.markdown('</div>', unsafe_allow_html=True)

# TASKS SECTION - HORIZONTAL LAYOUT
if len(df) > 0:
    st.markdown('<h3 style="margin: 20px 0 15px 0;">📝 Your Tasks</h3>', unsafe_allow_html=True)
    
    for index, row in df.iterrows():
        is_completed = row['status'] == "✅"
        
        # Create the horizontal row using HTML/CSS
        st.markdown(f'''
        <div class="task-row {'completed' if is_completed else ''}">
            <!-- Checkbox -->
            <div class="checkbox-container">
                <div class="task-checkbox {'checked' if is_completed else ''}"></div>
            </div>
            
            <!-- Task Text -->
            <div class="task-content">
                <p class="task-text {'completed' if is_completed else ''}">{row["task"]}</p>
            </div>
            
            <!-- Action Buttons -->
            <div class="action-buttons">
        ''', unsafe_allow_html=True)
        
        # Now create Streamlit buttons that will be styled by CSS
        col1, col2 = st.columns(2)
        
        with col1:
            # Toggle status button
            if is_completed:
                if st.button("❌", key=f"undo_{row['id']}", help="Mark incomplete"):
                    cur.execute(f'UPDATE "todotask_{tab}" SET status = "❌" WHERE id = ?;', (row['id'],))
                    conn.commit()
                    st.rerun()
            else:
                if st.button("✅", key=f"done_{row['id']}", help="Mark complete"):
                    cur.execute(f'UPDATE "todotask_{tab}" SET status = "✅" WHERE id = ?;', (row['id'],))
                    conn.commit()
                    st.rerun()
        
        with col2:
            # Delete button
            if st.button("🗑️", key=f"delete_{row['id']}", help="Delete task"):
                cur.execute(f'DELETE FROM "todotask_{tab}" WHERE id = ?;', (row['id'],))
                conn.commit()
                st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)
else:
    # Empty state
    st.markdown("""
    <div class="empty-state">
        <div style="font-size: 48px; margin-bottom: 15px;">📝</div>
        <h3 style="color:#333; margin-bottom:10px;">No tasks yet!</h3>
        <p style="color:#666; margin:0;">Add your first task below</p>
    </div>
    """, unsafe_allow_html=True)

# ADD TASK FORM
st.markdown('<div class="add-form">', unsafe_allow_html=True)
st.markdown('<h3 style="margin-top: 0;">➕ Add New Task</h3>', unsafe_allow_html=True)

with st.form("add_task", clear_on_submit=True):
    # Horizontal form layout
    st.markdown('<div class="form-row">', unsafe_allow_html=True)
    
    # Input field
    task_input = st.text_input(
        "",
        placeholder="Enter task...",
        label_visibility="collapsed",
        key="task_input"
    )
    
    # Add button
    submitted = st.form_submit_button("Add", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted and task_input.strip() != "":
        cur.execute(f'INSERT INTO "todotask_{tab}"(status, task) VALUES(?, ?);', ('❌', task_input.strip()))
        conn.commit()
        st.success("Added!")
        st.rerun()
    elif submitted and task_input.strip() == "":
        st.warning("Enter a task")

st.markdown('</div>', unsafe_allow_html=True)

# CLEAR ALL BUTTON
if len(df) > 0:
    st.markdown('<div class="clear-section">', unsafe_allow_html=True)
    
    if 'show_clear_confirmation' not in st.session_state:
        st.session_state.show_clear_confirmation = False
    
    if not st.session_state.show_clear_confirmation:
        if st.button("🗑️ Clear All Tasks", use_container_width=True, type="secondary"):
            st.session_state.show_clear_confirmation = True
            st.rerun()
    else:
        st.warning("Delete ALL tasks?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes", use_container_width=True):
                cur.execute(f'DELETE FROM "todotask_{tab}"')
                conn.commit()
                st.session_state.show_clear_confirmation = False
                st.rerun()
        with col2:
            if st.button("❌ No", use_container_width=True):
                st.session_state.show_clear_confirmation = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

conn.close()

# FOOTER
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 15px; color: #666; font-size: 12px;">
    <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
        <span>✅ Auto-save</span>
        <span>📱 Mobile-friendly</span>
        <span>🔗 Shareable</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End main wrapper
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




























