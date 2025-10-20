import streamlit as st
import requests
import pandas as pd

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:8000/api/v1"
st.set_page_config(page_title="QueryCraft", page_icon="🤖", layout="wide")

# --- Page Title and Description ---
st.title("🤖 QueryCraft: Text-to-SQL")
st.markdown("Ask a question about the music database in plain English, and the AI will get the answer for you.")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Display different content based on what's in the message
        if "sql" in message:
            with st.expander("Generated SQL Query"):
                st.code(message["sql"], language="sql")
        if "data" in message:
            st.dataframe(message["data"])
        if "error" in message:
            st.error(message["error"])
        if "content" in message:
            st.markdown(message["content"])

# --- Handle New User Input ---
if prompt := st.chat_input("Ask a question about the database (e.g., 'Show me all artists from Brazil')"):
    
    # 1. Add user's message to chat and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Send request to API and get response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            response = requests.post(f"{API_BASE_URL}/query", json={"text": prompt})
            response.raise_for_status()  # Raise an error for bad status codes
            
            data = response.json()
            bot_message = {}

            if data.get("error"):
                # Handle API-level or SQL errors
                bot_message = {"role": "assistant", "error": data["error"]}
                if data.get("sql_query"):
                    bot_message["sql"] = data["sql_query"]
                message_placeholder.error(data["error"])

            else:
                # Handle successful query
                sql = data.get("sql_query")
                df = pd.DataFrame(data.get("data", []))
                
                bot_message = {"role": "assistant", "sql": sql, "data": df}
                
                # Display the results
                message_placeholder.empty() # Clear "Thinking..."
                with st.expander("Generated SQL Query"):
                    st.code(sql, language="sql")
                
                st.dataframe(df)
                
                # Try to plot a simple chart if data is appropriate
                if not df.empty and len(df.columns) == 2:
                    try:
                        # Check if we can make a bar chart
                        if pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
                            st.bar_chart(df.set_index(df.columns[0]))
                    except Exception:
                        pass # Fail silently if chart can't be made

            st.session_state.messages.append(bot_message)

        except requests.exceptions.RequestException as e:
            # Handle connection errors
            error_msg = f"Failed to connect to backend API: {e}"
            st.session_state.messages.append({"role": "assistant", "error": error_msg})
            message_placeholder.error(error_msg)
