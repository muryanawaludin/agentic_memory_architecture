"""
Konfigurasi Global Sistem Memori Agen.
© 2026 Muryan Awaludin. Seluruh hak cipta dilindungi undang-undang.
"""
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class MemorySystemConfig:
    APP_TITLE: str = "Agentic Memory Architecture: Customer Support Engine"
    AUTHOR_COPYRIGHT: str = "© 2026 Muryan Awaludin. Seluruh hak cipta dilindungi undang-undang."
    
    # Path Sumber Data
    DATA_TICKETS_PATH: str = os.path.join(os.path.dirname(__file__), "data", "customer_support_tickets.csv")
    DATA_KB_PATH: str = os.path.join(os.path.dirname(__file__), "data", "knowledge_base.json")
    
    # Parameter Pembobotan Memori Kognitif Terpadu
    ALPHA_RECENCY: float = 0.25
    ALPHA_IMPORTANCE: float = 0.35
    ALPHA_RELEVANCE: float = 0.40
    DECAY_RATE: float = 0.98  # Peluruhan per hari
    MAX_WORKING_MEMORY_TOKENS: int = 2048

CONFIG = MemorySystemConfig()