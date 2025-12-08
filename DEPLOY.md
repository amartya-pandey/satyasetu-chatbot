# Deploy Satyasetu Chatbot to Railway

## Quick Deploy Steps:

1. **Install Railway CLI** (if not already):
```bash
npm i -g @railway/cli
```

2. **Login to Railway**:
```bash
railway login
```

3. **Initialize Railway Project**:
```bash
railway init
```

4. **Add Environment Variables**:
```bash
railway variables set GROQ_API_KEY=your-groq-api-key-here
railway variables set DATABASE_URL=sqlite:///./data/satyasetu.db
railway variables set SECRET_KEY=your-secret-key-change-this-in-production
```

5. **Deploy**:
```bash
railway up
```

6. **Get Your URL**:
```bash
railway domain
```

## Alternative: Deploy via GitHub

1. Push your code to GitHub
2. Go to https://railway.app/
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables in Railway dashboard
6. Railway will auto-deploy!

Your app will be live at: `https://your-app-name.railway.app/docs`
