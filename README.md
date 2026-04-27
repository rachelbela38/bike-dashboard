## Bike Sharing Interactive Dashboard
Dashboard interaktif untuk menganalisis pola penggunaan sepeda berdasarkan dataset Bike Sharing. Project ini telah diperbarui berdasarkan hasil revisi, khususnya pada bagian Exploratory Data Analysis (EDA) dan Visualization. Perbaikan dilakukan dengan menambahkan analisis yang lebih lengkap, penggunaan agregasi data, serta penyesuaian visualisasi agar lebih sesuai dengan pertanyaan bisnis. Dashboard interaktif juga telah diperbarui untuk mencerminkan hasil analisis terbaru.


## Dashboard Preview
https://bike-dashboard-rachelbela38.streamlit.app/


## Business Questions
1. Faktor apa yang memengaruhi rendahnya penyewaan sepeda pada hari kerja di musim panas tahun 2012?
2. Kapan proporsi casual user melebihi 40% dari total penyewaan?
3. Bagaimana perbedaan pola penggunaan antara casual dan registered users berdasarkan jam?


## Setup Environment - Shell / Terminal
pip install -r requirements.txt


## Run Streamlit App
streamlit run app.py


## Features
- Filter interaktif (tahun, musim, cuaca)
- Analisis demand rendah
- Analisis proporsi casual user
- Perbandingan casual vs registered
- Analisis pola per jam (hourly)
- Tabel data harian dan per jam


## Key Insight
- Faktor cuaca dan suhu secara bersama-sama memengaruhi rendahnya demand
- Pengguna casual lebih dominan pada waktu santai dan kondisi rekreasi
- Perbedaan utama antara casual dan registered terletak pada volume penggunaan, bukan pola waktu


## Tech Stack
- Python 
- Pandas 
- Seaborn & Matplotlib 
- Plotly 
- Streamlit 

