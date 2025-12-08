# Quick Start Guide - Satyasetu Chatbot

## 🎯 Goal
Deploy a free RAG-based bilingual chatbot for educational document forgery detection on Railway.

## ⚡ Quick Start (5 minutes)

### 1. Get Free Groq API Key
```
1. Visit: https://console.groq.com
2. Sign up (free)
3. Generate API key
4. Copy the key
```

### 2. Create .env File
```powershell
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```env
GROQ_API_KEY=gsk_your_key_here
SECRET_KEY=your-secret-key-change-this
```

### 3. Install Dependencies
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Load Sample Data
```powershell
python load_sample_data.py
```

### 5. Run Locally
```powershell
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

## 🧪 Test the API

### Test 1: Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"test123","full_name":"Test User"}'
```

### Test 2: Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

Copy the `access_token` from response.

### Test 3: Chat (English)
```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"message":"How to detect forged degrees?","language":"en"}'
```

### Test 4: Chat (Hindi)
```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"message":"नकली डिग्री की पहचान कैसे करें?","language":"hi"}'
```

## 🚂 Deploy to Railway

### Step 1: Push to GitHub
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/satyasetu-chatbot.git
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Add Volume for database persistence (Settings → Volumes → mount at `/app/data`)

### Step 3: Set Environment Variables
In Railway Settings → Variables, add:
```
GROQ_API_KEY=your_groq_key
SECRET_KEY=use_openssl_rand_hex_32
CORS_ORIGINS=["*"]
```

### Step 4: Deploy & Get URL
- Railway auto-deploys
- Copy your app URL: `https://your-app.up.railway.app`
- API docs at: `https://your-app.up.railway.app/docs`

## 📱 Integrate with Frontend

### React Example
```javascript
const API_URL = "https://your-app.up.railway.app";

// Login
const login = async () => {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      email: 'test@test.com',
      password: 'test123'
    })
  });
  const data = await res.json();
  return data.access_token;
};

// Chat
const chat = async (token, message) => {
  const res = await fetch(`${API_URL}/chat/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ message })
  });
  return await res.json();
};
```

## 🎓 Add Your Training Data

Edit `load_sample_data.py` and add your documents:
```python
documents = [
    "Your custom forgery detection knowledge...",
    "More information about your specific needs..."
]
```

Then reload:
```powershell
python load_sample_data.py
```

## 🔧 Customize

### Change LLM Model
In `.env`:
```env
GROQ_MODEL=mixtral-8x7b-32768  # or llama2-70b-4096
```

### Add More Universities
```python
from app.models.university import University
from app.core.database import SessionLocal

db = SessionLocal()
uni = University(
    name="Your University",
    code="YU",
    location="City",
    state="State"
)
db.add(uni)
db.commit()
```

## 🐛 Troubleshooting

### Issue: ChromaDB not loading
```powershell
rm -rf chroma_db
python load_sample_data.py
```

### Issue: Database error on Railway
- Ensure volume is mounted at `/app/data`
- SQLite database will be created automatically

### Issue: Groq API errors
- Check your API key is valid
- Free tier: 30 requests/minute limit

## 📚 Next Steps

1. ✅ Test locally
2. ✅ Deploy to Railway
3. ✅ Add your training data
4. ✅ Integrate with frontend
5. ✅ Add more university data
6. ✅ Customize for your needs

## 🎉 You're Done!

Your free RAG chatbot is ready. Questions? Check README.md or create an issue.
