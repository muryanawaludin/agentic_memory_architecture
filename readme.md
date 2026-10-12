# Agentic Memory Architecture: Working, Episodic, and Semantic Retrieval Engine

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agentic-memory-engine.streamlit.app)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/muryanawaludin/agentic-memory-architecture)

Implementasi arsitektur memori kognitif terpadu untuk agen otonom tingkat enterprise (*Agentic AI*). Proyek ini mengintegrasikan tiga lapisan memori biologis komputasional: **Working Memory** (buffer sesi aktif), **Episodic Memory** (riwayat pengalaman dengan peluruhan eksponensial berbasis 8.469 tiket Kaggle), dan **Semantic Memory** (pencarian dokumen SOP industri via representasi vektor hibrida).

---

## 🔬 Fondasi Teoretis

Sistem ini memodelkan penarikan memori terpadu (*Unified Memory Retrieval*) berdasarkan formulasi kognitif Park et al. (2023):

$$S(m, q) = \alpha_{\text{rec}} \cdot s_{\text{rec}}(m) + \alpha_{\text{imp}} \cdot s_{\text{imp}}(m) + \alpha_{\text{rel}} \cdot s_{\text{rel}}(m, q)$$

- **Kebaruan Temporal ($s_{\text{rec}}$):** $s_{\text{rec}}(m) = \gamma^{\Delta t_m}$ (Peluruhan eksponensial Ebbinghaus).
- **Kepentingan Bisnis ($s_{\text{imp}}$):** Pemetaan derajat urgensi tiket (*Critical, High, Medium, Low*).
- **Relevansi Semantik ($s_{\text{rel}}$):** Kedekatan kosinus di ruang vektor teks.

---

## 📁 Sumber Data

Dataset yang digunakan bersumber dari repositori publik Kaggle:
- **Customer Support Ticket Dataset**: `https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset` (8.469 baris entri).
- **Knowledge Base JSON**: Manual panduan pemecahan masalah dan klaim garansi produk standar industri.

---

## 🚀 Menjalankan Secara Lokal

1. **Clone Repositori:**
   ```bash
   git clone [https://github.com/muryanawaludin/agentic_memory_architecture.git](https://github.com/muryanawaludin/agentic_memory_architecture.git)
   cd agentic-memory-architecture