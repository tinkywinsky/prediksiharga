import mysql.connector
import streamlit as st

def create_connection():
    """Fungsi untuk membuat koneksi ke database MySQL."""
        return mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_DATABASE"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"]    # Ganti dengan nama database Anda
        )


