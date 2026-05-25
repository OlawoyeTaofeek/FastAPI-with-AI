User
 │
 ▼
FastAPI (API Gateway)
 │
 ├── 🔐 Auth Service (your existing project!)
 │     ├── JWT (Access Token - short lived, 15min)
 │     ├── Refresh Token (long lived, 7days) → stored in Redis
 │     ├── Email Verification (on signup)
 │     ├── Password Reset (token via email)
 │     └── OAuth2 (Google login - optional later)
 │
 ├── 📧 Email Service
 │     └── SendGrid / Resend / SMTP
 │
 ├── ⚡ Redis
 │     ├── Refresh token store
 │     ├── Email verification tokens
 │     ├── Password reset tokens
 │     ├── Rate limiting (per user/IP)
 │     └── Session cache (user context)
 │
 ├── 📄 PDF Service
 │     ├── Upload → S3
 │     ├── Extract text → chunk
 │     ├── Embed → Pinecone (namespaced per user+session)
 │     └── Background task (FastAPI BackgroundTasks / Celery)
 │
 ├── 💬 Chat Service
 │     ├── Session management
 │     ├── Conversation history → PostgreSQL
 │     ├── Context retrieval → Pinecone
 │     └── Stream response → OpenAI
 │
 ├── 💳 Billing Service
 │     └── Stripe (plans, usage limits)
 │
 └── 🗄️ Data Layer
       ├── PostgreSQL (NeonDB)   ← persistent data
       ├── Redis                 ← ephemeral/fast data
       ├── AWS S3                ← raw PDF files
       └── Pinecone              ← vector embeddings


Register → Hash password → Save user (PostgreSQL)
        → Generate verify token → Store in Redis (TTL 24hrs)
        → Send email with link

Verify Email → Check Redis token → Mark user verified in PostgreSQL
             → Delete token from Redis

Login → Check credentials → Generate Access Token (JWT, 15min)
      → Generate Refresh Token → Store in Redis (TTL 7days)
      → Return both tokens

Request → Attach Access Token in header
        → FastAPI validates JWT
        → If expired → use Refresh Token → Redis checks it → new Access Token

Logout → Delete Refresh Token from Redis
       → Access Token expires naturally

