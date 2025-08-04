import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

def get_connection():
    """Membuat koneksi ke database MySQL menggunakan Streamlit Secrets."""
    try:
        conn = mysql.connector.connect(
            user = st.secrets["DB_USER"]
            password = st.secrets["DB_PASSWORD"]
        host = st.secrets["DB_HOST"]
        port = 3306  # Port default untuk MySQL
        database = st.secrets["DB_DATABASE"] # Password dari Streamlit Secrets
        )
        if conn.is_connected():
            print("Koneksi berhasil ke database.")
        return conn
    except Error as e:
        print(f"Error saat menyambungkan ke database: {e}")
        return None

def get_sqlalchemy_engine():
    """Membuat engine SQLAlchemy untuk koneksi ke database."""
    user = st.secrets["DB_USER"]
    password = st.secrets["DB_PASSWORD"]
    host = st.secrets["DB_HOST"]
    port = 3306  # Port default untuk MySQL
    database = st.secrets["DB_DATABASE"]

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    return engine

def fetch_data():
    """Mengambil data dari tabel parfum_table."""
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM parfum_table")
        data = cursor.fetchall()
        conn.close()
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()

# Fungsi menambahkan data ke database
def insert_data(varian_name, fragrant, formula, aquadest, alkohol, gender, jenis, ukuran, harga):
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        query = """
            INSERT INTO parfum_table (VARIAN_NAME, FRAGRANT, FORMULA, AQUADEST, ALKOHOL, GENDER, JENIS, UKURAN, HARGA)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (varian_name, fragrant, formula, aquadest, alkohol, gender, jenis, ukuran, harga)
        cursor.execute(query, values)
        conn.commit()
        conn.close()

# Fungsi memperbarui data di database
def update_data(id, varian_name, fragrant, formula, aquadest, alkohol, gender, jenis, ukuran, harga):
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        query = """
            UPDATE parfum_table
            SET VARIAN_NAME = %s, FRAGRANT = %s, FORMULA = %s, AQUADEST = %s, ALKOHOL = %s, GENDER = %s, JENIS = %s, UKURAN = %s, HARGA = %s
            WHERE id = %s
        """
        values = (varian_name, fragrant, formula, aquadest, alkohol, gender, jenis, ukuran, harga, id)
        cursor.execute(query, values)
        conn.commit()
        conn.close()

# Fungsi menghapus data dari database
def delete_data(id):
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        query = "DELETE FROM parfum_table WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        conn.close()




