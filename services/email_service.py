# services/email_service.py
from sqlalchemy.orm import Session
from models.database import IncomingEmail
from datetime import datetime
from typing import Optional, List, Dict, Any


class EmailService:
    """Сервис для работы с письмами в БД"""

    def __init__(self, db: Session):
        self.db = db

    def create_email(
        self,
        subject: str,
        body: str,
        sender: Optional[str] = None,
        sender_name: Optional[str] = None
    ) -> IncomingEmail:
        """Создает запись о письме в БД"""
        email = IncomingEmail(
            subject=subject,
            body=body,
            sender=sender,
            sender_name=sender_name,
            status="pending"
        )
        self.db.add(email)
        self.db.commit()
        self.db.refresh(email)
        return email

    def update_classification(
        self,
        email_id: int,
        category: str,
        confidence: float,
        reason: str
    ) -> Optional[IncomingEmail]:
        """Обновляет классификацию письма"""
        email = self.db.query(IncomingEmail).filter(IncomingEmail.id == email_id).first()
        if email:
            email.category = category
            email.confidence = confidence
            email.classification_reason = reason
            email.is_processed = True
            email.processed_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(email)
            return email
        return None

    def update_draft(self, email_id: int, draft_response: str) -> Optional[IncomingEmail]:
        """Обновляет черновик ответа"""
        email = self.db.query(IncomingEmail).filter(IncomingEmail.id == email_id).first()
        if email:
            email.draft_response = draft_response
            self.db.commit()
            self.db.refresh(email)
            return email
        return None

    def approve_email(self, email_id: int, final_response: Optional[str] = None) -> Optional[IncomingEmail]:
        """Утверждает письмо"""
        email = self.db.query(IncomingEmail).filter(IncomingEmail.id == email_id).first()
        if email:
            email.status = "approved"
            email.is_approved = True
            email.approved_at = datetime.utcnow()
            if final_response:
                email.final_response = final_response
            self.db.commit()
            self.db.refresh(email)
            return email
        return None

    def get_email(self, email_id: int) -> Optional[IncomingEmail]:
        """Получает письмо по ID"""
        return self.db.query(IncomingEmail).filter(IncomingEmail.id == email_id).first()

    def get_all_emails(self, limit: int = 100, offset: int = 0) -> List[IncomingEmail]:
        """Получает все письма с пагинацией"""
        return self.db.query(IncomingEmail).order_by(
            IncomingEmail.received_at.desc()
        ).offset(offset).limit(limit).all()

    def get_pending_emails(self) -> List[IncomingEmail]:
        """Получает все необработанные письма"""
        return self.db.query(IncomingEmail).filter(IncomingEmail.is_processed == False).all()

    def get_stats(self) -> Dict[str, Any]:
        """Получает статистику по письмам"""
        from sqlalchemy import func
        
        total = self.db.query(IncomingEmail).count()
        pending = self.db.query(IncomingEmail).filter(IncomingEmail.is_processed == False).count()
        processed = self.db.query(IncomingEmail).filter(IncomingEmail.is_processed == True).count()
        approved = self.db.query(IncomingEmail).filter(IncomingEmail.is_approved == True).count()
        
        categories = self.db.query(
            IncomingEmail.category,
            func.count(IncomingEmail.id)
        ).group_by(IncomingEmail.category).all()
        
        return {
            "total": total,
            "pending": pending,
            "processed": processed,  # ← ДОБАВЛЕНО!
            "approved": approved,
            "categories": {cat: count for cat, count in categories if cat is not None}
        }

    def delete_email(self, email_id: int) -> bool:
        """Удаляет письмо"""
        email = self.db.query(IncomingEmail).filter(IncomingEmail.id == email_id).first()
        if email:
            self.db.delete(email)
            self.db.commit()
            return True
        return False