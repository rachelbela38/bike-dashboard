Bike Sharing Interactive Dashboard

*Deskripsi*
Dashboard interaktif ini dibuat untuk menganalisis pola penggunaan sepeda berdasarkan dataset Bike Sharing. Dashboard ini dikembangkan untuk menjawab beberapa pertanyaan bisnis terkait faktor yang memengaruhi jumlah penyewaan sepeda serta perilaku pengguna.

*Tujuan Analisis*
Dashboard ini bertujuan untuk menjawab pertanyaan berikut:
1. Faktor apa saja yang memengaruhi rendahnya jumlah penyewaan sepeda pada hari kerja selama musim panas tahun 2012?
2. Pada kondisi apa proporsi pengguna casual melebihi 40% dari total penyewaan selama kuartal 2 tahun 2012?
3. Bagaimana perbedaan pola penyewaan antara pengguna casual dan registered berdasarkan jam penggunaan?

*Fitur Dashboard*
Filter interaktif berdasarkan:
  - Tahun
  - Musim (Season)
  - Kondisi cuaca (Weather)
- Visualisasi tren penyewaan sepeda
- Analisis demand rendah (Low Demand)
- Analisis proporsi casual user
- Perbandingan pola penggunaan antara casual dan registered users
- Analisis pola penggunaan per jam (hourly analysis)
- Tabel data harian dan per jam

*Dataset yang digunakan:*
- day.csv → data agregasi harian
- hour.csv→ data agregasi per jam

*Teknologi yang Digunakan*
- Python
- Streamlit
- Pandas
- Plotly

*Cara Menjalankan Dashboard Secara Lokal*
1. Install dependencies: pip install -r requirements.txt
2. Jalankanaplikasi: streamlit run app.py

*Dashboard Online* : https://bike-dashboard-psduscudbx5mn7oocnvxoy.streamlit.app/

*Insight Utama*
- Jumlah penyewaan sepeda dipengaruhi oleh kondisi cuaca, musim, dan hari kerja
- Casual users cenderung aktif pada waktu tertentu (non-working hours)
- Registered users menunjukkan pola penggunaan yang lebih stabil dan rutin
- Aktivitas penyewaan memiliki pola jam tertentu (peak hour)
Dashboard ini tidak hanya menampilkan visualisasi, tetapi juga menyediakan insight berbasis data untuk membantu memahami pola penggunaan sepeda secara lebih mendalam.
