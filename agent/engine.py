"""
Mesin Orkestrasi Kognitif Tri-Memory:
Memadukan Working Memory, Rekam Jejak Episodik, dan Memori Semantik SOP.
© 2026 Muryan Awaludin.
"""
from config import CONFIG
from agent.schema import ActiveTicketInput, SynthesizedAgentDecision
from agent.memory_store import WorkingMemoryController, EpisodicMemoryEngine, SemanticKnowledgeEngine

class TriMemoryAgentCoordinator:
    def __init__(self):
        self.episodic_engine = EpisodicMemoryEngine(CONFIG.DATA_TICKETS_PATH)
        self.semantic_engine = SemanticKnowledgeEngine(CONFIG.DATA_KB_PATH)

    def resolve_ticket(self, ticket: ActiveTicketInput) -> SynthesizedAgentDecision:
        # 1. Inisialisasi Working Memory
        working_state = WorkingMemoryController.initialize_session(ticket)
        working_summary = f"Sesi: {working_state.session_id} | Produk: {ticket.product_purchased} | Gejala: '{ticket.ticket_subject}'"

        # 2. Penarikan Rekam Jejak dari Episodic Memory
        search_query = f"{ticket.product_purchased} {ticket.ticket_subject} {ticket.ticket_description}"
        episodes = self.episodic_engine.retrieve_customer_episodes(
            customer_name=ticket.customer_name,
            current_ticket_id=ticket.ticket_id,
            current_query=search_query,
            top_k=2
        )

        # 3. Penarikan Aturan dari Semantic Memory
        guidelines = self.semantic_engine.retrieve_guidelines(
            query=search_query,
            top_k=2
        )

        top_sop = guidelines[0] if guidelines else None
        sop_instruction = top_sop.content if top_sop else "Terapkan langkah diagnostik standar."

        # 4. Sintesis Kognitif Lintas Memori
        if episodes:
            past_notes = f"Kami mencatat riwayat tiket terdahulu Anda pada tiket #{episodes[0].ticket_id} ({episodes[0].ticket_subject}) dengan status '{episodes[0].ticket_status}'."
        else:
            past_notes = "Ini merupakan catatan interaksi tiket pertama Anda dalam sistem kami."

        synthesized_text = (
            f"Halo {ticket.customer_name}, terima kasih telah menghubungi pusat layanan kami terkait kendala pada {ticket.product_purchased}. "
            f"{past_notes} Menindaklanjuti keluhan '{ticket.ticket_subject}', berdasarkan prosedur standar {top_sop.doc_id if top_sop else 'SOP-01'}: "
            f"{sop_instruction}"
        )

        actionable_recommendasi = (
            f"1. Instruksikan pengguna menjalankan mitigasi {top_sop.doc_id if top_sop else 'Dasar'}. "
            f"2. Jika status tiket sebelumnya kritis dan belum terselesaikan, prioritaskan jadwal kunjungan teknisi lapangan."
        )

        return SynthesizedAgentDecision(
            ticket_id=ticket.ticket_id,
            customer_name=ticket.customer_name,
            product_name=ticket.product_purchased,
            working_memory_summary=working_summary,
            retrieved_episodes=episodes,
            retrieved_knowledge=guidelines,
            synthesized_resolution=synthesized_text,
            actionable_recommendation=actionable_recommendasi
        )