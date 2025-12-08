# Institution Details API Documentation

## Overview

This API provides comprehensive access to institution details including all sub-admins and certificates issued by the institution. When accessing through a Mumbai University SE ID (or any institution admin email), you can retrieve:

1. **Institution Information**: Basic details about the institution
2. **Sub-Admin Details**: All administrators and sub-admins linked to the institution
3. **Certificate Details**: All certificates issued by sub-admins attached to the institution

## Endpoints

### 1. Get Institution Details by ID

**Endpoint:** `GET /universities/institution/{institution_id}/details`

**Description:** Retrieve comprehensive institution details including sub-admins and certificates.

**Parameters:**
- `institution_id` (path, required): MongoDB ObjectId of the institution
- `include_certificates` (query, optional): Whether to include certificate details (default: true)
- `limit_certificates` (query, optional): Maximum number of certificates to return (default: 100)

**Example Request:**
```bash
GET http://localhost:8000/universities/institution/69199937d07e4f5df10b518d/details?include_certificates=true&limit_certificates=50
```

**Response Structure:**
```json
{
  "institution": {
    "id": "69199937d07e4f5df10b518d",
    "name": "MMMUT",
    "email": "mmmmut@example.com",
    "address": "Gorakhpur, UP",
    "type": "University",
    "created_at": "2024-11-17T09:06:34.450000",
    "updated_at": "2025-12-02T12:01:53.142000"
  },
  "statistics": {
    "total_sub_admins": 5,
    "total_regular_users": 120,
    "total_certificates_issued": 250,
    "certificates_shown": 50
  },
  "sub_admins": [
    {
      "id": "69199937d07e4f5df10b518b",
      "name": "MMMUT Admin",
      "email": "admin@mmmut.edu",
      "username": "mmmut_admin",
      "role": "INSTITUTION_ADMIN",
      "created_at": "2024-11-17T09:06:34.450000",
      "is_active": true,
      "meta": {
        "institutionName": "MMMUT",
        "department": "Admin"
      }
    }
  ],
  "regular_users": [
    {
      "id": "user123",
      "name": "John Doe",
      "email": "john@example.com",
      "username": "john_doe",
      "role": "USER",
      "created_at": "2024-11-17T09:06:34.450000",
      "is_active": true,
      "meta": {}
    }
  ],
  "certificates": [
    {
      "certificate_id": "SATYA-2025-591D6A",
      "student_name": "Anurag Banerjee",
      "course": "BTech",
      "department": "CSE",
      "roll_number": "2024021209",
      "registration_number": "REGIS123",
      "cgpa": 9.2,
      "passing_year": 2028,
      "issue_date": "2025-11-17T00:00:00",
      "status": "ISSUED",
      "pdf_url": "https://res.cloudinary.com/dzqtx9kms/raw/upload/...",
      "verification_url": "https://satya-setu.example.com/verify/SATYA-2025-591D6A",
      "issuer": {
        "id": "69199937d07e4f5df10b518b",
        "name": "MMMUT Admin",
        "email": "admin@mmmut.edu",
        "role": "INSTITUTION_ADMIN"
      },
      "blockchain_status": "ANCHORED",
      "created_at": "2025-11-17T09:06:34.450000",
      "template_name": "Default Template B — Ornate Certificate"
    }
  ]
}
```

---

### 2. Get Institution Details by User Email

**Endpoint:** `GET /universities/user/{user_email}/institution-details`

**Description:** Retrieve institution details using a user's email (e.g., Mumbai University SE ID). This is useful when you have the admin/sub-admin email and want to get all related institution data.

**Parameters:**
- `user_email` (path, required): Email of the institution admin or sub-admin
- `include_certificates` (query, optional): Whether to include certificate details (default: true)
- `limit_certificates` (query, optional): Maximum number of certificates to return (default: 100)

**Example Request:**
```bash
GET http://localhost:8000/universities/user/wejosi2543@kudimi.com/institution-details?include_certificates=true&limit_certificates=100
```

**Response Structure:** Same as endpoint #1

