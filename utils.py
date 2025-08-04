import mysql.connector
import streamlit as st

def create_connection():
    """Fungsi untuk membuat koneksi ke database MySQL menggunakan Streamlit Secrets."""
    try:
        connection = mysql.connector.connect(
            host=st.secrets["DB_HOST"],        # Host dari Streamlit Secrets
            database=st.secrets["DB_DATABASE"],  # Nama database dari Streamlit Secrets
            user=st.secrets["DB_USER"],             # Username dari Streamlit Secrets
            password=st.secrets["DB_PASSWORD"]   # Password dari Streamlit Secrets
        )
        return connection
    except Exception as e:
        st.error(f"Error saat membuat koneksi ke database: {e}")
        return None
