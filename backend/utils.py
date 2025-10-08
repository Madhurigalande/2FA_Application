import pyotp
import qrcode
from passlib.context import CryptContext
from io import BytesIO
import base64

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Truncate password to 72 characters before hashing
    truncated = password[:72]
    return pwd_context.hash(truncated)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password[:72], hashed)


def generate_otp_secret():
    return pyotp.random_base32()

def generate_qr_code_uri(username: str, secret: str):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name="SecureApp")
    qr = qrcode.make(uri)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return qr_b64

def verify_totp(secret: str, code: str):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
