from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from app.models.university import University, DocumentTemplate
import logging
import json

logger = logging.getLogger(__name__)


class UniversityService:
    """Service for managing university data and document verification."""
    
    def get_university_by_id(self, db: Session, university_id: int) -> Optional[University]:
        """Get university by ID."""
        return db.query(University).filter(University.id == university_id).first()
    
    def get_university_by_code(self, db: Session, code: str) -> Optional[University]:
        """Get university by code."""
        return db.query(University).filter(University.code == code).first()
    
    def search_universities(
        self,
        db: Session,
        query: str,
        state: Optional[str] = None
    ) -> List[University]:
        """Search universities by name or location."""
        filters = [University.is_active == True]
        
        if query:
            filters.append(
                (University.name.ilike(f"%{query}%")) |
                (University.location.ilike(f"%{query}%"))
            )
        
        if state:
            filters.append(University.state == state)
        
        return db.query(University).filter(*filters).all()
    
    def create_university(self, db: Session, university_data: dict) -> University:
        """Create new university."""
        university = University(**university_data)
        db.add(university)
        db.commit()
        db.refresh(university)
        return university
    
    def get_document_templates(
        self,
        db: Session,
        university_id: int
    ) -> List[DocumentTemplate]:
        """Get document templates for a university."""
        return db.query(DocumentTemplate).filter(
            DocumentTemplate.university_id == university_id
        ).all()
    
    def get_verification_info(
        self,
        db: Session,
        university_id: int,
        document_type: str
    ) -> Dict:
        """Get verification information for a specific document type."""
        university = self.get_university_by_id(db, university_id)
        if not university:
            return {}
        
        template = db.query(DocumentTemplate).filter(
            DocumentTemplate.university_id == university_id,
            DocumentTemplate.document_type == document_type
        ).first()
        
        verification_info = {
            "university_name": university.name,
            "verification_url": university.verification_url,
            "verification_method": json.loads(university.verification_method) if university.verification_method else {},
            "common_forgery_patterns": json.loads(university.common_forgery_patterns) if university.common_forgery_patterns else []
        }
        
        if template:
            verification_info["template_features"] = json.loads(template.template_features) if template.template_features else {}
            verification_info["security_features"] = json.loads(template.security_features) if template.security_features else {}
        
        return verification_info


# Singleton instance
university_service = UniversityService()
