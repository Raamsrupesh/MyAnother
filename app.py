# import sqlite3 
# import streamlit as st 
# import pandas as pd 
# st.header("SQL query executor: ")
# DB_name = st.text_input("Enter the name of the database: ")
# if DB_name != "":
#     conn = sqlite3.connect(f"{DB_name}.db")
#     cur = conn.cursor()
#     with st.form(f"Executing query{DB_name}", clear_on_submit=True):
#         query = st.text_area("Execute your query here: ", placeholder=f"SELECT * FROM {DB_name};")
#         # one_many = st.selectbox(" Is the output of the query singular or plural: ", options=['ONE','MANY', 'NONE'], index=2)
#         try:
#             st.caption(f"You're doing operations on: {st.session_state['table_name']}")
#         except:
#             st.caption("You didn't create a table yet")
#         st.write("---")
#         if st.form_submit_button("EXECUTE", type='primary'):
#             if query != "":
#                 query = query.lower()
                
#                 if (('insert' in query) or ('update' in query) or ('delete' in query) or ('create' in query)):
#                     conn.commit()
#                     if 'create' in query:
#                         if 'table_name' not in st.session_state:
#                             st.session_state['table_name'] = query.split()[2].capitalize()
#                     st.success(f"Successfully {query.split()[0].capitalize()}ed")
#             else:
#                  st.warning("The query is empty!")
#     st.subheader("Output: ")
#     st.write(pd.read_sql_query(query, con=conn))
# else:
#      st.error("The name of the database is empty!!")

import sqlite3
import streamlit as st
import pandas as pd

st.header("SQL query executor:")

DB_name = st.text_input("Enter the name of the database:")

if DB_name != "":
    conn = sqlite3.connect(f"{DB_name}.db")
    cur = conn.cursor()

    with st.form(f"Executing query {DB_name}", clear_on_submit=True):
        query = st.text_area(
            "Execute your query here:",
            placeholder=f"SELECT name FROM sqlite_master WHERE type='table';"
        )

        try:
            st.caption(f"You're doing operations on: {st.session_state['table_name']}")
        except KeyError:
            st.caption("You didn't create a table yet")

        st.write("---")

        submitted = st.form_submit_button("EXECUTE", type="primary")

        if submitted:
            if query.strip() == "":
                st.warning("The query is empty!")
            else:
                try:
                    # Do NOT force lowercasing the whole query
                    first_word = query.strip().split()[0].upper()

                    # Execute query
                    cur.execute(query)

                    # If it is a write operation, commit
                    if first_word in ("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"):
                        conn.commit()
                        if first_word == "CREATE":
                            parts = query.strip().split()
                            # e.g. CREATE TABLE table_name (
                            if len(parts) >= 3 and parts[1].upper() == "TABLE":
                                st.session_state["table_name"] = parts[2]
                        st.success(f"Successfully executed {first_word} query.")
                    else:
                        st.success("Successfully executed query.")

                except Exception as e:
                    st.error(f"Error while executing query: {e}")

    st.subheader("Output:")

    # Only attempt to show output if last query exists and was SELECT-like
    if "query" in locals() and query.strip() != "":
        try:
            first_word = query.strip().split()[0].upper()
            if first_word in ("SELECT", "PRAGMA", "WITH"):
                df = pd.read_sql_query(query, con=conn)
                st.dataframe(df)
            else:
                st.caption("No tabular output for this query (non-SELECT).")
        except Exception as e:
            st.error(f"Error fetching output: {e}")
else:
    st.error("The name of the database is empty!!")
