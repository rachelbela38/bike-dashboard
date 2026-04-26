## Bike Sharing Interactive Dashboard
Dashboard interaktif untuk menganalisis pola penggunaan sepeda berdasarkan dataset Bike Sharing.

## Dashboard Preview
https://bike-dashboard-psduscudbx5mn7oocnvxoy.streamlit.app/

## Project Structure
submission
├── app.py
├── day.csv
├── hour.csv
├── notebook_submission_2.ipynb
├── requirements.txt
├── url.txt
└── README.md

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

## Key Insights
- Penyewaan sepeda dipengaruhi oleh musim dan kondisi cuaca
- Casual users lebih aktif pada waktu tertentu (non-working hours)
- Registered users memiliki pola penggunaan yang lebih stabil
- Terdapat pola peak hour dalam penggunaan sepeda

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly

