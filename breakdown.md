## 🧱 System Components

1. **Data Ingestion**

   - Fetch data dari Google Maps, TomTom, dll.
   - Simpan data secara terstruktur (CSV, SQLite, atau PostgreSQL)

2. **Data Processing & Storage**

   - Membersihkan dan menyiapkan data
   - Simpan sebagai dataset time-series

3. **Modeling**

   - Time series forecasting (Prophet / LSTM)
   - Anomaly detection based on error threshold

4. **Alerting Logic**

   - Jika selisih prediksi vs aktual > threshold, trigger alert

5. **API Backend**

   - FastAPI endpoint untuk prediksi, alert, dan status

6. **Deployment**

   - Local (Docker)
   - Cloud (GCP, Cloud Run atau Cloud Scheduler)

7. **Monitoring & Logging**

   - Loguru logger
   - Placeholder untuk observabilitas (Grafana, dsb.)

8. **Documentation**
   - Swagger/OpenAPI untuk API
   - Setup guide, demo script
