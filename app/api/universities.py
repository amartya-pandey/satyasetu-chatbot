from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.university import University
from app.schemas.university import UniversityResponse, UniversityCreate
from app.services.university_service import university_service
from app.models.mongo_models import User, Certificate
from bson import ObjectId
from app.core.mongodb import get_database

router = APIRouter(prefix="/universities", tags=["Universities"])


@router.get("/", response_model=List[UniversityResponse])
async def search_universities(
    query: Optional[str] = Query(None, description="Search by name or location"),
    state: Optional[str] = Query(None, description="Filter by state"),
    db: Session = Depends(get_db)
):
    """Search universities."""
    universities = university_service.search_universities(db, query or "", state)
    return universities


@router.get("/{university_id}", response_model=UniversityResponse)
async def get_university(
    university_id: int,
    db: Session = Depends(get_db)
):
    """Get university by ID."""
    university = university_service.get_university_by_id(db, university_id)
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    return university


@router.post("/", response_model=UniversityResponse)
async def create_university(
    university: UniversityCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new university (admin only)."""
    # Convert forgery patterns to JSON string if provided
    import json
    
    university_data = university.dict()
    if university_data.get("verification_method"):
        university_data["verification_method"] = json.dumps(university_data["verification_method"])
    if university_data.get("common_forgery_patterns"):
        university_data["common_forgery_patterns"] = json.dumps(university_data["common_forgery_patterns"])
    
    return university_service.create_university(db, university_data)


@router.get("/{university_id}/verification/{document_type}")
async def get_verification_info(
    university_id: int,
    document_type: str,
    db: Session = Depends(get_db)
):
    """Get verification information for a specific document type."""
    info = university_service.get_verification_info(db, university_id, document_type)
    if not info:
        raise HTTPException(status_code=404, detail="Verification info not found")
    return info


@router.get("/institution/{institution_id}/details")
async def get_institution_details(
    institution_id: str,
    include_certificates: bool = Query(True, description="Include certificates issued by sub-admins"),
    limit_certificates: int = Query(100, description="Maximum number of certificates to return")
):
    """
    Get comprehensive institution details including all sub-admins and certificates.
    This endpoint shows all sub-admin details linked to the institution and 
    all certificates issued by sub-admins attached to it.
    
    Parameters:
    - institution_id: The MongoDB ObjectId of the institution
    - include_certificates: Whether to include certificate details (default: True)
    - limit_certificates: Maximum number of certificates to return (default: 100)
    """
    try:
        # Convert string to ObjectId
        if not ObjectId.is_valid(institution_id):
            raise HTTPException(status_code=400, detail="Invalid institution ID format")
        
        org_id = ObjectId(institution_id)
        mongo_db = get_database()
        
        # Get institution details
        institution = await mongo_db.institutions.find_one({"_id": org_id})
        if not institution:
            raise HTTPException(status_code=404, detail="Institution not found")
        
        # Get all users (sub-admins) linked to this institution
        all_users = await User.find({"organization": str(org_id)}).to_list()
        
        # Organize users by role
        sub_admins = []
        regular_users = []
        
        for user in all_users:
            user_data = {
                "id": str(user.id),
                "name": user.full_name,
                "email": user.email,
                "username": user.username,
                "role": user.role,
                "created_at": user.created_at,
                "is_active": user.is_active,
                "meta": user.meta or {}
            }
            
            if user.role in ['ADMIN', 'SUBADMIN', 'INSTITUTION_ADMIN', 'INSTITUTION']:
                sub_admins.append(user_data)
            else:
                regular_users.append(user_data)
        
        # Get certificates issued by this institution
        certificates_data = []
        total_certificates = 0
        
        if include_certificates:
            # Query certificates from MongoDB using native collection
            certificates_cursor = mongo_db.certificates.find(
                {"institutionId": org_id}
            ).limit(limit_certificates)
            
            certificates_list = await certificates_cursor.to_list(length=limit_certificates)
            total_certificates = await mongo_db.certificates.count_documents({"institutionId": org_id})
            
            # Process certificates
            for cert in certificates_list:
                # Get issuer details
                issuer_info = None
                if cert.get('issuerId'):
                    issuer = await mongo_db.users.find_one({"_id": cert.get('issuerId')})
                    if issuer:
                        issuer_info = {
                            "id": str(issuer.get('_id')),
                            "name": issuer.get('name') or issuer.get('full_name'),
                            "email": issuer.get('email'),
                            "role": issuer.get('role')
                        }
                
                cert_data = {
                    "certificate_id": cert.get('certificateId'),
                    "student_name": cert.get('student', {}).get('fullName'),
                    "course": cert.get('student', {}).get('course'),
                    "department": cert.get('student', {}).get('department'),
                    "roll_number": cert.get('student', {}).get('rollNumber'),
                    "registration_number": cert.get('student', {}).get('registrationNumber'),
                    "cgpa": cert.get('student', {}).get('cgpa'),
                    "passing_year": cert.get('student', {}).get('passingYear'),
                    "issue_date": cert.get('student', {}).get('issueDate') or cert.get('issuedAt'),
                    "status": cert.get('status'),
                    "pdf_url": cert.get('pdfUrl'),
                    "verification_url": cert.get('verificationUrl'),
                    "issuer": issuer_info,
                    "blockchain_status": cert.get('blockchainStatus'),
                    "created_at": cert.get('createdAt'),
                    "template_name": cert.get('metadata', {}).get('templateName')
                }
                certificates_data.append(cert_data)
        
        # Build response
        response = {
            "institution": {
                "id": str(institution.get('_id')),
                "name": institution.get('name'),
                "email": institution.get('email'),
                "address": institution.get('address'),
                "type": institution.get('type'),
                "created_at": institution.get('createdAt'),
                "updated_at": institution.get('updatedAt')
            },
            "statistics": {
                "total_sub_admins": len(sub_admins),
                "total_regular_users": len(regular_users),
                "total_certificates_issued": total_certificates,
                "certificates_shown": len(certificates_data)
            },
            "sub_admins": sub_admins,
            "regular_users": regular_users,
            "certificates": certificates_data if include_certificates else []
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching institution details: {str(e)}")


@router.get("/user/{user_email}/institution-details")
async def get_user_institution_details(
    user_email: str,
    include_certificates: bool = Query(True, description="Include certificates issued by sub-admins"),
    limit_certificates: int = Query(100, description="Maximum number of certificates to return")
):
    """
    Get institution details by user email (e.g., Mumbai University SE ID).
    Shows all sub-admin details and certificates linked to the user's institution.
    
    Parameters:
    - user_email: Email of the institution admin or sub-admin
    - include_certificates: Whether to include certificate details (default: True)
    - limit_certificates: Maximum number of certificates to return (default: 100)
    """
    try:
        # Find user by email
        user = await User.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user.organization:
            raise HTTPException(status_code=400, detail="User is not linked to any institution")
        
        # Call the institution details endpoint with the organization ID
        return await get_institution_details(
            institution_id=user.organization,
            include_certificates=include_certificates,
            limit_certificates=limit_certificates
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user institution details: {str(e)}")
