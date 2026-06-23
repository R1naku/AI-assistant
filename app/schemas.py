# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmailRequest(BaseModel):
    """Модель для входящего запроса (письмо от клиента)"""
    subject: str
    body: str
    sender: Optional[str] = None
    sender_name: Optional[str] = None


class EmailResponse(BaseModel):
    """Модель для ответа API (классификация + черновик)"""
    category: str
    confidence: float
    reason: str
    draft_response: str
    sender: Optional[str] = None
    sender_name: Optional[str] = None


class EmailInDB(BaseModel):
    """Полная модель для работы с БД (соответствует таблице incoming_emails)"""
    id: int
    subject: str
    body: str
    sender: Optional[str] = None
    sender_name: Optional[str] = None
    recipient: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    classification_reason: Optional[str] = None
    draft_response: Optional[str] = None
    final_response: Optional[str] = None
    status: str
    is_processed: bool
    is_approved: bool
    received_at: datetime
    processed_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    metadata_json: Optional[dict] = None
    attachments_count: int = 0
    is_urgent: bool = False

    class Config:
        from_attributes = True


class EmailListResponse(BaseModel):
    """Модель для списка писем (краткая информация)"""
    id: int
    subject: str
    category: Optional[str] = None
    status: str
    received_at: datetime

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    """Модель для статистики"""
    total: int
    pending: int
    processed: int
    approved: int
    categories: dict