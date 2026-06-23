# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from inbox_agent import inbox_agent
from core.database import get_db
from services.email_service import EmailService
from app.schemas import (
    EmailRequest,
    EmailResponse,
    EmailInDB,
    EmailListResponse,
    StatsResponse
)

app = FastAPI(
    title="AI-assistant",
    description="An AI assistant that can help you with various tasks.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== ЭНДПОИНТЫ ==========

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "AI Assistant API",
        "llm": "LM Studio",
        "database": "PostgreSQL"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/llm_test")
async def llm_test():
    from llm_service import llm_service
    try:
        response = llm_service.generate(
            prompt="Привет, как дела?",
            system_prompt="Ты дружелюбный помощник."
        )
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/v1/inbox/process", response_model=EmailResponse)
async def process_email(
    email: EmailRequest,
    db: Session = Depends(get_db)
):
    """Полная обработка письма: классификация + черновик + сохранение в БД"""
    try:
        email_service = EmailService(db)
        
        # 1. Сохраняем письмо в БД
        email_record = email_service.create_email(
            subject=email.subject,
            body=email.body,
            sender=email.sender,
            sender_name=email.sender_name
        )
        
        # 2. Классифицируем
        classification = inbox_agent.classify_email(
            email.subject,
            email.body,
            sender=email.sender,
            sender_name=email.sender_name
        )
        
        # 3. Сохраняем классификацию в БД
        email_service.update_classification(
            email_record.id,
            classification.get("category", "other"),
            classification.get("confidence", 0.0),
            classification.get("reason", "")
        )
        
        # 4. Генерируем черновик
        draft = inbox_agent.generate_draft_response(
            email.subject,
            email.body,
            category=classification.get("category", "general_question"),
            sender=email.sender,
            sender_name=email.sender_name
        )
        
        # 5. Сохраняем черновик в БД
        email_service.update_draft(email_record.id, draft)

        return EmailResponse(
            category=classification.get("category", "other"),
            confidence=classification.get("confidence", 0.0),
            reason=classification.get("reason", ""),
            draft_response=draft,
            sender=email.sender,
            sender_name=email.sender_name
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/inbox/classify")
async def classify_email(
    email: EmailRequest,
    db: Session = Depends(get_db)
):
    """Только классифицирует письмо без генерации ответа, сохраняет в БД"""
    try:
        email_service = EmailService(db)
        
        # Сохраняем письмо
        email_record = email_service.create_email(
            subject=email.subject,
            body=email.body,
            sender=email.sender,
            sender_name=email.sender_name
        )
        
        # Классифицируем
        classification = inbox_agent.classify_email(
            email.subject, 
            email.body,
            sender=email.sender,
            sender_name=email.sender_name
        )
        
        # Сохраняем классификацию
        email_service.update_classification(
            email_record.id,
            classification.get("category", "other"),
            classification.get("confidence", 0.0),
            classification.get("reason", "")
        )
        
        return classification
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/emails", response_model=list[EmailInDB])
async def get_all_emails(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Получить все письма из БД с пагинацией"""
    try:
        email_service = EmailService(db)
        emails = email_service.get_all_emails(limit, offset)
        
        return [
            EmailInDB(
                id=e.id,
                subject=e.subject,
                body=e.body,
                sender=e.sender,
                sender_name=e.sender_name,
                category=e.category,
                confidence=e.confidence,
                classification_reason=e.classification_reason,
                draft_response=e.draft_response,
                final_response=e.final_response,
                status=e.status,
                is_processed=e.is_processed,
                is_approved=e.is_approved,
                received_at=e.received_at,
                processed_at=e.processed_at,
                approved_at=e.approved_at,
                created_at=e.created_at,
                updated_at=e.updated_at,
                is_urgent=e.is_urgent or False
            )
            for e in emails
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/emails/{email_id}", response_model=EmailInDB)
async def get_email(
    email_id: int,
    db: Session = Depends(get_db)
):
    """Получить письмо по ID"""
    try:
        email_service = EmailService(db)
        email = email_service.get_email(email_id)
        
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        return EmailInDB(
            id=email.id,
            subject=email.subject,
            body=email.body,
            sender=email.sender,
            sender_name=email.sender_name,
            category=email.category,
            confidence=email.confidence,
            classification_reason=email.classification_reason,
            draft_response=email.draft_response,
            final_response=email.final_response,
            status=email.status,
            is_processed=email.is_processed,
            is_approved=email.is_approved,
            received_at=email.received_at,
            processed_at=email.processed_at,
            approved_at=email.approved_at,
            created_at=email.created_at,
            updated_at=email.updated_at,
            is_urgent=email.is_urgent or False
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Получить статистику по письмам"""
    try:
        email_service = EmailService(db)
        stats = email_service.get_stats()
        return StatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))