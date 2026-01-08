import sqlite3 
import streamlit as st 
import pandas as pd 
st.set_page_config(page_title="SQL Query Executor", layout="wide")
st.header("SQL query executor")
DB_name = st.text_input("Enter the name of the database: ")
if DB_name != "":
    conn = sqlite3.connect(f"{DB_name}.db")
    cur = conn.cursor()
    with st.form(f"Executing query{DB_name}", clear_on_submit=True):
        query = st.text_area("Execute your query here: ", placeholder=f"SELECT * FROM {DB_name};")

        if 'table_name' in st.session_state:
            st.caption(f"You're doing operations on: {st.session_state['table_name']}")
        else:
            st.caption("You didn't create a table yet!")

        st.write("---")
        if st.form_submit_button("EXECUTE", type='primary'):
            if query.strip() != "":
                try:
                    # query = query.lower()
                    cur.execute(query)
                    first_word = query.strip().split()[0].upper()
                    if first_word in ("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"):
                        conn.commit()
                        if first_word == "CREATE":
                                if len(query.strip().split()) >= 3 and query.strip().split()[1].upper() == "TABLE":
                                    st.session_state['table_name'] = query.strip().split()[2].capitalize()
                        st.success(f"Successfully {query.split()[0].capitalize()}ed table: {st.session_state.get('table_name', 'Unknown')}")
                    else:
                         st.success("Successfully executed the query!")
                except Exception as e:
                     st.error(f"Error while executing query: {e}")
            else:
                 st.warning("The query is empty!")

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

