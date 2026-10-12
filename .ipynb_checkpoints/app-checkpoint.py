"""
Aplikasi Antarmuka Pengguna Streamlit: Dasbor Arsitektur Memori Tiga Lapis Agen.
Mengintegrasikan Dataset Kaggle customer_support_tickets.csv (8.469 baris).
© 2026 Muryan Awaludin. Seluruh hak cipta dilindungi undang-undang.
"""
import streamlit as st
import pandas as pd
import json
import os
from config import CONFIG
from agent.schema import ActiveTicketInput
from agent.engine import TriMemoryAgentCoordinator

st.set_page_config(
    page_title=CONFIG.APP_TITLE,
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Agentic Memory Architecture Dashboard")
st.caption("Penerapan Tiga Lapisan Kognitif: Working Memory, Episodic Memory, dan Semantic Retrieval Berbasis Dataset Kaggle")

# Inisialisasi Koordinator Agen
if "memory_coordinator" not in st.session_state:
    st.session_state.memory_coordinator = TriMemoryAgentCoordinator()

# Pemuatan Dataset Kaggle
@st.cache_data
def load_tickets_data():
    if os.path.exists(CONFIG.DATA_TICKETS_PATH):
        df = pd.read_csv(CONFIG.DATA_TICKETS_PATH)
        df["Customer Name"] = df["Customer Name"].astype(str).str.strip()
        df["Ticket Subject"] = df["Ticket Subject"].astype(str).str.strip()
        df["Product Purchased"] = df["Product Purchased"].astype(str).str.strip()
        return df
    return pd.DataFrame()

df_raw = load_tickets_data()

# Sidebar: Pemilihan Pelanggan & Tiket
with st.sidebar:
    st.header("📋 Pemilihan Tiket Masuk")
    st.markdown("Sumber: *Kaggle Customer Support Ticket Dataset* (8.469 baris)")

    if not df_raw.empty:
        # Cari pelanggan yang memiliki lebih dari satu tiket untuk demonstrasi memori episodik
        name_counts = df_raw["Customer Name"].value_counts()
        frequent_customers = name_counts[name_counts > 1].index.tolist()

        mode_filter = st.radio(
            "Pilihan Sampel:",
            ["Pelanggan dengan Riwayat Ganda (Demo Memori)", "Seluruh Antrean Tiket"],
            index=0
        )

        if mode_filter.startswith("Pelanggan dengan Riwayat"):
            filtered_df = df_raw[df_raw["Customer Name"].isin(frequent_customers)].reset_index(drop=True)
        else:
            filtered_df = df_raw

        selected_row_idx = st.selectbox(
            "Pilih Antrean Tiket:",
            range(len(filtered_df)),
            format_func=lambda i: f"[#{filtered_df.iloc[i]['Ticket ID']}] {filtered_df.iloc[i]['Customer Name']} - {filtered_df.iloc[i]['Product Purchased']}"
        )

        row = filtered_df.iloc[selected_row_idx]
        active_ticket = ActiveTicketInput(
            ticket_id=int(row["Ticket ID"]),
            customer_name=str(row["Customer Name"]),
            customer_email=str(row["Customer Email"]),
            product_purchased=str(row["Product Purchased"]),
            ticket_type=str(row["Ticket Type"]),
            ticket_subject=str(row["Ticket Subject"]),
            ticket_description=str(row["Ticket Description"]),
            ticket_priority=str(row["Ticket Priority"]),
            date_of_purchase=str(row["Date of Purchase"])
        )
    else:
        st.error("Dataset 'customer_support_tickets.csv' belum ditemukan di folder data/.")
        active_ticket = None

    btn_run = st.button("🚀 Aktifkan Sistem Memori Agen", type="primary", use_container_width=True, disabled=(active_ticket is None))

    if active_ticket:
        st.divider()
        st.markdown(f"**ID Tiket Aktif:** `#{active_ticket.ticket_id}`")
        st.markdown(f"**Nama Pelanggan:** `{active_ticket.customer_name}`")
        st.markdown(f"**Produk:** `{active_ticket.product_purchased}`")
        st.markdown(f"**Prioritas:** `{active_ticket.ticket_priority}`")
        st.markdown(f"**Tanggal Beli:** `{active_ticket.date_of_purchase}`")
        st.markdown("**Deskripsi Keluhan Aktif:**")
        st.info(active_ticket.ticket_description)

    st.divider()
    st.markdown("© 2026 **Muryan Awaludin**  \nHak Cipta Dilindungi.")

# Area Kerja Utama
if btn_run and active_ticket:
    with st.spinner("Mengaktifkan integrasi tiga lapis memori kognitif..."):
        st.session_state.memory_result = st.session_state.memory_coordinator.resolve_ticket(active_ticket)

if "memory_result" in st.session_state and st.session_state.memory_result is not None:
    res = st.session_state.memory_result

    st.subheader(f"🔍 Audit Kognitif Lintas Lapisan Memori: Tiket #{res.ticket_id}")
    col_work, col_epi, col_sem = st.columns(3)

    # 1. Kolom Working Memory
    with col_work:
        st.markdown("### ⚡ Working Memory")
        st.caption("Fokus komputasi aktif jendela saat ini")
        with st.container(border=True):
            st.markdown(f"**Status Sesi:**\n`{res.working_memory_summary}`")
            st.markdown(f"**Pelanggan:** `{res.customer_name}`")
            st.markdown(f"**Produk Fokus:** `{res.product_name}`")
            st.markdown(f"**Batas Alokasi Token:** `{CONFIG.MAX_WORKING_MEMORY_TOKENS} token`")

    # 2. Kolom Episodic Memory
    with col_epi:
        st.markdown("### 📜 Episodic Memory")
        st.caption("Pengalaman lampau dari dataset 8.469 tiket")
        if res.retrieved_episodes:
            for ep in res.retrieved_episodes:
                with st.container(border=True):
                    st.markdown(f"**Tiket Lampau:** `#{ep.ticket_id}` - *{ep.ticket_subject}*")
                    st.markdown(f"**Produk Lampau:** `{ep.product_purchased}`")
                    st.markdown(f"**Status Lalu:** `{ep.ticket_status}` | Prioritas: `{ep.ticket_priority}`")
                    st.markdown(f"**Waktu Berlalu:** `{ep.days_ago}` hari")
                    st.caption(f"Skor: Recency `{ep.recency_score}` | Relevance `{ep.relevance_score}` | Composite `{ep.composite_score}`")
        else:
            st.info("Tidak ada riwayat tiket lampau untuk pelanggan ini (Interaksi Pertama).")

    # 3. Kolom Semantic Memory
    with col_sem:
        st.markdown("### 📚 Semantic Memory")
        st.caption("Manual pengetahuan SOP industri terindeks")
        for kb in res.retrieved_knowledge:
            with st.container(border=True):
                st.markdown(f"**Dokumen:** `{kb.doc_id}` - *{kb.topic}*")
                st.markdown(f"**Skor Kemiripan Kosinus:** `{kb.similarity_score}`")
                st.caption(f"Kutipan Panduan: {kb.content[:130]}...")

    st.divider()

    # Hasil Sintesis Respons
    st.subheader("💡 Hasil Sintesis Kognitif dan Tindakan Resolusi")
    col_out_left, col_out_right = st.columns([1.2, 0.8])

    with col_out_left:
        st.markdown("**Draf Respons Otomatis ke Pelanggan:**")
        st.success(res.synthesized_resolution)

    with col_out_right:
        st.markdown("**Rekomendasi Prosedural untuk Tim Operasional:**")
        st.info(res.actionable_recommendation)
else:
    st.info("Pilih baris tiket pada panel sebelah kiri lalu tekan tombol **'Aktifkan Sistem Memori Agen'** untuk memulai analisis.")

st.divider()
st.caption(CONFIG.AUTHOR_COPYRIGHT)