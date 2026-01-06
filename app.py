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
    initial_sidebar_state="collapsed"  # Better for mobile
)

# Generate or retrieve device UUID from session state
if 'device_uuid' not in st.session_state:
    query_params = st.query_params
    if 'user_id' in query_params:
        st.session_state.device_uuid = query_params['user_id']
    else:
        st.session_state.device_uuid = str(uuid.uuid4())
        st.query_params['user_id'] = st.session_state.device_uuid

tab = st.session_state.device_uuid

# Apply responsive CSS
st.markdown("""
<style>
/* Mobile-first responsive design */
@media (max-width: 768px) {
    /* Stack columns vertically on mobile */
    .mobile-task-row {
        flex-direction: column !important;
        align-items: stretch !important;
    }
    
    .mobile-task-col {
        width: 100% !important;
        margin-bottom: 10px;
    }
    
    .mobile-button-group {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-top: 10px;
    }
    
    .mobile-button-group button {
        flex: 1;
    }
    
    /* Adjust header for mobile */
    .main-header {
        padding: 15px !important;
        margin: 10px 5px !important;
    }
    
    /* Adjust task container for mobile */
    .task-container {
        padding: 12px !important;
        margin: 10px 5px !important;
    }
    
    /* Sidebar adjustments */
    .sidebar .sidebar-content {
        padding: 10px !important;
    }
    
    /* Hide sidebar on mobile if not needed */
    [data-testid="stSidebar"] {
        min-width: 0 !important;
        max-width: none !important;
    }
}

/* Base styles */
.task-container {
    background: white;
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid #e8e8e8;
}

.task-completed {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    opacity: 0.9;
}

.mobile-task-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
}

.mobile-task-content {
    flex: 1;
    min-width: 200px;
    padding: 0 10px;
}

.mobile-task-text {
    font-size: 16px;
    color: #333;
    margin: 0;
    word-break: break-word;
}

.task-text-completed {
    color: #6c757d !important;
    text-decoration: line-through;
}

.mobile-task-actions {
    display: flex;
    gap: 8px;
    align-items: center;
}

.status-indicator {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    font-size: 12px;
}

.status-completed {
    background: #4CAF50;
    color: white;
}

/* Button styles */
.stButton > button {
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 14px;
    min-height: 36px;
}

/* Responsive form */
@media (max-width: 768px) {
    .mobile-form-row {
        flex-direction: column !important;
    }
    
    .mobile-form-row > div {
        width: 100% !important;
        margin-bottom: 10px !important;
    }
}

/* Progress bar responsive */
@media (max-width: 768px) {
    .progress-metrics {
        flex-direction: column !important;
        gap: 10px !important;
    }
    
    .progress-metrics > div {
        width: 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Title and user info
st.markdown(f"""
<div style="background: white; border-radius: 12px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);">
    <h1 style="margin:0; color:#333; display:flex; align-items:center; gap:10px;">
        ✅ Personal To Do List
    </h1>
    <p style="margin:5px 0 0 0; color:#666; font-size:14px;">
        ID: <code style="background:#f0f0f0; padding:2px 8px; border-radius:4px;">{tab[:8]}...</code>
        <span style="float:right;">
            <button onclick="navigator.clipboard.writeText(window.location.href)" style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; border:none; padding:4px 12px; border-radius:6px; font-size:12px; cursor:pointer;">
                📋 Copy Link
            </button>
        </span>
    </p>
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

# Progress section - Responsive layout
if len(df) > 0:
    completed = df[df['status'] == '✅'].shape[0]
    total = len(df)
    progress_percent = (completed / total * 100) if total > 0 else 0
    
    st.markdown("""
    <div style="background: white; border-radius: 12px; padding: 15px; margin: 15px 0; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);">
        <div style="display: flex; flex-wrap: wrap; gap: 15px; align-items: center;" class="progress-metrics">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 4])
    
    with col1:
        st.metric("Total", total)
    with col2:
        st.metric("Done", completed)
    with col3:
        st.metric("Progress", f"{progress_percent:.1f}%")
    with col4:
        st.progress(progress_percent / 100)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# Display tasks with mobile-responsive layout
if len(df) > 0:
    st.markdown("### 📝 Your Tasks")
    
    for index, row in df.iterrows():
        is_completed = row['status'] == "✅"
        container_class = "task-container task-completed" if is_completed else "task-container"
        
        st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
        
        # Mobile responsive row
        st.markdown('<div class="mobile-task-row">', unsafe_allow_html=True)
        
        # Status indicator (always visible)
        status_class = "status-indicator status-completed" if is_completed else "status-indicator"
        status_text = "✓" if is_completed else "○"
        
        # Create flexible layout
        col1, col2 = st.columns([1, 11])
        
        with col1:
            # Status indicator only - small and compact
            st.markdown(f'<div class="{status_class}" style="margin: auto;">{status_text}</div>', unsafe_allow_html=True)
        
        with col2:
            # Task text and buttons in a vertical stack for mobile
            st.markdown('<div style="width: 100%;">', unsafe_allow_html=True)
            
            # Task text (full width)
            task_class = "mobile-task-text task-text-completed" if is_completed else "mobile-task-text"
            st.markdown(f'<p class="{task_class}" style="margin-bottom: 10px;">{row["task"]}</p>', unsafe_allow_html=True)
            
            # Action buttons (horizontal on desktop, full width on mobile)
            st.markdown('<div class="mobile-button-group">', unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                # Toggle status button
                if is_completed:
                    if st.button("Mark ❌", key=f"undo_{row['id']}", use_container_width=True):
                        cur.execute(f'UPDATE "todotask_{tab}" SET status = "❌" WHERE id = ?;', (row['id'],))
                        conn.commit()
                        st.rerun()
                else:
                    if st.button("Mark ✅", key=f"done_{row['id']}", use_container_width=True):
                        cur.execute(f'UPDATE "todotask_{tab}" SET status = "✅" WHERE id = ?;', (row['id'],))
                        conn.commit()
                        st.rerun()
            
            with col_btn2:
                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{row['id']}", use_container_width=True):
                    cur.execute(f'DELETE FROM "todotask_{tab}" WHERE id = ?;', (row['id'],))
                    conn.commit()
                    st.rerun()
            
            with col_btn3:
                # Small space for better mobile layout
                st.write("")  # Empty for spacing
            
            st.markdown('</div>', unsafe_allow_html=True)  # End button group
            st.markdown('</div>', unsafe_allow_html=True)  # End task content
        
        st.markdown('</div>', unsafe_allow_html=True)  # End mobile-task-row
        st.markdown('</div>', unsafe_allow_html=True)  # End task-container
else:
    # Empty state
    st.markdown("""
    <div style="background: white; border-radius: 12px; padding: 40px; margin: 20px 0; text-align: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);">
        <h3 style="color:#666; margin-bottom:15px;">✨ No tasks yet!</h3>
        <p style="color:#888;">Add your first task below to get started</p>
    </div>
    """, unsafe_allow_html=True)

# Add new task form - Mobile responsive
st.markdown("""
<div style="background: white; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);">
    <h3 style="margin-top:0;">➕ Add New Task</h3>
""", unsafe_allow_html=True)

with st.form("add_task", clear_on_submit=True):
    # Responsive form layout
    st.markdown('<div class="mobile-form-row" style="display:flex; flex-wrap:wrap; gap:10px;">', unsafe_allow_html=True)
    
    # Input field (takes most space)
    task_input = st.text_input(
        "Task description:",
        placeholder="What needs to be done?",
        label_visibility="collapsed",
        key="task_input"
    )
    
    # Add button (compact)
    col1, col2 = st.columns([3, 1])
    with col2:
        submitted = st.form_submit_button("➕ Add", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted and task_input.strip() != "":
        cur.execute(f'INSERT INTO "todotask_{tab}"(status, task) VALUES(?, ?);', ('❌', task_input.strip()))
        conn.commit()
        st.success("✓ Task added!")
        st.rerun()
    elif submitted and task_input.strip() == "":
        st.warning("Please enter a task description!")

st.markdown('</div>', unsafe_allow_html=True)

# Clear all tasks button (mobile-friendly)
if len(df) > 0:
    st.markdown("---")
    
    if 'show_clear_confirmation' not in st.session_state:
        st.session_state.show_clear_confirmation = False
    
    if not st.session_state.show_clear_confirmation:
        if st.button("🗑️ Clear All Tasks", type="secondary", use_container_width=True):
            st.session_state.show_clear_confirmation = True
            st.rerun()
    else:
        st.warning("⚠️ Delete ALL tasks? This cannot be undone!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes", type="primary", use_container_width=True):
                cur.execute(f'DELETE FROM "todotask_{tab}"')
                conn.commit()
                st.session_state.show_clear_confirmation = False
                st.success("All tasks cleared!")
                st.rerun()
        with col2:
            if st.button("❌ No", type="secondary", use_container_width=True):
                st.session_state.show_clear_confirmation = False
                st.rerun()

# Mobile-friendly sidebar toggle
st.sidebar.title("📱 Mobile Menu")
with st.sidebar:
    st.markdown(f"**Your ID:** `{tab[:8]}...`")
    
    share_url = f"{st.get_option('server.baseUrlPath') or ''}?user_id={tab}"
    if st.button("📋 Copy Share Link", use_container_width=True):
        st.code(share_url, language="text")
    
    st.markdown("---")
    
    if len(df) > 0:
        completed = df[df['status'] == '✅'].shape[0]
        total = len(df)
        progress_percent = (completed / total * 100) if total > 0 else 0
        
        st.metric("Progress", f"{progress_percent:.0f}%")
        st.progress(progress_percent / 100)
        st.caption(f"{completed}/{total} tasks done")

conn.close()

# Footer with responsive text
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; padding: 20px 10px;">
    <div style="display: inline-block; background: #f8f9fa; padding: 8px 16px; border-radius: 8px;">
        🔒 Tasks stored locally • 📱 Mobile-friendly • 🔗 Share with link
    </div>
</div>
""", unsafe_allow_html=True)
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


























