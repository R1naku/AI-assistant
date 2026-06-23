# models/database.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.sql import func
from core.database import Base


class IncomingEmail(Base):
    """Модель для входящих писем"""
    __tablename__ = "incoming_emails"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(String(255), unique=True, nullable=True)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    sender = Column(String(255), nullable=True)
    sender_name = Column(String(255), nullable=True)
    recipient = Column(String(255), nullable=True)
    
    category = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    classification_reason = Column(Text, nullable=True)
    
    draft_response = Column(Text, nullable=True)
    final_response = Column(Text, nullable=True)
    
    status = Column(String(50), default="pending")
    is_processed = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    
    received_at = Column(DateTime, server_default=func.now())
    processed_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    metadata_json = Column(JSON, nullable=True)
    attachments_count = Column(Integer, default=0)
    is_urgent = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Email(id={self.id}, subject='{self.subject[:30]}...')>"


class AgentLog(Base):
    """Модель для логов агентов"""
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100))
    email_id = Column(Integer, nullable=True)
    action = Column(String(50))
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    status = Column(String(50))
    error_message = Column(Text, nullable=True)
    processing_time = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class KnowledgeBase(Base):
    """Модель для базы знаний"""
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500))
    content = Column(Text)
    category = Column(String(100))
    tags = Column(JSON, nullable=True)
    source = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())