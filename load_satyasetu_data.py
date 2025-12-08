"""
Satyasetu Knowledge Base Loader
This script loads Satyasetu-specific knowledge into the knowledge base
"""

from app.services.rag_service import rag_service
from app.core.database import SessionLocal, init_db
from app.models.university import University
import json


def load_satyasetu_knowledge():
    """Load Satyasetu-specific knowledge."""
    
    documents = [
        # About Satyasetu
        """About Satyasetu - The Trust Layer for Academic Credentials

Satyasetu is a blockchain-powered platform for issuing, storing, and verifying academic credentials. It provides instant verification of educational documents with zero fraud and complete transparency.

Key Features:
- Issue tamper-proof digital certificates with blockchain-grade encryption
- Instant verification in 2 seconds
- AI-powered certificate detection with 98.7% accuracy
- Blockchain-backed immutable records on Polygon network
- Privacy-first and purpose-built for modern institutions

The platform connects three key stakeholders:
1. Institutions (Universities & Organizations) - Issue verified credentials
2. Credential Holders (Students & Professionals) - Store and share credentials
3. Verifiers (HR Teams & Recruiters) - Verify credentials instantly
""",

        # Hindi version
        """सत्यसेतु के बारे में - शैक्षिक प्रमाणपत्रों के लिए विश्वास परत

सत्यसेतु एक ब्लॉकचेन-संचालित प्लेटफ़ॉर्म है जो शैक्षिक प्रमाणपत्रों को जारी करने, संग्रहीत करने और सत्यापित करने के लिए है। यह शून्य धोखाधड़ी और पूर्ण पारदर्शिता के साथ शैक्षिक दस्तावेज़ों का तत्काल सत्यापन प्रदान करता है।

मुख्य विशेषताएं:
- ब्लॉकचेन-ग्रेड एन्क्रिप्शन के साथ छेड़छाड़-रोधी डिजिटल प्रमाणपत्र जारी करें
- 2 सेकंड में तत्काल सत्यापन
- 98.7% सटीकता के साथ AI-संचालित प्रमाणपत्र पहचान
- पॉलीगॉन नेटवर्क पर ब्लॉकचेन-समर्थित अपरिवर्तनीय रिकॉर्ड
- गोपनीयता-प्रथम और आधुनिक संस्थानों के लिए विशेष रूप से निर्मित
""",

        # Platform Features
        """Satyasetu Platform Features - Complete Security Suite

1. CRYPTOGRAPHIC FINGERPRINT
   - SHA-256 Hash embedded in every certificate
   - Unique hash for offline verification
   - Embedded directly in PDF
   - Works without internet connection

2. BLOCKCHAIN ANCHORING
   - Immutably recorded on Polygon Network
   - Public verification on Sepolia testnet
   - Contract address: 0xe01434dafeba7fff90463ced6a228023fb8963e9
   - Permanent proof that can never be altered or deleted
   - 12-second blockchain confirmation

3. AI CERTIFICATE DETECTION
   - Vision Model v2.1 with 98.7% accuracy
   - Signature Authenticity: 98% detection
   - Watermark Check: 100% verification
   - Metadata Integrity: 95% analysis
   - OCR Analysis: 99% accuracy
   - Automated fraud detection

4. RSA DIGITAL SIGNATURES
   - 2048-bit RSA-PSS encryption
   - Mathematically unforgeable signatures
   - Signature strength validation
   - Industry-standard cryptographic protection
   - AES-256 encryption for data security

5. REAL-TIME VERIFICATION
   - 2-second verification time
   - 100% uptime guarantee
   - Unique verification URL for each certificate
   - Scan QR code or type ID
   - Audit-grade logs maintained
""",

        # How it Works - Workflow
        """Satyasetu Certificate Issuance Workflow - 5 Simple Steps

STEP 1: Upload Your Roster
- Drop a CSV, connect your SIS, or paste a list
- Auto-map fields for easy integration
- Highlights anything needing attention
- Supports CSV, XLSX, and API integration
- Processing time: Under 120 seconds

STEP 2: Generate Tamper-Proof PDFs
- One-click certificate generation
- Renders with your brand system, signatures, and seals
- QR verification marks embedded
- RSA-SHA256 digitally signed
- AES-256 encryption applied

STEP 3: Anchor on Blockchain
- Certificate hash recorded on Polygon blockchain
- Creates immutable, publicly verifiable proof
- Permanent record that cannot be altered
- Blockchain verification in 12 seconds
- Viewable on Sepolia testnet

STEP 4: Distribute Instantly
- Students receive branded emails
- Wallet-ready links provided
- Multiple download options
- Track opens, clicks, and resends
- Email + SMS delivery
- Webhook callbacks available

STEP 5: Instant Verification
- Unique verification URL for each certificate
- HR teams can type, scan, or upload
- Confirms instantly with blockchain-backed proof
- Blockchain verified badge
- Audit-grade logs maintained
- Works forever - no expiration
""",

        # Problem & Solution
        """The Problem Satyasetu Solves

PROBLEMS IN TRADITIONAL VERIFICATION:

1. HR Challenges:
   - HR teams waste hours calling universities
   - Manual verification takes 3 weeks or more
   - Difficult to verify international credentials
   - No standardized verification process

2. Fraud Issues:
   - Candidates submit fake PDFs
   - Easy to manipulate digital documents
   - Difficult to detect sophisticated forgeries
   - Trust deficit between stakeholders

3. Cost & Time:
   - ₹5,000+ courier costs for document verification
   - 60-day embassy wait times
   - Manual PDF edits required
   - Slow bulk credential issuance

SATYASETU SOLUTION:

✓ Instant Verification: 2 seconds instead of weeks
✓ Zero Fraud: Blockchain-backed immutable proof
✓ Complete Transparency: Public verification available
✓ Cost Effective: No courier or manual processing costs
✓ Bulk Operations: 500 certificates in 30 seconds
✓ Forever Accessible: Permanent blockchain records
✓ AI Detection: 98.7% accuracy in fraud detection
✓ 100% Uptime: Always available for verification
""",

        # Use Cases
        """Satyasetu Use Cases - Real World Applications

USE CASE 1: MASS HIRING WEEK
Scenario: Corporate HR clearing 500 shortlisted candidates

BEFORE Satyasetu:
- Three weeks chasing registrar offices
- Manual phone calls to universities
- Paper-based verification
- High risk of fake credentials

AFTER Satyasetu:
- Instant verification of all 500 candidates
- 2 seconds per credential
- Blockchain-backed proof
- Zero fraud detected

USE CASE 2: GLOBAL STUDY PACK
Scenario: Graduate bundling transcripts for visa & university applications

BEFORE Satyasetu:
- ₹5,000 courier cost
- 60-day embassy wait
- Multiple document copies needed
- Risk of document loss

AFTER Satyasetu:
- Digital wallet-ready credentials
- Instant sharing with universities
- Zero courier costs
- Permanent blockchain storage

USE CASE 3: SKILL BADGE DROP
Scenario: Partner academy shipping 10K micro-credentials

BEFORE Satyasetu:
- Manual PDF edits required
- Zip file uploads for each batch
- Slow processing time
- Difficult to verify authenticity

AFTER Satyasetu:
- 30 seconds for bulk issuance
- Automated generation from CSV
- Instant blockchain anchoring
- Built-in verification system

USE CASE 4: UNIVERSITY CREDENTIAL MANAGEMENT
- Design certificates in minutes (upload logo, choose layout)
- Issue in bulk (500 certificates in 30 seconds)
- Verify instantly (anyone can verify in 2 seconds)
- No designer needed
- MoE (Ministry of Education) integration
""",

        # Technical Security Details
        """Satyasetu Technical Security Architecture

LAYER 1: CRYPTOGRAPHIC PROTECTION
- SHA-256 Hash Generation
  * Unique hash for each certificate
  * Embedded in PDF metadata
  * Offline verification capable
  * Collision-resistant algorithm

- RSA-PSS Digital Signatures
  * 2048-bit key strength
  * Mathematically unforgeable
  * Industry-standard algorithm
  * Private key security

- AES-256 Encryption
  * Data encryption at rest
  * Secure transmission
  * End-to-end protection

LAYER 2: BLOCKCHAIN IMMUTABILITY
- Polygon Network Integration
  * Low transaction costs
  * Fast confirmation (12 seconds)
  * Environmentally friendly PoS
  * Ethereum compatibility

- Smart Contract Verification
  * Public contract address
  * Viewable on Sepolia testnet
  * Immutable record storage
  * Transparent verification

- Hash Anchoring
  * Certificate hash stored on-chain
  * Timestamped proof
  * Cannot be altered or deleted
  * Public audit trail

LAYER 3: AI FRAUD DETECTION
- Vision Model v2.1
  * 98.7% overall accuracy
  * Deep learning algorithms
  * Continuous model improvement

- Multi-Factor Analysis
  * Signature authenticity (98%)
  * Watermark verification (100%)
  * Metadata integrity (95%)
  * OCR text analysis (99%)

- Pattern Recognition
  * Detects known forgery techniques
  * Compares with genuine samples
  * Anomaly detection
  * Real-time fraud alerts

LAYER 4: VERIFICATION INFRASTRUCTURE
- 100% Uptime Guarantee
  * Redundant servers
  * Load balancing
  * DDoS protection
  * Automatic failover

- Multiple Verification Methods
  * QR code scanning
  * URL verification
  * Certificate ID lookup
  * File upload verification

- Audit Trail
  * Every verification logged
  * Timestamp records
  * IP tracking
  * Export capabilities
""",

        # Ministry of Education Integration
        """Satyasetu Ministry of Education (MoE) Integration

GOVERNMENT INTEGRATION:
- Ministry of Education data integration
- Compliance with Indian education standards
- UGC (University Grants Commission) recognized
- AICTE (All India Council for Technical Education) compatible
- National Academic Depository (NAD) alignment

FEATURES:
✓ MoE Insights Integration: Direct connection to government databases
✓ Regulatory Compliance: Meets all educational verification standards
✓ Standardized Format: Follows MoE guidelines for digital credentials
✓ Data Security: Government-grade security protocols
✓ Interoperability: Works with existing government systems

BENEFITS FOR INSTITUTIONS:
- Simplified compliance reporting
- Reduced administrative burden
- Government-recognized credentials
- Streamlined accreditation process
- Direct data submission to MoE
""",

        # Platform Benefits
        """Satyasetu Platform Benefits - Measurable Impact

REAL NUMBERS & IMPACT:

📊 Hours Saved:
- Eliminated manual verification time
- From 3 weeks to 2 seconds
- Bulk processing: 500 certificates in 30 seconds
- Automated workflow reduces admin work by 90%

🛡️ Fraud Prevention:
- Zero fraudulent claims accepted
- 98.7% AI detection accuracy
- Blockchain-backed immutability
- Every certificate cryptographically verified
- Mathematical proof of authenticity

🏛️ MoE Insights:
- Integrated with government data
- Real-time education database access
- Regulatory compliance built-in
- Standardized credential format

⚡ 100% Uptime:
- Always available for verification
- Redundant infrastructure
- 24/7 accessibility
- Never lose access to credentials

💰 Cost Savings:
- Eliminate ₹5,000+ courier costs
- No paper or printing expenses
- Reduce administrative overhead
- Scale without additional cost

🌐 Global Accessibility:
- Works from anywhere
- Multiple language support
- International standard compliance
- Cross-border verification
""",

        # Verification Process
        """How to Verify Credentials on Satyasetu

VERIFICATION METHODS:

Method 1: QR Code Scanning
1. Open certificate PDF
2. Locate QR code on certificate
3. Scan with smartphone camera
4. Instant verification result displayed
5. View blockchain proof

Method 2: Certificate ID Verification
1. Visit satyasetu.live/verify
2. Enter unique certificate ID
3. Click verify button
4. See complete verification details
5. Check blockchain timestamp

Method 3: File Upload Verification
1. Go to verification portal
2. Upload PDF certificate
3. AI analyzes document authenticity
4. Cryptographic hash checked
5. Blockchain anchor verified
6. Comprehensive report generated

VERIFICATION RESULTS INCLUDE:
✓ Certificate Status (Valid/Invalid)
✓ Issuing Institution
✓ Issue Date and Blockchain Timestamp
✓ Recipient Details
✓ Blockchain Transaction Hash
✓ AI Authenticity Score
✓ Digital Signature Verification
✓ Tamper Detection Report

VERIFICATION TIME: 2 seconds
ACCURACY: 100% for blockchain-verified certificates
AVAILABILITY: 24/7/365
COST: Free for verifiers
""",

        # For HR Teams & Recruiters
        """Satyasetu for HR Teams and Recruiters - Streamlined Hiring

WHY HR TEAMS CHOOSE SATYASETU:

⚡ INSTANT VERIFICATION
- Verify 500+ candidates in minutes
- 2-second verification per credential
- No phone calls to universities needed
- Eliminate 3-week waiting periods

🔒 ZERO FRAUD RISK
- Blockchain-backed authenticity
- AI detection catches sophisticated fakes
- Mathematical proof of credential validity
- Complete audit trail maintained

📊 BULK VERIFICATION
- Upload candidate list (CSV/Excel)
- Batch verification processing
- Automated fraud flagging
- Export verification reports

💼 HIRING CONFIDENCE
- Make faster hiring decisions
- Reduce candidate drop-off
- Improve candidate experience
- Legal compliance maintained

📈 AUDIT & COMPLIANCE
- Complete verification logs
- Export for compliance audits
- Timestamp records
- Meets industry standards

INTEGRATION OPTIONS:
- API for ATS (Applicant Tracking Systems)
- Webhook callbacks for automation
- CSV bulk upload
- Manual verification portal

TYPICAL WORKFLOW:
1. Candidate submits Satyasetu certificate
2. HR scans QR or enters ID
3. Instant verification result
4. Make hiring decision
5. Archive verification proof
"""
    ]
    
    metadatas = [
        {"category": "about", "language": "en", "topic": "platform_overview"},
        {"category": "about", "language": "hi", "topic": "platform_overview"},
        {"category": "features", "language": "en", "topic": "security_features"},
        {"category": "workflow", "language": "en", "topic": "issuance_process"},
        {"category": "problems", "language": "en", "topic": "problem_solution"},
        {"category": "use_cases", "language": "en", "topic": "real_world_applications"},
        {"category": "technical", "language": "en", "topic": "security_architecture"},
        {"category": "government", "language": "en", "topic": "moe_integration"},
        {"category": "benefits", "language": "en", "topic": "measurable_impact"},
        {"category": "verification", "language": "en", "topic": "how_to_verify"},
        {"category": "hr", "language": "en", "topic": "hiring_solutions"}
    ]
    
    ids = [f"satyasetu_{i}" for i in range(len(documents))]
    
    print("Loading Satyasetu knowledge into database...")
    rag_service.add_documents(documents, metadatas, ids)
    print(f"✓ Successfully loaded {len(documents)} Satyasetu-specific documents")


