import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

def get_connection():
    """Membuat koneksi ke database MySQL."""
    try:
        conn = mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_DATABASE"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"]  # Ganti dengan password MySQL Anda
        )
        return conn
    except Error as e:
        print(f"Error saat menyambungkan ke database: {e}")
        return None

def get_sqlalchemy_engine():
    user = 'tugasakh_winan'
    password = 'windandamendes'
    host = 'jade2.hidden-server.net'
    port = 2082
    database = 'tugasakh_login_app'


    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    return engine

def fetch_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM parfum_table")
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data)

# Fungsi menambahkan data ke database
def insert_data(varian_name, fragrant, formula, aquadest, alkohol, gender, jenis, ukuran, harga):
    conn = get_connection()
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
    cursor = conn.cursor()
    query = "DELETE FROM parfum_table WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()






