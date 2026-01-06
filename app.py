import streamlit as st
import pandas as pd
import sqlite3
import uuid

# Initialize database connection
conn = sqlite3.connect('todotask.db', check_same_thread=False)
cur = conn.cursor()

# Set page configuration for mobile-first
st.set_page_config(
    page_title="To Do List",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed",  # Hide sidebar on mobile
    menu_items=None  # Remove menu on mobile
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

# MOBILE-FIRST CSS (small screens < 768px are default)
st.markdown("""
<style>
/* ===== MOBILE FIRST (Default for < 768px) ===== */
/* Base container for entire app */
.main-container {
    max-width: 100%;
    margin: 0 auto;
    padding: 10px;
}

/* Header for mobile */
.mobile-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Task card for mobile */
.mobile-task-card {
    background: white;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid #e8e8e8;
}

/* Completed task styling */
.mobile-task-completed {
    background: #f8f9fa;
    border-left: 4px solid #4CAF50;
}

/* Task content layout for mobile */
.task-content-mobile {
    display: block;
    width: 100%;
}

/* Status indicator for mobile */
.status-mobile {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #f0f0f0;
    margin-right: 10px;
    vertical-align: middle;
}

.status-completed-mobile {
    background: #4CAF50;
    color: white;
}

/* Task text for mobile */
.task-text-mobile {
    font-size: 16px;
    color: #333;
    margin: 10px 0;
    line-height: 1.4;
    word-break: break-word;
}

.completed-text-mobile {
    color: #6c757d !important;
    text-decoration: line-through;
}

/* Action buttons for mobile (stacked vertically) */
.action-buttons-mobile {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 12px;
}

.action-buttons-mobile button {
    width: 100% !important;
    margin: 0 !important;
    padding: 10px !important;
    border-radius: 8px !important;
    font-size: 15px !important;
}

/* Form styling for mobile */
.mobile-form-container {
    background: white;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.mobile-form-input {
    width: 100%;
    margin-bottom: 10px;
}

.mobile-form-button {
    width: 100% !important;
    padding: 12px !important;
}

/* Progress bar for mobile */
.mobile-progress-container {
    background: white;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* Stats for mobile */
.stats-mobile {
    display: flex;
    justify-content: space-between;
    margin: 10px 0;
}

.stat-item-mobile {
    text-align: center;
    flex: 1;
}

.stat-value-mobile {
    font-size: 20px;
    font-weight: bold;
    color: #333;
}

.stat-label-mobile {
    font-size: 12px;
    color: #666;
}

/* Empty state for mobile */
.empty-state-mobile {
    background: white;
    border-radius: 10px;
    padding: 30px 20px;
    margin: 20px 0;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* ===== TABLET (768px - 1024px) ===== */
@media (min-width: 768px) {
    .main-container {
        max-width: 90%;
        padding: 20px;
    }
    
    .mobile-task-card {
        padding: 18px;
    }
    
    .action-buttons-mobile {
        flex-direction: row;
    }
    
    .action-buttons-mobile button {
        flex: 1;
    }
}

/* ===== DESKTOP (> 1024px) ===== */
@media (min-width: 1024px) {
    .main-container {
        max-width: 800px;
        padding: 30px 20px;
    }
    
    .mobile-header {
        padding: 20px;
        border-radius: 12px;
    }
    
    .mobile-task-card {
        padding: 20px;
        border-radius: 12px;
    }
    
    .action-buttons-mobile {
        flex-direction: row;
        justify-content: flex-end;
    }
    
    .action-buttons-mobile button {
        max-width: 150px;
    }
    
    /* Two-column layout for desktop */
    .desktop-columns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        align-items: start;
    }
}

/* Utility classes */
.hide-on-mobile {
    display: none;
}

.show-on-desktop {
    display: none;
}

@media (min-width: 768px) {
    .hide-on-mobile {
        display: block;
    }
    
    .show-on-desktop {
        display: flex;
    }
}

/* Make all Streamlit elements responsive */
[data-testid="stHorizontalBlock"] {
    gap: 10px !important;
}

.stButton > button {
    min-height: 44px !important; /* Minimum touch target size */
}

.stTextInput > div > div > input {
    font-size: 16px !important; /* Prevent iOS zoom */
    min-height: 44px !important;
}

/* Fix for mobile scrolling */
[data-testid="stAppViewContainer"] {
    overflow-x: hidden;
}
</style>
""", unsafe_allow_html=True)

# Main container starts here
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# MOBILE HEADER
st.markdown(f"""
<div class="mobile-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 22px; color: white;">✅ To Do List</h1>
            <p style="margin: 5px 0 0 0; font-size: 13px; opacity: 0.9; color: white;">
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

# PROGRESS SECTION (Mobile optimized)
if len(df) > 0:
    completed = df[df['status'] == '✅'].shape[0]
    total = len(df)
    progress_percent = (completed / total * 100) if total > 0 else 0
    
    st.markdown('<div class="mobile-progress-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top: 0;">📊 Progress</h3>', unsafe_allow_html=True)
    
    # Mobile stats
    st.markdown('<div class="stats-mobile">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="stat-item-mobile"><div class="stat-value-mobile">{total}</div><div class="stat-label-mobile">Total</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-item-mobile"><div class="stat-value-mobile">{completed}</div><div class="stat-label-mobile">Done</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-item-mobile"><div class="stat-value-mobile">{progress_percent:.0f}%</div><div class="stat-label-mobile">Progress</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress_percent / 100)
    st.markdown('</div>', unsafe_allow_html=True)

# TASKS SECTION (Mobile optimized layout)
if len(df) > 0:
    st.markdown('<h3 style="margin: 20px 0 15px 0;">📝 Your Tasks</h3>', unsafe_allow_html=True)
    
    for index, row in df.iterrows():
        is_completed = row['status'] == "✅"
        task_class = "mobile-task-card mobile-task-completed" if is_completed else "mobile-task-card"
        
        st.markdown(f'<div class="{task_class}">', unsafe_allow_html=True)
        
        # Status and task in a row for mobile
        col1, col2 = st.columns([1, 11])
        
        with col1:
            # Status indicator
            status_class = "status-mobile status-completed-mobile" if is_completed else "status-mobile"
            status_text = "✓" if is_completed else "○"
            st.markdown(f'<div class="{status_class}">{status_text}</div>', unsafe_allow_html=True)
        
        with col2:
            # Task text
            text_class = "task-text-mobile completed-text-mobile" if is_completed else "task-text-mobile"
            st.markdown(f'<div class="{text_class}">{row["task"]}</div>', unsafe_allow_html=True)
        
        # Action buttons (stacked vertically on mobile, horizontal on larger screens)
        st.markdown('<div class="action-buttons-mobile">', unsafe_allow_html=True)
        
        # Toggle status button
        if is_completed:
            if st.button("Mark as Incomplete", key=f"undo_{row['id']}", use_container_width=True):
                cur.execute(f'UPDATE "todotask_{tab}" SET status = "❌" WHERE id = ?;', (row['id'],))
                conn.commit()
                st.rerun()
        else:
            if st.button("Mark as Complete", key=f"done_{row['id']}", use_container_width=True):
                cur.execute(f'UPDATE "todotask_{tab}" SET status = "✅" WHERE id = ?;', (row['id'],))
                conn.commit()
                st.rerun()
        
        # Delete button
        if st.button("🗑️ Delete Task", key=f"delete_{row['id']}", use_container_width=True):
            cur.execute(f'DELETE FROM "todotask_{tab}" WHERE id = ?;', (row['id'],))
            conn.commit()
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # End action buttons
        st.markdown('</div>', unsafe_allow_html=True)  # End task card
else:
    # Empty state for mobile
    st.markdown("""
    <div class="empty-state-mobile">
        <div style="font-size: 48px; margin-bottom: 15px;">📝</div>
        <h3 style="color:#333; margin-bottom:10px;">No tasks yet!</h3>
        <p style="color:#666; margin:0;">Add your first task below to get started</p>
    </div>
    """, unsafe_allow_html=True)

# ADD TASK FORM (Mobile optimized)
st.markdown('<div class="mobile-form-container">', unsafe_allow_html=True)
st.markdown('<h3 style="margin-top: 0;">➕ Add New Task</h3>', unsafe_allow_html=True)

with st.form("add_task", clear_on_submit=True):
    # Input field (full width on mobile)
    task_input = st.text_input(
        "",
        placeholder="Enter your task here...",
        label_visibility="collapsed",
        key="task_input_mobile"
    )
    
    # Add button (full width on mobile)
    submitted = st.form_submit_button("Add Task", use_container_width=True, type="primary")
    
    if submitted and task_input.strip() != "":
        cur.execute(f'INSERT INTO "todotask_{tab}"(status, task) VALUES(?, ?);', ('❌', task_input.strip()))
        conn.commit()
        st.success("Task added! ✅")
        st.rerun()
    elif submitted and task_input.strip() == "":
        st.warning("Please enter a task description")

st.markdown('</div>', unsafe_allow_html=True)

# CLEAR ALL BUTTON (Mobile optimized)
if len(df) > 0:
    st.markdown("---")
    
    if 'show_clear_confirmation' not in st.session_state:
        st.session_state.show_clear_confirmation = False
    
    if not st.session_state.show_clear_confirmation:
        if st.button("🗑️ Clear All Tasks", use_container_width=True, type="secondary"):
            st.session_state.show_clear_confirmation = True
            st.rerun()
    else:
        st.warning("⚠️ Delete ALL tasks?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete", use_container_width=True, type="primary"):
                cur.execute(f'DELETE FROM "todotask_{tab}"')
                conn.commit()
                st.session_state.show_clear_confirmation = False
                st.success("All tasks cleared! ✨")
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_clear_confirmation = False
                st.rerun()

# DESKTOP-ONLY SIDEBAR (hidden on mobile)
with st.sidebar:
    if len(df) > 0:
        completed = df[df['status'] == '✅'].shape[0] if len(df) > 0 else 0
        total = len(df)
        progress_percent = (completed / total * 100) if total > 0 else 0
        
        st.metric("Overall Progress", f"{progress_percent:.0f}%")
        st.progress(progress_percent / 100)
        st.caption(f"{completed} of {total} tasks completed")

conn.close()

# Footer for mobile
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 15px; color: #666; font-size: 12px;">
    <div style="display: inline-flex; flex-wrap: wrap; gap: 10px; justify-content: center; align-items: center;">
        <span>✅ Tasks saved locally</span>
        <span style="color: #ccc;">•</span>
        <span>📱 Mobile optimized</span>
        <span style="color: #ccc;">•</span>
        <span>🔄 Refresh to sync</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End main container
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



























