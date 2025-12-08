# Quick Reference: Institution Details API

## 🚀 Quick Start

### Access via Mumbai University SE ID (Email)
```bash
GET /universities/user/{email}/institution-details
```

**Example:**
```bash
curl "http://localhost:8000/universities/user/wejosi2543@kudimi.com/institution-details"
```

### Access via Institution ID
```bash
GET /universities/institution/{institution_id}/details
```

**Example:**
```bash
curl "http://localhost:8000/universities/institution/69199937d07e4f5df10b518d/details"
```

---

## 📊 What You Get

When you access through Mumbai University SE ID, you get:

### 1. Institution Information
- Name, Email, Address, Type
- Creation and update timestamps

### 2. Statistics
- Total number of sub-admins
- Total number of regular users
- Total certificates issued
- Certificates shown in response

### 3. Sub-Admin Details ✅
- Full name, email, username
- Role (ADMIN, SUBADMIN, INSTITUTION_ADMIN)
- Active status
- Additional metadata
- User ID and creation date

### 4. All Certificates ✅
- Certificate ID and student details
- Course, department, roll number
- CGPA and passing year
- **Issuer information** (which sub-admin issued it)
- PDF download link
- Verification URL
- Blockchain status
- Issue date and status

---

## 🎯 Common Use Cases

### Use Case 1: View All Sub-Admins
```bash
curl "http://localhost:8000/universities/user/wejosi2543@kudimi.com/institution-details?include_certificates=false"
```
**Result:** Only institution info and sub-admin list (fast)

### Use Case 2: View All Certificates with Issuers
```bash
curl "http://localhost:8000/universities/user/wejosi2543@kudimi.com/institution-details?include_certificates=true&limit_certificates=100"
```
**Result:** Full details including up to 100 certificates with issuer info

### Use Case 3: Quick Statistics
```bash
curl "http://localhost:8000/universities/user/wejosi2543@kudimi.com/institution-details?include_certificates=false"
```
**Result:** Get counts without loading all certificate data

---

## 🐍 Python Example

```python
import requests

# Setup
BASE_URL = "http://localhost:8000"
email = "wejosi2543@kudimi.com"

# Get all details
response = requests.get(
    f"{BASE_URL}/universities/user/{email}/institution-details",
    params={
        "include_certificates": True,
        "limit_certificates": 50
    }
)

data = response.json()

# Print summary
print(f"Institution: {data['institution']['name']}")
print(f"Sub-Admins: {data['statistics']['total_sub_admins']}")
print(f"Certificates: {data['statistics']['total_certificates_issued']}")

# List all sub-admins
print("\nSub-Admins:")
for admin in data['sub_admins']:
    print(f"  • {admin['name']} ({admin['email']}) - {admin['role']}")

# Show certificates with issuers
print("\nRecent Certificates:")
for cert in data['certificates'][:5]:
    print(f"  {cert['certificate_id']}: {cert['student_name']}")
    if cert['issuer']:
        print(f"    Issued by: {cert['issuer']['name']}")
```

---

## 📋 Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_certificates` | boolean | true | Include certificate details in response |
| `limit_certificates` | integer | 100 | Maximum number of certificates to return |

---

## ✅ Response Fields

### Institution
- `id`, `name`, `email`, `address`, `type`
- `created_at`, `updated_at`

### Statistics
- `total_sub_admins` - Count of all admins
- `total_regular_users` - Count of regular users
- `total_certificates_issued` - Total certificates
- `certificates_shown` - Certificates in this response

### Sub-Admin
- `id`, `name`, `email`, `username`
- `role` - ADMIN, SUBADMIN, INSTITUTION_ADMIN
- `is_active` - Account status
- `created_at` - When account was created
- `meta` - Additional metadata

### Certificate
- `certificate_id` - Unique ID
- `student_name`, `course`, `department`
- `roll_number`, `registration_number`
- `cgpa`, `passing_year`
- `issue_date`, `status`
- `pdf_url` - Download certificate
- `verification_url` - Verify authenticity
- **`issuer`** - Who issued it:
  - `id`, `name`, `email`, `role`
- `blockchain_status` - PENDING/ANCHORED
- `template_name` - Certificate template

---

## 🔧 Testing

Run these scripts to test:

```bash
# Check data structure
python check_cert_structure.py

# Test institution details
python test_institution_details.py

# Test with MMMUT data
python test_mmmut_details.py

# Run example API calls
python example_institution_api.py
```

---

## 📚 Full Documentation

- **Complete API Docs**: `INSTITUTION_API_DOCS.md`
- **Implementation Details**: `INSTITUTION_FEATURE_SUMMARY.md`
- **Code Examples**: `example_institution_api.py`

---

## 💡 Key Points

1. ✅ **Shows ALL sub-admins** linked to the institution
2. ✅ **Shows ALL certificates** issued by sub-admins
3. ✅ **Includes issuer details** for each certificate
4. ✅ **Accessible via email** (Mumbai University SE ID)
5. ✅ **Configurable response size** with limit parameter
6. ✅ **Fast statistics** when certificates not needed

---

## 🎉 Features Added

- Track which sub-admin issued each certificate
- View all sub-admins in one place
- Filter certificates by institution
- Access via user email or institution ID
- Comprehensive institution analytics
- Issuer accountability and tracking
