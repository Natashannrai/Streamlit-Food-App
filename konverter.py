import pandas as pd
import sqlite3

# Baca file CSV (ganti path sesuai file kamu)
df = pd.read_csv("global_street_food.csv")

# Buat file database SQLite (akan dibuat otomatis jika belum ada)
conn = sqlite3.connect("global_street_food.db")

# Masukkan data ke dalam tabel bernama 'foods'
df.to_sql("global_street_food", conn, if_exists="replace", index=False)

# Tutup koneksi
conn.close()

print("Dataset berhasil dimasukkan ke SQLite!")
