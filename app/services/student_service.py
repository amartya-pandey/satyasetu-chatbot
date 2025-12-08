from app.models.mongo_models import Certificate, StudentData, User
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class StudentDataService:
    """Service to query student-specific data from MongoDB."""
    
    @staticmethod
    async def get_student_certificates(user_email: str, user_role: str = "USER", organization_id: str = None) -> List[Dict]:
        """Get certificates based on user role."""
        try:
            # Query MongoDB certificates collection directly using Motor
            from motor.motor_asyncio import AsyncIOMotorClient
            from app.core.config import settings
            from bson import ObjectId
            
            client = AsyncIOMotorClient(settings.MONGODB_URL)
            db = client[settings.MONGODB_DB_NAME]
            
            # Build query based on role
            if user_role == "MOE":
                # MOE: Get ALL certificates across all institutions
                query = {}
                limit = 10000
            elif user_role in ["ADMIN", "INSTITUTION"] and organization_id:
                # Admin/Institution: Get all certificates from their institution
                query = {"institutionId": ObjectId(organization_id)}
                limit = 1000
            else:
                # Student: Get only their own certificates
                query = {"student.email": user_email}
                limit = 100
            
            certificates_cursor = db.certificates.find(query)
            certificates = await certificates_cursor.to_list(length=limit)
            
            client.close()
            
            return [
                {
                    "certificate_id": cert.get("certificateId"),
                    "name": cert.get("student", {}).get("fullName"),
                    "course": cert.get("student", {}).get("course"),
                    "issue_date": cert.get("issuedAt").strftime("%Y-%m-%d") if cert.get("issuedAt") else "N/A",
                    "grade": cert.get("student", {}).get("cgpa"),
                    "status": cert.get("status"),
                    "pdf_url": cert.get("pdfUrl"),
                    "department": cert.get("student", {}).get("department"),
                    "roll_number": cert.get("student", {}).get("rollNumber"),
                    "student_email": cert.get("student", {}).get("email")
                }
                for cert in certificates
            ]
        except Exception as e:
            logger.error(f"Error fetching certificates: {e}")
            return []
    
    @staticmethod
    async def get_student_data(student_id: str) -> Optional[Dict]:
        """Get student data from MongoDB."""
        try:
            student = await StudentData.find_one({"student_id": student_id})
            if student:
                return {
                    "enrollment_number": student.enrollment_number,
                    "courses_enrolled": student.courses_enrolled,
                    "certificates_earned": student.certificates_earned,
                    "total_credits": student.total_credits,
                    "current_semester": student.current_semester,
                    "department": student.department,
                    "additional_info": student.additional_info
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching student data: {e}")
            return None
    
    @staticmethod
    async def get_student_summary(user_email: str, user_name: str, user_role: str = "USER", organization_id: str = None) -> str:
        """Get a formatted summary based on user role."""
        try:
            # Get certificates based on role
            certificates = await StudentDataService.get_student_certificates(
                user_email, user_role, organization_id
            )
            cert_count = len(certificates)
            
            # Get student data (optional - for future use)
            student_data = None  # Not using student_id anymore
            
            # Format summary based on role
            if user_role == "MOE":
                summary = f"Ministry of Education - System Overview for {user_name}:\n\n"
                summary += f"Role: Ministry of Education (MOE)\n"
                summary += f"Total Certificates in System: {cert_count}\n"
                
                if certificates:
                    summary += "\nRecent Certificates (showing up to 15):\n"
                    for i, cert in enumerate(certificates[:15], 1):
                        summary += f"{i}. {cert['name']} ({cert.get('student_email', 'N/A')}) - {cert['course']} "
                        summary += f"(Issued: {cert['issue_date']}, Status: {cert['status']})\n"
                    
                    if cert_count > 15:
                        summary += f"\n...and {cert_count - 15} more certificates across all institutions.\n"
            elif user_role in ["ADMIN", "INSTITUTION"]:
                summary = f"Institution Admin Profile for {user_name}:\n\n"
                summary += f"Role: {user_role}\n"
                summary += f"Total Certificates Issued: {cert_count}\n"
                
                if certificates:
                    summary += "\nRecent Certificates (showing up to 10):\n"
                    for i, cert in enumerate(certificates[:10], 1):
                        summary += f"{i}. {cert['name']} ({cert.get('student_email', 'N/A')}) - {cert['course']} "
                        summary += f"(Issued: {cert['issue_date']}, Status: {cert['status']})\n"
                    
                    if cert_count > 10:
                        summary += f"\n...and {cert_count - 10} more certificates.\n"
            else:
                # Student profile
                summary = f"Student Profile for {user_name}:\n\n"
                
                if student_data:
                    summary += f"Enrollment Number: {student_data['enrollment_number']}\n"
                    summary += f"Department: {student_data.get('department', 'N/A')}\n"
                    summary += f"Current Semester: {student_data.get('current_semester', 'N/A')}\n"
                    summary += f"Total Credits: {student_data.get('total_credits', 0)}\n"
                    summary += f"Courses Enrolled: {len(student_data.get('courses_enrolled', []))}\n"
                
                summary += f"\nCertificates Issued: {cert_count}\n"
                
                if certificates:
                    summary += "\nCertificate Details:\n"
                    for i, cert in enumerate(certificates, 1):
                        summary += f"{i}. {cert['name']} - {cert['course']} "
                        summary += f"(Issued: {cert['issue_date']}, Status: {cert['status']})\n"
            
            return summary
        except Exception as e:
            logger.error(f"Error creating student summary: {e}")
            return f"Error retrieving data for {user_name}"
