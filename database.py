import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

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
















