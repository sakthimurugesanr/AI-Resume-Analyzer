# 🤖 AI Resume Analyser

A FastAPI-powered backend that lets users register with a profile image and resume. Resumes and images are stored on **Cloudinary** (in separate folders) and user data is persisted to **NeonDB** (PostgreSQL).

---

## ✨ Features

- 📋 User registration with username, email, role, and phone
- 🖼️ Profile image upload → Cloudinary `users/images/`
- 📄 Resume upload (PDF / DOC / DOCX) → Cloudinary `users/resumes/`
- 🗄️ All data stored in NeonDB (serverless PostgreSQL)
- ✅ Auto-creates the database table on startup
- 🌐 CORS configured for frontend dev servers

---

## 🗂️ Project Structure

```
Resume-with-AI/
├── main.py                  # API routes
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (never commit this)
├── db/
│   ├── __init__.py
│   ├── database.py          # DB connection
│   └── schema.py            # Table creation
├── models/
│   ├── __init__.py
│   └── user.py              # Pydantic response model
└── cloudinary_utils/
    ├── __init__.py
    └── uploader.py          # Cloudinary config + upload helpers
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Resume-with-AI.git
cd Resume-with-AI
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
DATABASE_URL=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

Fill in the values:

| Variable | Where to get it |
|---|---|
| `DATABASE_URL` | [NeonDB Console](https://console.neon.tech) → Connection string |
| `CLOUDINARY_CLOUD_NAME` | [Cloudinary Dashboard](https://cloudinary.com/console) → Cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary Dashboard → API Keys |
| `CLOUDINARY_API_SECRET` | Cloudinary Dashboard → API Keys |

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API will be live at **http://127.0.0.1:8000**

---

## 📡 API Endpoints

### `POST /users` — Register a user

| Field | Type | Required | Description |
|---|---|---|---|
| `username` | string | ✅ | Full name |
| `email` | string | ✅ | Email address |
| `role` | string | ✅ | e.g. `developer`, `designer` |
| `phone` | string | ❌ | Phone number |
| `image` | file | ❌ | Profile picture (JPEG / PNG / WEBP) |
| `resume` | file | ❌ | Resume (PDF / DOC / DOCX) |

**Example response:**
```json
{
  "id": 1,
  "username": "John Doe",
  "email": "john@example.com",
  "role": "developer",
  "phone": "+1234567890",
  "image_url": "https://res.cloudinary.com/.../users/images/...",
  "resume_url": "https://res.cloudinary.com/.../users/resumes/...",
  "message": "User registered successfully."
}
```

### `GET /users/{id}` — Get user by ID

### `GET /health` — Health check

---

## 📖 Interactive API Docs

Once the server is running, open:

- **Swagger UI** → http://127.0.0.1:8000/docs
- **ReDoc** → http://127.0.0.1:8000/redoc

---

## 🔒 Environment Variables Reference

```env
# Comma-separated list of allowed frontend origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# NeonDB PostgreSQL connection string
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Cloudinary credentials
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

> ⚠️ **Never commit your `.env` file.** Add it to `.gitignore`.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `asyncpg` | Async PostgreSQL driver |
| `cloudinary` | File uploads |
| `python-multipart` | Form & file parsing |
| `python-dotenv` | Load `.env` file |
| `pydantic` | Data validation |

---

## 🛡️ .gitignore (recommended)

Add these to your `.gitignore`:

```
venv/
__pycache__/
.env
*.pyc
```