# MongoDB Integration Guide

## Setup MongoDB

### Option 1: Local MongoDB Installation

1. **Download and Install MongoDB Community Server**
   - Visit: https://www.mongodb.com/try/download/community
   - Download for Windows
   - Run installer and follow instructions
   - MongoDB will run on `mongodb://localhost:27017` by default

2. **Start MongoDB Service**
   ```powershell
   # Start MongoDB service
   net start MongoDB
   ```

### Option 2: MongoDB Atlas (Cloud - Free Tier)

1. **Create Free Account**
   - Visit: https://www.mongodb.com/cloud/atlas/register
   - Create a free M0 cluster

2. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Example: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`

3. **Update Configuration**
   - Add to `.env` file:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DB_NAME=satyasetu_chatbot
   ```

### Option 3: Docker MongoDB

```powershell
# Run MongoDB in Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## Configuration

Update your `.env` file:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=satyasetu_chatbot
```

For MongoDB Atlas:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=satyasetu_chatbot
```

## New API Endpoints

### MongoDB Authentication Endpoints

- **POST** `/auth/mongo/register` - Register new user
- **POST** `/auth/mongo/login` - Login and get token
- **GET** `/auth/mongo/me` - Get current user info

### MongoDB Chat Endpoints

- **POST** `/chat/mongo/` - Send message (requires auth)
- **GET** `/chat/mongo/conversations` - Get all conversations
- **GET** `/chat/mongo/conversations/{id}` - Get specific conversation

## Usage Example

1. **Register a user:**
```json
POST /auth/mongo/register
{
  "email": "test@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "password": "testpass123"
}
```

2. **Login:**
```json
POST /auth/mongo/login
{
  "email": "test@example.com",
  "password": "testpass123"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

3. **Authorize in Swagger:**
   - Click "Authorize" button
   - Enter: `Bearer <your_token>`
   - Click Authorize

4. **Chat:**
```json
POST /chat/mongo/
{
  "message": "What courses are available?",
  "conversation_id": 0,
  "language": "en",
  "university_id": 0
}
```

## Data Models

### User Collection
- `email`: User email (unique)
- `username`: Username (unique)
- `full_name`: Full name
- `hashed_password`: Bcrypt hashed password
- `is_active`: Account status
- `created_at`: Registration timestamp

### Conversation Collection
- `user_id`: Reference to user
- `university_id`: University filter
- `messages`: Array of message objects
- `created_at`: Conversation start time
- `updated_at`: Last message time

### Message Embedded Document
- `content`: Message text
- `is_user`: True for user messages, False for bot
- `timestamp`: Message time
- `language`: Message language (en/hi)
- `sources`: RAG source documents

## Benefits of MongoDB

1. **Flexible Schema**: Easy to add new fields without migrations
2. **Embedded Documents**: Messages stored within conversations (no joins)
3. **Scalability**: Better for high-volume chat applications
4. **Cloud Ready**: MongoDB Atlas provides free tier
5. **Rich Queries**: Powerful aggregation and search capabilities

## Migration from SQLite

Both SQLite and MongoDB endpoints coexist:
- SQLite: `/auth/*` and `/chat/*`
- MongoDB: `/auth/mongo/*` and `/chat/mongo/*`

You can migrate gradually or use MongoDB for new features.

## Verify MongoDB Connection

Check server logs after starting:
```
INFO:app.core.mongodb:Connected to MongoDB at mongodb://localhost:27017
INFO:app.core.mongodb:Beanie initialized with document models
```

Visit: http://localhost:8000/docs to see all endpoints.
