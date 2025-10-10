# 2FA_Application

# 🔐 FastAPI Full-Stack 2FA Authentication Application

A secure full‑stack web application that implements **user registration** and **Two‑Factor Authentication (2FA)** using **TOTP (Time‑based One‑Time Password)** compatible with standard authenticator apps (Google Authenticator, Authy, etc.).

This repository contains a production‑ready FastAPI backend, a recommended Vue 3 frontend, database configuration examples (MySQL / PostgreSQL), and optional Docker Compose orchestration.

---

## 🚀 Quick overview

* **Backend:** Python + FastAPI + SQLAlchemy + PyOTP + JWT
* **Database:** MySQL (default example) 
* **Auth:** Hashed passwords (bcrypt / passlib), TOTP (PyOTP), QR code provisioning
* **Frontend:** Vue 3 (Composition API) example (Axios + Pinia + Vue Router)
* **Dev tools:** Uvicorn, Alembic (optional for migrations)

---

## ✨ Features

* ✅ User registration and login with hashed passwords
* ✅ JWT based authentication
* ✅ TOTP 2FA provisioning and verification
* ✅ QR code generation (for easy setup in authenticator apps)
* ✅ Protected API routes requiring both JWT and successful 2FA verification
* ✅ CORS configuration for frontend integration
* ✅ Modular project structure for maintainability

---

## 📁 project structure

```
/2FA_Application
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ database.py
│  │  ├─ models.py
│  │  ├─ schemas.py
│  │  ├─ auth.py
│  │  ├─ routes/
│  │  │  ├─ auth_routes.py
│  │  │  ├─ user_routes.py
│  │  ├─ utils/
│  │  │  ├─ security.py
│  │  │  ├─ qr.py
│  ├─ requirements.txt
├─ frontend/
│  ├─ (vue 3 app)
├─ README.md
```

---

## ⚙️ Installation & Setup (Backend)

### Prerequisites

* Python 3.11+
* MySQL server (or PostgreSQL)
* Node.js + npm (for frontend)

### 1) Clone the repo

```bash
git clone <repository-url>
cd 2FA_Application
```

### 2) Backend (local dev)

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (example below) and fill with your values.

**Example `.env`**

```
# Database
DATABASE_URL=mysql+pymysql://db_user:db_pass@localhost:3306/2fa_db
# or for postgres:
# DATABASE_URL=postgresql+psycopg2://pg_user:pg_pass@localhost:5432/2fa_db

# App
FRONTEND_URL=http://localhost:5173
```

Start the app:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` and interactive docs at `http://localhost:8000/docs`.

### 3) Frontend (recommended)

Use the `frontend` folder to host a Vue 3 app. Basic steps:

```bash
cd frontend
npm install
npm run dev
```

Adjust API base URL in frontend config (e.g. `src/services/api.js`) to `http://localhost:8000`.

---

## 🗄️ Database

Create the database user and DB before running the backend. Example for MySQL:

```sql
CREATE DATABASE `2fa_db`;
CREATE USER 'db_user'@'localhost' IDENTIFIED BY 'db_pass';
GRANT ALL PRIVILEGES ON `2fa_db`.* TO 'db_user'@'localhost';
FLUSH PRIVILEGES;
```

If using Alembic for migrations, configure `alembic.ini` and run:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

---

## 🧩 API Endpoints (example)

> These are example routes — adapt to your implementation.

### Public

* `POST /api/auth/register` — register new user. Body: `{ "username": "...", "password": "..." }`
* `POST /api/auth/login` — login with username & password. Returns temporary JWT + flag `2fa_enabled`.

### 2FA Setup (authenticated)