**Use Cases:**
- Access institution details via Mumbai University SE ID
- Get all sub-admins linked to the institution
- View all certificates issued by any sub-admin in the institution
- Track certificate issuance by specific sub-admins

---

## Response Fields Description

### Institution Object
- `id`: MongoDB ObjectId of the institution
- `name`: Name of the institution
- `email`: Contact email of the institution
- `address`: Physical address
- `type`: Type of institution (University, College, etc.)
- `created_at`: When the institution was created
- `updated_at`: Last update timestamp

### Statistics Object
- `total_sub_admins`: Total number of admins/sub-admins
- `total_regular_users`: Total number of regular users
- `total_certificates_issued`: Total certificates issued by the institution
- `certificates_shown`: Number of certificates in the current response (limited by `limit_certificates`)

### Sub-Admin Object
- `id`: User ID
- `name`: Full name
- `email`: Email address
- `username`: Username
- `role`: User role (ADMIN, SUBADMIN, INSTITUTION_ADMIN, etc.)
- `created_at`: Account creation date
- `is_active`: Whether the account is active
- `meta`: Additional metadata (institution name, department, etc.)

### Certificate Object
- `certificate_id`: Unique certificate identifier
- `student_name`: Name of the student
- `course`: Course name
- `department`: Department name
- `roll_number`: Student roll number
- `registration_number`: Student registration number
- `cgpa`: CGPA achieved
- `passing_year`: Year of passing
- `issue_date`: Date when certificate was issued
- `status`: Certificate status (ISSUED, PENDING, REVOKED)
- `pdf_url`: URL to download the certificate PDF
- `verification_url`: URL to verify the certificate
- `issuer`: Details of the person who issued the certificate
  - `id`: Issuer's user ID
  - `name`: Issuer's name
  - `email`: Issuer's email
  - `role`: Issuer's role
- `blockchain_status`: Blockchain anchoring status (PENDING, ANCHORED, FAILED)
- `created_at`: Certificate creation timestamp
- `template_name`: Name of the certificate template used

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid institution ID format"
}
```

### 404 Not Found
```json
{
  "detail": "Institution not found"
}
```
or
```json
{
  "detail": "User not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error fetching institution details: [error message]"
}
```

---

## Examples

### Example 1: Get all details for Mumbai University
```bash
curl -X GET "http://localhost:8000/universities/user/wejosi2543@kudimi.com/institution-details?include_certificates=true&limit_certificates=50"
```

### Example 2: Get only sub-admin details (no certificates)
```bash
curl -X GET "http://localhost:8000/universities/user/wejosi2543@kudimi.com/institution-details?include_certificates=false"
```

### Example 3: Get institution details by ID with limited certificates
```bash
curl -X GET "http://localhost:8000/universities/institution/69199937d07e4f5df10b518d/details?include_certificates=true&limit_certificates=10"
```

---

## Python Example

```python
import requests

# Access via user email (Mumbai University SE ID)
email = "wejosi2543@kudimi.com"
url = f"http://localhost:8000/universities/user/{email}/institution-details"
params = {
    "include_certificates": True,
    "limit_certificates": 100
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    # Print institution info
    print(f"Institution: {data['institution']['name']}")
    print(f"Total Sub-Admins: {data['statistics']['total_sub_admins']}")
    print(f"Total Certificates: {data['statistics']['total_certificates_issued']}")
    
    # List all sub-admins
    for admin in data['sub_admins']:
        print(f"Sub-Admin: {admin['name']} ({admin['email']}) - {admin['role']}")
    
    # List certificates with issuers
    for cert in data['certificates']:
        print(f"\nCertificate: {cert['certificate_id']}")
        print(f"Student: {cert['student_name']}")
        if cert.get('issuer'):
            print(f"Issued by: {cert['issuer']['name']} ({cert['issuer']['role']})")
```

---

## Notes

1. **Performance**: For large institutions with many certificates, use the `limit_certificates` parameter to control response size
2. **Pagination**: Currently not implemented. Consider implementing pagination for very large datasets
3. **Authentication**: Add authentication middleware if these endpoints should be protected
4. **Rate Limiting**: Consider adding rate limiting for production use
5. **Caching**: Consider caching institution details for frequently accessed institutions
