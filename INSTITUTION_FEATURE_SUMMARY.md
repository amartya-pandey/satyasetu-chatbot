# Institution Details Feature - Implementation Summary

## Overview
This feature allows accessing comprehensive institution details through a Mumbai University SE ID (or any institution admin email), showing all sub-admin details and certificates issued by sub-admins attached to the institution.

## What Was Implemented

### 1. Updated Data Models (`app/models/mongo_models.py`)

#### User Model Enhancements:
- Added `meta` field to store additional metadata (institution name, department, etc.)
- Updated role field to include 'SUBADMIN' role type

#### Certificate Model Enhancements:
- Added `institution_id` field to link certificates to institutions
- Added `issuer_id` field to track which sub-admin issued each certificate

### 2. New API Endpoints (`app/api/universities.py`)

#### Endpoint 1: Get Institution Details by ID
```
GET /universities/institution/{institution_id}/details
```
**Query Parameters:**
- `include_certificates`: Boolean (default: true)
- `limit_certificates`: Integer (default: 100)

**Returns:**
- Institution basic information
- Statistics (total sub-admins, users, certificates)
- List of all sub-admins with details
- List of regular users
- List of certificates with issuer information

#### Endpoint 2: Get Institution Details by User Email
```
GET /universities/user/{user_email}/institution-details
```
**Query Parameters:**
- `include_certificates`: Boolean (default: true)
- `limit_certificates`: Integer (default: 100)

**Returns:** Same as Endpoint 1, but accessed via user email

**Use Case:** Access institution data using Mumbai University SE ID email

### 3. Response Structure

```json
{
  "institution": {
    "id": "...",
    "name": "Institute Name",
    "email": "...",
    "address": "...",
    "type": "...",
    "created_at": "...",
    "updated_at": "..."
  },
  "statistics": {
    "total_sub_admins": 5,
    "total_regular_users": 120,
    "total_certificates_issued": 250,
    "certificates_shown": 50
  },
  "sub_admins": [
    {
      "id": "...",
      "name": "Admin Name",
      "email": "admin@example.com",
      "username": "...",
      "role": "INSTITUTION_ADMIN",
      "created_at": "...",
      "is_active": true,
      "meta": {...}
    }
  ],
  "regular_users": [...],
  "certificates": [
    {
      "certificate_id": "SATYA-2025-...",
      "student_name": "Student Name",
      "course": "BTech",
      "department": "CSE",
      "roll_number": "...",
      "registration_number": "...",
      "cgpa": 9.2,
      "passing_year": 2028,
      "issue_date": "...",
      "status": "ISSUED",
      "pdf_url": "...",
      "verification_url": "...",
      "issuer": {
        "id": "...",
        "name": "Issuer Name",
        "email": "issuer@example.com",
        "role": "INSTITUTION_ADMIN"
      },
      "blockchain_status": "ANCHORED",
      "created_at": "...",
      "template_name": "..."
    }
  ]
}
```

## Key Features

1. **Sub-Admin Tracking**: Shows all administrators and sub-admins linked to an institution
2. **Certificate Tracking**: Displays all certificates issued by the institution
3. **Issuer Information**: Each certificate includes details about who issued it
4. **Flexible Access**: Can access by institution ID or by user email
5. **Configurable Response**: Option to include/exclude certificates and limit response size
6. **Comprehensive Statistics**: Quick overview of institution metrics

## Files Created/Modified

### Modified Files:
1. `app/models/mongo_models.py` - Updated User and Certificate models
2. `app/api/universities.py` - Added new endpoints

### New Files:
1. `INSTITUTION_API_DOCS.md` - Comprehensive API documentation
2. `example_institution_api.py` - Example usage script
3. `test_institution_details.py` - Test script for data validation
4. `test_mmmut_details.py` - Test script for MMMUT institution
5. `check_cert_structure.py` - Certificate structure verification

## Usage Examples

### Example 1: Access via Mumbai University SE ID
```bash
curl -X GET "http://localhost:8000/universities/user/wejosi2543@kudimi.com/institution-details?include_certificates=true&limit_certificates=100"
```

### Example 2: Access via Institution ID
```bash
curl -X GET "http://localhost:8000/universities/institution/69199937d07e4f5df10b518d/details?include_certificates=true&limit_certificates=50"
```

### Example 3: Get only Sub-Admin details (no certificates)
```bash
curl -X GET "http://localhost:8000/universities/user/wejosi2543@kudimi.com/institution-details?include_certificates=false"
```

## Python Client Example

```python
import requests

# Access via Mumbai University SE ID
email = "wejosi2543@kudimi.com"
url = f"http://localhost:8000/universities/user/{email}/institution-details"

response = requests.get(url, params={
    "include_certificates": True,
    "limit_certificates": 100
})

data = response.json()

# Access institution details
print(f"Institution: {data['institution']['name']}")
print(f"Total Sub-Admins: {data['statistics']['total_sub_admins']}")

# List all sub-admins
for admin in data['sub_admins']:
    print(f"Sub-Admin: {admin['name']} ({admin['email']})")

# List certificates with issuers
for cert in data['certificates']:
    print(f"Certificate: {cert['certificate_id']}")
    print(f"Issued by: {cert['issuer']['name']}")
```

## Testing

Test scripts have been created to verify:
1. Certificate structure in MongoDB
2. Institution details retrieval
3. Sub-admin listing
4. Certificate-to-issuer mapping

Run tests:
```bash
python test_institution_details.py
python test_mmmut_details.py
```

## Next Steps

### Recommended Enhancements:
1. **Authentication**: Add JWT authentication to protect endpoints
2. **Pagination**: Implement pagination for large certificate lists
3. **Filtering**: Add filters for certificates (by date, status, issuer, etc.)
4. **Caching**: Cache institution details for better performance
5. **Rate Limiting**: Add rate limiting for production
6. **Search**: Add search functionality for certificates and sub-admins
7. **Export**: Add CSV/Excel export for certificates
8. **Analytics**: Add analytics dashboard for certificate issuance trends

### Optional Features:
- Bulk certificate operations
- Certificate revocation tracking
- Sub-admin activity logs
- Email notifications for certificate issuance
- Certificate verification API

## Database Structure

### Collections Used:
1. **institutions** - Institution master data
2. **users** - All users including sub-admins
3. **certificates** - All issued certificates

### Key Relationships:
- `User.organization` → `Institution._id`
- `Certificate.institutionId` → `Institution._id`
- `Certificate.issuerId` → `User._id`

## Notes

1. The endpoints use MongoDB's native collection access for better performance with large datasets
2. Certificate issuer information is fetched in real-time to ensure accuracy
3. Response size can be controlled using the `limit_certificates` parameter
4. All dates are in ISO 8601 format
5. ObjectIds are converted to strings in the response for JSON compatibility

## Documentation

Complete API documentation is available in:
- `INSTITUTION_API_DOCS.md` - Full API reference
- `example_institution_api.py` - Working code examples

## Support

For issues or questions:
1. Check the API documentation in `INSTITUTION_API_DOCS.md`
2. Review example usage in `example_institution_api.py`
3. Run test scripts to verify data structure