* `POST /api/auth/2fa/setup` — generate TOTP secret & provisioning URI (returns QR code data / otpauth URI).

  * Response: `{ "otpauth_url": "otpauth://totp/YourApp:username?secret=ABCDEF...&issuer=YourApp", "qr_base64": "data:image/png;base64,..." }
* `POST /api/auth/2fa/verify-setup` — confirm the 6‑digit code to enable 2FA. Body: `{ "token": "123456" }`.
* `POST /api/auth/2fa/disable` — disable 2FA after verifying password & TOTP code.

### 2FA Login Flow

1. `POST /api/auth/login` — server verifies credentials; if user has 2FA enabled, server returns `access_token` limited/temporary or a `login_token` and `2fa_required: true`.
2. `POST /api/auth/2fa/login` — send `{ "login_token": "...", "otp": "123456" }` to finalize login. Server returns full `access_token`.

### Protected routes

* `GET /api/user/me` — protected; requires Authorization header `Bearer <access_token>` and optionally `X-2FA-Verified: true` or an internal server check that 2FA was validated for the token.

---

## 🔐 2FA Flow (detailed)

1. During setup, backend generates a secret using `pyotp.random_base32()` and stores it (encrypted/hashed or safely stored) against the user record.
2. The backend returns a provisioning URI `pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name='YourApp')` and a QR code image (use `qrcode` or `qrcode[pil]`) which users scan with an authenticator app.
3. The user reads the 6-digit code from the authenticator and submits it to `verify-setup`. The backend verifies with `pyotp.TOTP(secret).verify(code, valid_window=1)`.
4. On login, if 2FA enabled, require an additional OTP verification before issuing final tokens.

**Security tips:** never expose the TOTP secret in plain text to clients after initial setup. If possible, encrypt the secret at rest with a server-side key.

---

## 🧾 Example code snippets

### Password hashing (Passlib, bcrypt)

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### TOTP generation & verification (pyotp)

```python
import pyotp

secret = pyotp.random_base32()
# provisioning uri
uri = pyotp.totp.TOTP(secret).provisioning_uri(name="user@example.com", issuer_name="YourApp")
# verify
totp = pyotp.TOTP(secret)
valid = totp.verify("123456")
```

---

## 📣 Frontend notes

* Provide screens for: Register, Login (step1 credentials), Login 2FA (step2 enter OTP), Enable 2FA (show QR + enter initial code), Disable 2FA, Profile.
* Use Axios for API calls; save the final JWT in memory or `httpOnly` cookies (recommended for security). Avoid storing JWT in localStorage if you want better XSS protection.
* Example flow: after login (credentials), if API responds with `2fa_required: true`, show OTP input. On success, receive full access token and redirect to dashboard.

---

## ✅ Security best practices (recommended)

* Use `httpOnly`, `Secure`, `SameSite` cookies for storing tokens when possible.
* Rotate and protect `JWT_SECRET_KEY` using environment variables or secret managers.
* Rate limit login attempts & 2FA verification requests.
* Encrypt TOTP secrets at rest or use an HSM / secrets manager for production.
* Use HTTPS in production.
* Keep dependencies up to date and run security scanning tools.

---

## 🧪 Testing

* Unit test authentication logic (password hashing, JWT, TOTP verification).
* Integration tests for the full login + 2FA flow.
* Manual test: register → enable 2FA → scan QR code → verify → log out → login → enter OTP.

---

## 📈 Future improvements

* Add refresh tokens and token revocation list
* Add account recovery / backup codes for 2FA
* Add email / SMS fallback MFA (careful with SIM swap risk)
* Add role‑based access control (RBAC)
* Add audit logging for security events

---

## 🛠️ Use of AI Tools

This project may include generated example code or documentation written with the help of AI tools. Review and audit any generated code before deploying.

---

## 🤝 Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/name`)
3. Commit your changes (`git commit -m "feat: description"`)
4. Push to the branch (`git push origin feature/name`)
5. Open a Pull Request

Please include tests and update documentation where applicable.

---



## 📬 Contact

If you need help, or want me to generate example backend source files (e.g., `main.py`, `models.py`, `auth.py`) or a sample Vue frontend, tell me which files you want and I'll create them.

---


