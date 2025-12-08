"""
Sample data loader for Satyasetu Knowledge Base
This script loads forgery detection knowledge into ChromaDB
"""

from app.services.rag_service import rag_service
from app.core.database import SessionLocal, init_db
from app.models.university import University
import json


def load_sample_knowledge():
    """Load sample forgery detection knowledge."""
    
    documents = [
        # General forgery detection
        """Educational Document Forgery Detection: Common Signs
        
        1. Paper Quality: Authentic degrees use high-quality paper with watermarks
        2. Seal and Stamp: Official embossed seals are difficult to forge
        3. Font Consistency: Check for consistent fonts and spacing
        4. Registration Numbers: Verify registration numbers with university databases
        5. Signature Analysis: Compare signatures with official records
        6. UV Light Test: Many authentic documents have UV-reactive elements
        7. Microprinting: Look for tiny text that's hard to reproduce
        8. Digital Verification: Many universities now provide online verification portals
        """,
        
        # Hindi version
        """शैक्षिक दस्तावेज़ जालसाजी की पहचान: सामान्य संकेत
        
        1. कागज़ की गुणवत्ता: असली डिग्री में उच्च गुणवत्ता का कागज़ और वॉटरमार्क होता है
        2. मोहर और स्टाम्प: आधिकारिक उभरी हुई मोहरें नकली बनाना मुश्किल होती हैं
        3. फ़ॉन्ट की स्थिरता: सुसंगत फ़ॉन्ट और स्पेसिंग की जांच करें
        4. पंजीकरण संख्या: विश्वविद्यालय डेटाबेस के साथ पंजीकरण संख्या सत्यापित करें
        5. हस्ताक्षर विश्लेषण: आधिकारिक रिकॉर्ड के साथ हस्ताक्षर की तुलना करें
        6. यूवी लाइट परीक्षण: कई प्रामाणिक दस्तावेज़ों में यूवी-प्रतिक्रियाशील तत्व होते हैं
        7. माइक्रोप्रिंटिंग: छोटे टेक्स्ट की तलाश करें जो पुनरुत्पादन करना कठिन है
        8. डिजिटल सत्यापन: कई विश्वविद्यालय अब ऑनलाइन सत्यापन पोर्टल प्रदान करते हैं
        """,
        
        # Degree verification process
        """Degree Verification Process:
        
        Step 1: Check University Accreditation
        - Verify the university is recognized by UGC/AICTE
        - Check if the university is listed on official education portals
        
        Step 2: Document Physical Inspection
        - Examine paper quality and texture
        - Check for embossed seals and holograms
        - Verify signature authenticity
        
        Step 3: Digital Verification
        - Use university's online verification portal
        - Match registration/enrollment numbers
        - Verify dates and grades
        
        Step 4: Cross-Reference
        - Contact university registrar's office
        - Request official transcript
        - Verify through National Academic Depository (NAD)
        """,
        
        # Marksheet verification
        """Marksheet Verification Guidelines:
        
        Authentic marksheets contain:
        - University logo and name
        - Student's photograph and signature
        - Roll number and registration number
        - Subject codes and marks
        - CGPA/percentage calculation
        - Controller of Examinations signature
        - Date of issue
        - Security features (watermark, hologram)
        
        Red flags:
        - Poor print quality
        - Spelling errors in university name
        - Incorrect seal or missing embossing
        - Suspicious modifications or overwriting
        - Inconsistent font styles
        """,
        
        # Common forgery techniques
        """Common Forgery Techniques in Educational Documents:
        
        1. Photocopy Manipulation: Scanning and editing original documents
        2. Template Forgery: Creating fake templates that mimic authentic ones
        3. Seal Forgery: Using fake rubber stamps or digital seals
        4. Data Alteration: Changing marks, grades, or dates
        5. Complete Fabrication: Creating documents from scratch
        6. Certificate Mills: Fake universities selling fraudulent degrees
        
        Detection Methods:
        - Compare with genuine samples
        - Use forensic document examination
        - Verify with issuing authority
        - Check digital signatures and QR codes
        - Use specialized forgery detection software
        """,
        
        # University-specific info
        """Indian Universities Document Verification:
        
        Major Universities and Verification Methods:
        
        1. University of Delhi: Online verification at du.ac.in
        2. Mumbai University: Verification portal at mu.ac.in
        3. Anna University: Digital verification system
        4. Jawaharlal Nehru University: Registrar office verification
        5. Savitribai Phule Pune University: Online verification portal
        
        National Academic Depository (NAD):
        - Central repository for academic awards
        - Digital verification of degrees and certificates
        - Available at nad.gov.in
        - Partner universities can upload digital certificates
        """,
        
        # Technical aspects
        """Technical Aspects of Document Forgery Detection:
        
        Digital Forensics:
        - Metadata analysis of scanned documents
        - Image manipulation detection
        - Font analysis and comparison
        - Color profile verification
        
        Physical Analysis:
        - Paper composition testing
        - Ink analysis
        - Printing method identification
        - Security feature examination
        
        AI/ML Based Detection:
        - Pattern recognition algorithms
        - Anomaly detection in document structure
        - Signature verification using computer vision
        - OCR-based text consistency checking
        """
    ]
    
    metadatas = [
        {"category": "general", "language": "en", "topic": "forgery_signs"},
        {"category": "general", "language": "hi", "topic": "forgery_signs"},
        {"category": "process", "language": "en", "topic": "degree_verification"},
        {"category": "process", "language": "en", "topic": "marksheet_verification"},
        {"category": "techniques", "language": "en", "topic": "forgery_methods"},
        {"category": "universities", "language": "en", "topic": "verification_portals"},
        {"category": "technical", "language": "en", "topic": "detection_methods"}
    ]
    
    ids = [f"doc_{i}" for i in range(len(documents))]
    
    print("Loading sample knowledge into ChromaDB...")
    rag_service.add_documents(documents, metadatas, ids)
    print(f"✓ Successfully loaded {len(documents)} documents")


