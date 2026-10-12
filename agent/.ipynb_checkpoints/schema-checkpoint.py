"""
Definisi Skema Model Data untuk Arsitektur Memori Tiga Lapis.
© 2026 Muryan Awaludin.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ActiveTicketInput(BaseModel):
    ticket_id: int
    customer_name: str
    customer_email: str
    product_purchased: str
    ticket_type: str
    ticket_subject: str
    ticket_description: str
    ticket_priority: str
    date_of_purchase: str

class WorkingMemoryState(BaseModel):
    session_id: str
    customer_name: str
    active_ticket_id: int
    product_focus: str
    current_inquiry: str
    extracted_keywords: List[str] = Field(default_factory=list)

class EpisodicMemoryEntry(BaseModel):
    ticket_id: int
    product_purchased: str
    ticket_type: str
    ticket_subject: str
    ticket_description: str
    ticket_status: str
    ticket_priority: str
    resolution_text: str
    customer_satisfaction: Optional[float] = None
    days_ago: float
    recency_score: float = 0.0
    importance_score: float = 0.0
    relevance_score: float = 0.0
    composite_score: float = 0.0

class SemanticKnowledgeDocument(BaseModel):
    doc_id: str
    topic: str
    content: str
    similarity_score: float = 0.0

class SynthesizedAgentDecision(BaseModel):
    ticket_id: int
    customer_name: str
    product_name: str
    working_memory_summary: str
    retrieved_episodes: List[EpisodicMemoryEntry]
    retrieved_knowledge: List[SemanticKnowledgeDocument]
    synthesized_resolution: str
    actionable_recommendation: str