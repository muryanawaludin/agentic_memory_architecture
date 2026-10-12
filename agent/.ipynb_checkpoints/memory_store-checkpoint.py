"""
Implementasi Komponen Penyimpanan dan Penarikan Tiga Lapis Memori:
Working Memory, Episodic Memory, dan Semantic Knowledge Store.
© 2026 Muryan Awaludin.
"""
import json
import math
import os
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import CONFIG
from agent.schema import ActiveTicketInput, WorkingMemoryState, EpisodicMemoryEntry, SemanticKnowledgeDocument

class WorkingMemoryController:
    """Mengelola buffer konteks sesi interaksi aktif dan ekstraksi status operasional."""
    @staticmethod
    def initialize_session(ticket: ActiveTicketInput) -> WorkingMemoryState:
        keywords = [word for word in ticket.ticket_subject.lower().split() if len(word) > 3]
        return WorkingMemoryState(
            session_id=f"SES-TCK-{ticket.ticket_id}",
            customer_name=ticket.customer_name,
            active_ticket_id=ticket.ticket_id,
            product_focus=ticket.product_purchased,
            current_inquiry=ticket.ticket_description,
            extracted_keywords=keywords
        )


class EpisodicMemoryEngine:
    """Mengelola penarikan pengalaman historis dari dataset 8.469 baris tiket pelanggan Kaggle."""
    def __init__(self, csv_path: str):
        self.df_tickets = pd.DataFrame()
        self._load_dataset(csv_path)

    def _load_dataset(self, csv_path: str):
        if not os.path.exists(csv_path):
            return
        try:
            self.df_tickets = pd.read_csv(csv_path)
            # Normalisasi kolom yang mengandung nilai kosong
            self.df_tickets["Resolution"] = self.df_tickets["Resolution"].fillna("Tidak ada catatan resolusi.")
            self.df_tickets["Customer Satisfaction Rating"] = self.df_tickets["Customer Satisfaction Rating"].fillna(3.0)
            self.df_tickets["Customer Name"] = self.df_tickets["Customer Name"].astype(str).str.strip()
        except Exception:
            self.df_tickets = pd.DataFrame()

    def retrieve_customer_episodes(self, customer_name: str, current_ticket_id: int, current_query: str, top_k: int = 3) -> List[EpisodicMemoryEntry]:
        if self.df_tickets.empty:
            return []

        # Filter seluruh tiket lampau milik pelanggan ini (mengecualikan tiket yang sedang aktif diproses)
        customer_history = self.df_tickets[
            (self.df_tickets["Customer Name"].str.lower() == customer_name.lower()) &
            (self.df_tickets["Ticket ID"] != current_ticket_id)
        ].copy()

        if customer_history.empty:
            return []

        # Pemetaan Skor Kepentingan Intrinsik dari Prioritas
        priority_weights = {"Critical": 1.0, "High": 0.75, "Medium": 0.50, "Low": 0.25}

        # Perhitungan Kemiripan Relevansi Semantik via TF-IDF
        corpus = [current_query] + (customer_history["Ticket Subject"] + " " + customer_history["Ticket Description"]).tolist()
        vectorizer = TfidfVectorizer().fit_transform(corpus)
        relevance_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:])[0]

        records: List[EpisodicMemoryEntry] = []
        now_date = datetime.strptime("2026-10-09", "%Y-%m-%d")

        for idx, (_, row) in enumerate(customer_history.iterrows()):
            # Estimasi delta hari dari Date of Purchase
            try:
                purchase_date = datetime.strptime(str(row["Date of Purchase"]), "%Y-%m-%d")
                delta_days = max(1.0, (now_date - purchase_date).days)
            except Exception:
                delta_days = 30.0

            # 1. Skor Kebaruan Temporal (Exponential Decay)
            recency = round(math.pow(CONFIG.DECAY_RATE, delta_days / 30.0), 4)

            # 2. Skor Kepentingan Bisnis
            importance = priority_weights.get(row["Ticket Priority"], 0.50)

            # 3. Skor Relevansi Semantik
            relevance = round(float(relevance_matrix[idx]), 4)

            # 4. Skor Memori Terpadu
            composite = round(
                (CONFIG.ALPHA_RECENCY * recency) +
                (CONFIG.ALPHA_IMPORTANCE * importance) +
                (CONFIG.ALPHA_RELEVANCE * relevance), 4
            )

            entry = EpisodicMemoryEntry(
                ticket_id=int(row["Ticket ID"]),
                product_purchased=str(row["Product Purchased"]),
                ticket_type=str(row["Ticket Type"]),
                ticket_subject=str(row["Ticket Subject"]),
                ticket_description=str(row["Ticket Description"]),
                ticket_status=str(row["Ticket Status"]),
                ticket_priority=str(row["Ticket Priority"]),
                resolution_text=str(row["Resolution"]),
                customer_satisfaction=float(row["Customer Satisfaction Rating"]),
                days_ago=round(delta_days, 1),
                recency_score=recency,
                importance_score=importance,
                relevance_score=relevance,
                composite_score=composite
            )
            records.append(entry)

        # Urutkan berdasarkan skor komposit tertinggi
        records.sort(key=lambda x: x.composite_score, reverse=True)
        return records[:top_k]


class SemanticKnowledgeEngine:
    """Mengelola temu kembali pengetahuan faktual SOP dan manual panduan perusahaan."""
    def __init__(self, kb_path: str):
        self.documents: List[SemanticKnowledgeDocument] = []
        self._load_knowledge_base(kb_path)

    def _load_knowledge_base(self, kb_path: str):
        if not os.path.exists(kb_path):
            return
        with open(kb_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                self.documents.append(SemanticKnowledgeDocument(
                    doc_id=item["doc_id"],
                    topic=item["topic"],
                    content=item["content"]
                ))

    def retrieve_guidelines(self, query: str, top_k: int = 2) -> List[SemanticKnowledgeDocument]:
        if not self.documents:
            return []

        doc_texts = [d.topic + " " + d.content for d in self.documents]
        corpus = [query] + doc_texts
        vectorizer = TfidfVectorizer().fit_transform(corpus)
        sim_scores = cosine_similarity(vectorizer[0:1], vectorizer[1:])[0]

        scored_docs: List[SemanticKnowledgeDocument] = []
        for idx, doc in enumerate(self.documents):
            score = round(float(sim_scores[idx]), 4)
            scored_docs.append(SemanticKnowledgeDocument(
                doc_id=doc.doc_id,
                topic=doc.topic,
                content=doc.content,
                similarity_score=score
            ))

        scored_docs.sort(key=lambda x: x.similarity_score, reverse=True)
        return scored_docs[:top_k]