def load_sample_universities():
    """Load sample university data."""
    
    init_db()
    db = SessionLocal()
    
    # Clear existing universities
    db.query(University).delete()
    
    universities = [
        {
            "name": "University of Delhi",
            "code": "DU",
            "location": "Delhi",
            "state": "Delhi",
            "verification_url": "https://www.du.ac.in/",
            "verification_method": json.dumps({
                "satyasetu_enabled": True,
                "online_portal": True,
                "blockchain_verified": True,
                "email": "verification@du.ac.in",
                "phone": "+91-11-27667725"
            }),
            "common_forgery_patterns": json.dumps([
                "Fake seal impressions",
                "Incorrect university logo",
                "Modified registration numbers",
                "Use Satyasetu for instant verification"
            ])
        },
        {
            "name": "University of Mumbai",
            "code": "MU",
            "location": "Mumbai",
            "state": "Maharashtra",
            "verification_url": "https://www.mu.ac.in/",
            "verification_method": json.dumps({
                "satyasetu_enabled": True,
                "online_portal": True,
                "blockchain_verified": True,
                "verification_page": "https://verification.mu.ac.in"
            }),
            "common_forgery_patterns": json.dumps([
                "Poor quality paper",
                "Incorrect font styles",
                "Missing hologram",
                "Verify via Satyasetu blockchain"
            ])
        },
        {
            "name": "Indian Institute of Technology Delhi",
            "code": "IITD",
            "location": "New Delhi",
            "state": "Delhi",
            "verification_url": "https://www.iitd.ac.in/",
            "verification_method": json.dumps({
                "satyasetu_enabled": True,
                "blockchain_verified": True,
                "digital_verification": True,
                "instant_verify": True
            }),
            "common_forgery_patterns": json.dumps([
                "Blockchain verification required",
                "Satyasetu QR code verification"
            ])
        }
    ]
    
    print("Loading university data...")
    for uni_data in universities:
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
        load_satyasetu_knowledge()
        load_sample_universities()
        
        print("\n" + "=" * 60)
        print("✓ All Satyasetu data loaded successfully!")
        print("=" * 60)
        print("\nYour chatbot now knows about:")
        print("  • Satyasetu platform features")
        print("  • Blockchain verification process")
        print("  • AI fraud detection")
        print("  • Certificate issuance workflow")
        print("  • Use cases and benefits")
        print("  • How to verify credentials")
        print("  • HR team solutions")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error loading data: {e}")
        import traceback
        traceback.print_exc()
