"""
Example Usage of Institution Details API

This script demonstrates how to use the new endpoints to get:
1. All sub-admin details linked to an institution
2. All certificates issued by sub-admins attached to the institution

Endpoints:
1. GET /universities/institution/{institution_id}/details
2. GET /universities/user/{user_email}/institution-details
"""

import requests
import json

# Base URL of your API
BASE_URL = "http://localhost:8000"  # Update with your actual API URL

def get_institution_by_id(institution_id: str, include_certificates: bool = True, limit: int = 100):
    """
    Get institution details by institution ID
    
    Args:
        institution_id: MongoDB ObjectId of the institution
        include_certificates: Whether to include certificate details
        limit: Maximum number of certificates to return
    """
    url = f"{BASE_URL}/universities/institution/{institution_id}/details"
    params = {
        "include_certificates": include_certificates,
        "limit_certificates": limit
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print("=" * 80)
        print(f"INSTITUTION: {data['institution']['name']}")
        print("=" * 80)
        print(f"\nInstitution Email: {data['institution']['email']}")
        print(f"Institution Type: {data['institution']['type']}")
        
        print("\n" + "=" * 80)
        print("STATISTICS:")
        print("=" * 80)
        print(f"Total Sub-Admins: {data['statistics']['total_sub_admins']}")
        print(f"Total Regular Users: {data['statistics']['total_regular_users']}")
        print(f"Total Certificates Issued: {data['statistics']['total_certificates_issued']}")
        print(f"Certificates in Response: {data['statistics']['certificates_shown']}")
        
        print("\n" + "=" * 80)
        print(f"SUB-ADMINS ({len(data['sub_admins'])}):")
        print("=" * 80)
        for admin in data['sub_admins']:
            print(f"\n  • Name: {admin['name']}")
            print(f"    Email: {admin['email']}")
            print(f"    Role: {admin['role']}")
            print(f"    Username: {admin['username']}")
            print(f"    Active: {admin['is_active']}")
            if admin.get('meta'):
                print(f"    Meta: {admin['meta']}")
        
        if include_certificates and data['certificates']:
            print("\n" + "=" * 80)
            print(f"CERTIFICATES (showing first {len(data['certificates'])}):")
            print("=" * 80)
            for cert in data['certificates'][:5]:  # Show first 5
                print(f"\n  Certificate ID: {cert['certificate_id']}")
                print(f"  Student: {cert['student_name']}")
                print(f"  Course: {cert['course']} - {cert['department']}")
                print(f"  Roll Number: {cert['roll_number']}")
                print(f"  CGPA: {cert['cgpa']}")
                print(f"  Status: {cert['status']}")
                if cert.get('issuer'):
                    print(f"  Issued By: {cert['issuer']['name']} ({cert['issuer']['email']}) - {cert['issuer']['role']}")
                print(f"  Blockchain Status: {cert['blockchain_status']}")
                print(f"  PDF: {cert['pdf_url']}")
        
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None


def get_institution_by_user_email(email: str, include_certificates: bool = True, limit: int = 100):
    """
    Get institution details by user email (e.g., Mumbai University SE ID)
    
    Args:
        email: Email of the institution admin or sub-admin
        include_certificates: Whether to include certificate details
        limit: Maximum number of certificates to return
    """
    url = f"{BASE_URL}/universities/user/{email}/institution-details"
    params = {
        "include_certificates": include_certificates,
        "limit_certificates": limit
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print("=" * 80)
        print(f"ACCESSING VIA USER EMAIL: {email}")
        print("=" * 80)
        return get_institution_by_id(data['institution']['id'], include_certificates, limit)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None


# Example Usage:
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Access by Institution ID")
    print("=" * 80)
    
    # Example institution ID (replace with actual ID)
    institution_id = "69199937d07e4f5df10b518d"
    get_institution_by_id(institution_id, include_certificates=True, limit=10)
    
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Access by Mumbai University SE ID (User Email)")
    print("=" * 80)
    
    # Example: Mumbai University SE ID email
    mumbai_univ_email = "wejosi2543@kudimi.com"
    get_institution_by_user_email(mumbai_univ_email, include_certificates=True, limit=10)
    
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: Get Only Sub-Admin Details (No Certificates)")
    print("=" * 80)
    
    get_institution_by_user_email(mumbai_univ_email, include_certificates=False)
