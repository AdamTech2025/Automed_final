import random
import string
from datetime import datetime, timedelta, timezone
import asyncio
import smtplib
from email.message import EmailMessage
import os
import logging
import ssl
from concurrent.futures import ThreadPoolExecutor
from passlib.context import CryptContext # For password hashing
from jose import JWTError, jwt # For JWT
from fastapi import Depends, HTTPException, status # Add Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer # Add OAuth2PasswordBearer
from typing import Union # Import Union

# Configure logging
logger = logging.getLogger(__name__)

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration (Read from environment variables)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
# Ensure default value if not set or invalid
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43600")) 
except ValueError:
    logger.warning("Invalid ACCESS_TOKEN_EXPIRE_MINUTES, defaulting to 43600.")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    logger.error("FATAL ERROR: JWT_SECRET_KEY environment variable not set.")
    # In a real app, you might want to exit or raise a more critical error here
    # For now, we log, but JWT creation will fail later if SECRET_KEY is None

# --- Password Hashing/Verification ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

# --- JWT Token Creation ---
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """Creates a JWT access token. Expects 'sub' (email) and optionally 'role' in data."""
    if not SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY is not configured. Cannot create token.")
        
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- OTP Generation ---
def generate_otp(length: int = 6) -> str:
    """Generates a random numeric OTP of a specified length."""
    return "".join(random.choices(string.digits, k=length))

# --- Email Sending Implementation ---
async def send_otp_email(email: str, otp: str):
    """
    Sends the OTP code to the specified email address using SMTP.
    Reads configuration from environment variables.
    """
    sender_email = os.getenv("EMAIL_SENDER_ADDRESS")
    sender_password = os.getenv("EMAIL_SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com") # Default example for Gmail
    smtp_port_str = os.getenv("SMTP_PORT", "587") # Default example for TLS

    if not sender_email or not sender_password:
        logger.error("Email sender address or password not configured in .env file.")
        return False
        
    try:
        smtp_port = int(smtp_port_str)
    except ValueError:
        logger.error(f"Invalid SMTP_PORT value in .env file: {smtp_port_str}")
        return False

    # Create the email message
    msg = EmailMessage()
    msg.set_content(f"""
    Dear User,

    Thank you for choosing Adam Tech. Your one-time verification code (OTP) is: {otp}

    Please enter this code on the verification page to complete your account setup. This code will expire in 10 minutes.

    If you didn't request this code, please ignore this email or contact our support team at support@adamtechnologies.in.

    Best regards,
    The Adam Tech Team
    Adam Tech Inc. | www.adamtechnologies.in
    """)
    msg['Subject'] = 'Your Adam Tech OTP for Verification'
    msg['From'] = sender_email
    msg['To'] = email

    logger.info(f"Attempting to send OTP email to {email} via {smtp_server}:{smtp_port}...")

    try:
        # Use run_in_executor for the blocking smtplib calls
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            await loop.run_in_executor(
                pool,
                lambda: send_email_sync(smtp_server, smtp_port, sender_email, sender_password, msg)
            )
        logger.info(f"Successfully sent OTP email to {email}")
        return True
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP Authentication failed. Check sender email/password/app password.")
        return False
    except smtplib.SMTPConnectError:
         logger.error(f"Could not connect to SMTP server {smtp_server}:{smtp_port}.")
         return False
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {str(e)}", exc_info=True)
        return False

def send_email_sync(smtp_server, smtp_port, sender_email, sender_password, msg):
    """Synchronous helper function to send email using smtplib."""
    # Connect to the SMTP server and send the email
    # Using SMTP_SSL() might be needed for different ports/servers (e.g., 465)
    context = ssl.create_default_context() # For TLS
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context) # Secure the connection
        server.login(sender_email, sender_password)
        server.send_message(msg)

# --- OTP Expiry Calculation ---
def calculate_otp_expiry(minutes: int = 10) -> datetime:
    """Calculates the OTP expiry timestamp."""
    return datetime.utcnow() + timedelta(minutes=minutes)

# --- Authentication Dependency --- 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login") # Point to your login route

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency to get the current user's data (as dict) from a JWT token.
    Validates the token, fetches the user from the database, and checks verification status.
    Returns the full user dictionary (excluding sensitive fields potentially handled by DB query).
    """
    # Import database here to avoid potential top-level circular imports
    from database import MedicalCodingDB 
    db = MedicalCodingDB()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if SECRET_KEY is None:
            logger.error("JWT_SECRET_KEY is not set, cannot validate token.")
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            logger.warning("Token payload missing 'sub' (email) claim.")
            raise credentials_exception
        # Role is now also in the token, but we fetch from DB for freshness
        # role: str | None = payload.get("role") # Example if we wanted to use role from token
        # if role is None:
        #    logger.warning("Token payload missing 'role' claim.")
        #    raise credentials_exception

    except JWTError as e:
        logger.error(f"JWT Error during token decode: {e}")
        raise credentials_exception from e

    # Fetch user from DB using the email from the token
    user = db.get_user_by_email(email) # This now fetches the role too
    if user is None:
        logger.warning(f"User with email '{email}' from token not found in DB.")
        raise credentials_exception
        
    # Ensure the user's email is verified before allowing access to protected routes
    if not user.get('is_email_verified'):
        logger.warning(f"Attempt to access protected route by unverified user: {email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please complete verification.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Authenticated user ID: {user.get('id')} | Email: {email} | Role: {user.get('role')}")
    # Exclude sensitive fields before returning (already handled by get_user_by_email select *)
    user_data = user.copy()
    user_data.pop('hashed_password', None)
    user_data.pop('otp', None)
    user_data.pop('otp_expires_at', None)
    return user_data # Return the user dictionary

# --- Role Check Dependency ---
async def require_admin_role(current_user: dict = Depends(get_current_user)):
    """
    Dependency that checks if the current user has the 'admin' role.
    Raises HTTP 403 Forbidden if the user is not an admin.
    """
    user_role = current_user.get('role')
    if user_role != 'admin':
        logger.warning(f"Admin access denied for user {current_user.get('id')} with role '{user_role}'.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required.",
        )
    logger.info(f"Admin access granted for user {current_user.get('id')}.")
    return current_user # Return user data if admin check passes 