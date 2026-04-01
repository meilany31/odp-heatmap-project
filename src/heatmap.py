print("🚀 SCRIPT JALAN")

import pandas as pd
import folium
from folium.plugins import HeatMap

# =============================
# LOAD DATA
# =============================
file_path = "../data/odp_avail_demo.txt"

# ❗ PENTING: pakai sep='|'
df = pd.read_csv(file_path, sep='|')

# =============================
# BERSIHKAN KOLOM
# =============================
df.columns = df.columns.str.strip()

print("Kolom:", df.columns)
print(df.head())

# =============================
# HAPUS BARIS HEADER ANEH
# =============================
df = df[df['latitude'].str.contains('-') == False]

# =============================
# KONVERSI KE NUMERIC
# =============================
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df['port_used'] = pd.to_numeric(df['port_used'], errors='coerce')

# =============================
# HAPUS DATA KOSONG
# =============================
df = df.dropna(subset=['latitude', 'longitude', 'port_used'])

print("Jumlah data bersih:", len(df))

# =============================
# HITUNG PERSENTASE
# =============================
total = df['port_used'].sum()
df['persentase'] = (df['port_used'] / total) * 100

# =============================
# BUAT PETA
# =============================
m = folium.Map(
    location=[df['latitude'].mean(), df['longitude'].mean()],
    zoom_start=13
)

# =============================
# DATA HEATMAP
# =============================
heat_data = [
    [row['latitude'], row['longitude'], row['persentase']]
    for _, row in df.iterrows()
]

HeatMap(
    heat_data,
    radius=15,
    blur=10
).add_to(m)

# =============================
# SIMPAN
# =============================
output_file = "../output/heatmap_persentase.html"
m.save(output_file)

print("✅ Heatmap berhasil dibuat:", output_file)