def load_sample_universities():
    """Load sample university data."""
    
    init_db()
    db = SessionLocal()
    
    universities = [
        {
            "name": "University of Delhi",
            "code": "DU",
            "location": "Delhi",
            "state": "Delhi",
            "verification_url": "https://www.du.ac.in/",
            "verification_method": json.dumps({
                "online_portal": True,
                "email": "verification@du.ac.in",
                "phone": "+91-11-27667725"
            }),
            "common_forgery_patterns": json.dumps([
                "Fake seal impressions",
                "Incorrect university logo",
                "Modified registration numbers"
            ])
        },
        {
            "name": "University of Mumbai",
            "code": "MU",
            "location": "Mumbai",
            "state": "Maharashtra",
            "verification_url": "https://www.mu.ac.in/",
            "verification_method": json.dumps({
                "online_portal": True,
                "verification_page": "https://verification.mu.ac.in"
            }),
            "common_forgery_patterns": json.dumps([
                "Poor quality paper",
                "Incorrect font styles",
                "Missing hologram"
            ])
        },
        {
            "name": "Anna University",
            "code": "AU",
            "location": "Chennai",
            "state": "Tamil Nadu",
            "verification_url": "https://www.annauniv.edu/",
            "verification_method": json.dumps({
                "online_portal": True,
                "digital_verification": True
            }),
            "common_forgery_patterns": json.dumps([
                "Fake QR codes",
                "Altered grade information"
            ])
        }
    ]
    
    print("Loading sample universities...")
    for uni_data in universities:
        existing = db.query(University).filter(University.code == uni_data["code"]).first()
        if not existing:
            university = University(**uni_data)
            db.add(university)
    
    db.commit()
    print(f"✓ Successfully loaded {len(universities)} universities")
    db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Satyasetu Knowledge Base Loader")
    print("=" * 60)
    
    try:
        load_sample_knowledge()
        load_sample_universities()
        
        print("\n" + "=" * 60)
        print("✓ All sample data loaded successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error loading data: {e}")
