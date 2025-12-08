# Satyasetu Chatbot API

A **100% FREE** RAG-based bilingual (English/Hindi) chatbot API for educational document forgery detection. Built to deploy on Railway's free tier.

## 🚀 Features

- ✅ **Bilingual Support**: English & Hindi with automatic language detection
- ✅ **RAG (Retrieval Augmented Generation)**: Uses ChromaDB for knowledge base
- ✅ **Free LLM**: Groq API (free tier with fast inference)
- ✅ **User Authentication**: JWT-based auth with user sessions
- ✅ **Conversation History**: Saves all user chats like ChatGPT
- ✅ **University Database**: Multi-university document verification info
- ✅ **REST API**: Easy integration with any frontend/mobile app
- ✅ **Railway Ready**: Configured for Railway deployment

## 🛠️ Tech Stack (100% Free)

| Component | Technology | Cost |
|-----------|-----------|------|
| Backend | FastAPI | Free |
| Database | SQLite (embedded) | Free |
| Vector DB | ChromaDB (embedded) | Free |
| LLM | Groq API | Free |
| Embeddings | sentence-transformers | Free |
| Translation | IndicTrans2 | Free |
| Hosting | Railway | Free tier |

## 📁 Project Structure

```
satyasetu-chatbot/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication
│   │   ├── chat.py       # Chat endpoints
│   │   ├── universities.py
│   │   └── knowledge.py
│   ├── core/             # Core configurations
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/           # Database models
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── university.py
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   │   ├── llm_service.py
│   │   ├── rag_service.py
│   │   ├── translation_service.py
│   │   └── university_service.py
│   └── main.py           # FastAPI application
├── load_sample_data.py   # Sample data loader
├── requirements.txt
├── Procfile             # Railway config
├── railway.json
└── .env.example
```

## 🔧 Local Setup

### 1. Clone & Install

```powershell
cd e:\chatbotsr
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update:

```env
# Get free Groq API key from: https://console.groq.com
GROQ_API_KEY=your-groq-api-key-here

# Generate secret key
SECRET_KEY=your-secret-key-here

# For local testing
DATABASE_URL=sqlite:///./satyasetu.db
```

### 3. Load Sample Data

```powershell
python load_sample_data.py
```

### 4. Run Locally

```powershell
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs for API documentation

## 🚂 Railway Deployment

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (free)

### Step 2: Create New Project
1. Click "New Project"
2. Choose "Deploy from GitHub repo"
3. Connect your GitHub account and select this repo

### Step 3: Configure Environment Variables
Add these in Railway Settings → Variables:
```
GROQ_API_KEY=your-groq-api-key
SECRET_KEY=generate-using-openssl-rand-hex-32
CORS_ORIGINS=["https://your-frontend.com"]
```

### Step 4: Add Volume for Database Persistence
1. In Railway Settings → "Volumes"
2. Add volume: Mount path = `/app/data`
3. This ensures SQLite database persists across deployments

### Step 5: Deploy
- Railway will auto-deploy on every push to main branch
- Get your API URL from Railway dashboard

## 📚 API Usage

### 1. Register User
```bash
POST /auth/register
{
  "email": "user@example.com",
  "username": "testuser",
  "password": "securepass123",
  "full_name": "Test User"
}
```

### 2. Login
```bash
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

Returns: `{ "access_token": "...", "token_type": "bearer" }`

### 3. Chat (English)
```bash
POST /chat/
Headers: Authorization: Bearer <token>
{
  "message": "How to detect forged degrees?",
  "language": "en"
}
```

### 4. Chat (Hindi)
```bash
POST /chat/
Headers: Authorization: Bearer <token>
{
  "message": "नकली डिग्री की पहचान कैसे करें?",
  "language": "hi"
}
```

### 5. Get Conversation History
```bash
GET /chat/conversations
Headers: Authorization: Bearer <token>
```

### 6. Search Universities
```bash
GET /universities?query=delhi
```

### 7. Get University Verification Info
```bash
GET /universities/1/verification/degree
```

## 🔌 Frontend Integration Examples

### React/Next.js
```javascript
const API_URL = "https://your-railway-app.up.railway.app";

// Login
const login = async (email, password) => {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await res.json();
  localStorage.setItem('token', data.access_token);
};

// Chat
const sendMessage = async (message, language = 'en') => {
  const token = localStorage.getItem('token');
  const res = await fetch(`${API_URL}/chat/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ message, language })
  });
  return await res.json();
};
```

### Mobile App (React Native)
```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';

const chat = async (message) => {
  const token = await AsyncStorage.getItem('token');
  const response = await fetch(`${API_URL}/chat/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message })
  });
  return await response.json();
};
```

## 🎓 Add Your Training Data

### Method 1: Using API
```python
import requests

token = "your-jwt-token"
documents = [
    "Your forgery detection knowledge here...",
    "More information about document verification..."
]

response = requests.post(
    "https://your-app.railway.app/knowledge/upload",
    headers={"Authorization": f"Bearer {token}"},
    data={
        "documents": documents,
        "metadatas": '[{"category": "custom"}]'
    }
)
```

### Method 2: Update load_sample_data.py
Add your custom knowledge to the `documents` list and run:
```powershell
python load_sample_data.py
```

## 🏢 Multi-University Support

Each user can query university-specific information:

```python
# Query with university context
{
  "message": "What are the security features in DU degrees?",
  "university_id": 1  # University of Delhi
}
```

## 🌐 Bilingual Feature

The chatbot automatically:
1. Detects input language (en/hi)
2. Retrieves relevant context in any language
3. Responds in the user's language
4. Maintains conversation history with language tags

## 🔒 Security Features

- JWT token authentication
- Password hashing (bcrypt)
- CORS protection
- Rate limiting ready
- SQL injection protection (SQLAlchemy ORM)

## 📊 Free Tier Limits

| Service | Free Limit |
|---------|------------|
| Railway | 500 hours/month, 512MB RAM, 1GB volume |
| Groq API | 30 requests/minute |
| SQLite | Unlimited (embedded) |
| ChromaDB | Unlimited (embedded) |

## 🚀 Performance Tips

1. **Railway**: Use persistent volume for ChromaDB
2. **Groq**: Cache frequently asked questions
3. **Database**: Index commonly queried fields
4. **Embeddings**: Use smaller models for faster inference

## 🤝 Contributing

Add more university data, improve translations, or enhance RAG accuracy!

## 📄 License

MIT License - Free to use and modify

## 🆘 Support

For issues or questions about Satyasetu chatbot, create an issue in the repo.

---

**Built with ❤️ for educational document verification in India**
