# Personalized Chatbot - User Data Isolation

## ✅ What's Been Implemented:

### 1. **User-Specific Data Isolation**
- Each user can ONLY see their own conversations
- No user can access another user's data
- All queries filter by `user_id` automatically

### 2. **Personalized Chatbot Responses**
- Chatbot greets users by their name
- Uses user's full name and email in context
- Remembers user preferences
- First-time greeting for new conversations

### 3. **Security Features**
- **Authentication Required**: All endpoints require login token
- **Authorization Checks**: Every conversation access checks if it belongs to the logged-in user
- **Data Isolation**: MongoDB queries filter by `user_id` to prevent data leakage

### 4. **New API Endpoints**

#### Get User Profile
```
GET /auth/mongo/profile
```
Returns:
- User details (name, email, username)
- Preferences
- Account statistics (conversation count, account age)

#### Update User Preferences
```
PUT /auth/mongo/profile
Body: {"language": "en", "interests": ["courses", "admissions"]}
```

#### Get User's Conversations
```
GET /chat/mongo/conversations
```
Returns ONLY conversations belonging to the logged-in user with:
- User info
- List of conversations
- Message previews

#### Get Specific Conversation
```
GET /chat/mongo/conversations/{conversation_id}
```
Returns conversation ONLY if it belongs to the logged-in user

## How It Works:

### Login Flow:
1. **User registers** → Creates account in MongoDB
2. **User logs in** → Gets JWT token with their `user_id`
3. **User makes request** → Token validates identity
4. **System filters data** → Shows only that user's data

### Example Scenarios:

**User A logs in:**
- Sees only User A's conversations
- Chatbot addresses them as "User A"
- Cannot access User B's data

**User B logs in:**
- Sees only User B's conversations
- Chatbot addresses them as "User B"  
- Cannot access User A's data

## Database Structure:

### Users Collection:
```json
{
  "_id": "ObjectId",
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "hashed_password": "...",
  "preferences": {"language": "en"},
  "profile_data": {},
  "created_at": "2025-12-06T..."
}
```

### Conversations Collection:
```json
{
  "_id": "ObjectId",
  "user_id": "user_ObjectId",  // Links to specific user
  "messages": [...],
  "created_at": "...",
  "updated_at": "..."
}
```

## Testing the Personalization:

### Test 1: Create Multiple Users
```bash
# User 1
POST /auth/mongo/register
{
  "email": "alice@example.com",
  "username": "alice",
  "full_name": "Alice Smith",
  "password": "pass123"
}

# User 2
POST /auth/mongo/register
{
  "email": "bob@example.com",
  "username": "bob",
  "full_name": "Bob Johnson",
  "password": "pass456"
}
```

### Test 2: Login as User 1
```bash
POST /auth/mongo/login
{
  "email": "alice@example.com",
  "password": "pass123"
}
# Copy token
```

### Test 3: Chat as User 1
```bash
POST /chat/mongo/
Authorization: Bearer <alice_token>
{
  "message": "Hello",
  "conversation_id": 0,
  "language": "en"
}
# Response will greet "Alice Smith"
```

### Test 4: Login as User 2
```bash
POST /auth/mongo/login
{
  "email": "bob@example.com",
  "password": "pass456"
}
# Copy token
```

### Test 5: Chat as User 2
```bash
POST /chat/mongo/
Authorization: Bearer <bob_token>
{
  "message": "Hello",
  "conversation_id": 0,
  "language": "en"
}
# Response will greet "Bob Johnson"
```

### Test 6: Try to Access Other User's Data
```bash
# Login as Alice, try to access Bob's conversation
GET /chat/mongo/conversations/<bob_conversation_id>
Authorization: Bearer <alice_token>

# Result: 404 "Conversation not found or you don't have permission"
```

## Benefits:

✅ **Privacy**: Each user's data is completely isolated
✅ **Personalization**: Chatbot knows who it's talking to
✅ **Security**: Authentication and authorization at every step
✅ **Scalability**: Can handle unlimited users
✅ **Compliance**: Meets data privacy requirements

## Frontend Integration:

When building your website:

1. **Login Page**: Call `/auth/mongo/login` → Store token
2. **Dashboard**: Call `/auth/mongo/profile` → Show user info
3. **Chat Interface**: Call `/chat/mongo/` with token → Personalized chat
4. **History**: Call `/chat/mongo/conversations` → Show only user's chats

## MongoDB Collections:

Your MongoDB database (`SatyaSetu`) now has:
- `users` collection (all registered users)
- `conversations` collection (filtered by user_id)
- `messages` embedded in conversations

Each user sees ONLY their own data! 🎉
