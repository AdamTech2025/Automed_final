from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
import logging
from datetime import datetime
from typing import Union

from database import MedicalCodingDB  # Import your DB class
from .auth_utils import (
    generate_otp, send_otp_email, calculate_otp_expiry, 
    get_password_hash, verify_password, create_access_token, get_current_user
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Initialize Database connection (consider using dependency injection for better practice)
db = MedicalCodingDB()

# --- Request Models ---
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str # Add password field
    phone: Union[str, None] = None

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

# Define a new response model for login
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    name: str
    email: EmailStr
    role: str
    has_seen_tour: bool = False

class UpdateTourStatusRequest(BaseModel):
    has_seen_tour: bool = True

class ResetPasswordRequest(BaseModel):
    email: EmailStr

class VerifyResetOtpRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

# --- Routes ---
@router.post("/signup/send-otp", status_code=status.HTTP_200_OK)
async def signup_send_otp(request: SignupRequest):
    """
    Handles the first step of signup: check email, create user (if new) with HASHED password, generate and send OTP.
    """
    logger.info(f"Signup attempt for email: {request.email}")
    try:
        # Check if user already exists
        existing_user = db.get_user_by_email(request.email)
        
        user_id = None
        if existing_user:
            logger.warning(f"Email {request.email} already exists.")
            if existing_user.get('is_email_verified'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered and verified."
                )
            # If user exists but not verified, we'll allow OTP resend, 
            # but first update potential details and *maybe* the password 
            # (or reject if password change attempt during OTP resend isn't allowed)
            user_id = existing_user.get('id')
            # For this flow, let's assume we update details but don't change password here
            db.update_user_details(user_id, {"name": request.name, "phone": request.phone})
            logger.info(f"Existing unverified user found for {request.email}. Proceeding with OTP resend.")
            # NOTE: Consider if you want to allow password updates at this stage.
            # Hashing and updating password here could be an option:
            # hashed_password = get_password_hash(request.password)
            # db.update_user_password(user_id, hashed_password) # Requires adding update_user_password method
        else:
            # Create new user record (unverified)
            hashed_password = get_password_hash(request.password) # Hash the password
            user_data = {
                "name": request.name,
                "email": request.email,
                "phone": request.phone,
                "hashed_password": hashed_password # Store the hash
            }
            new_user = db.create_user(user_data)
            if not new_user or not new_user[0].get('id'):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user record."
                )
            user_id = new_user[0]['id']
            logger.info(f"Created new user record for {request.email} with ID: {user_id}")
            
        # Generate OTP
        otp = generate_otp()
        otp_expiry = calculate_otp_expiry()
        
        # Update user record with OTP
        update_success = db.update_user_otp(user_id, otp, otp_expiry)
        if not update_success:
             raise HTTPException(
                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 detail="Failed to store OTP."
             )
        
        # Send OTP via email
        email_sent = await send_otp_email(request.email, otp)
        if not email_sent:
             raise HTTPException(
                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 detail="Failed to send OTP email."
             )
            
        logger.info(f"OTP generated and sent to {request.email}")
        # Don't return user_id directly in response for security, maybe just success message
        return {"message": f"OTP sent successfully to {request.email}. Please verify."}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error during OTP sending for {request.email}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post("/signup/verify-otp", response_model=Token)
async def signup_verify_otp(request: VerifyOtpRequest):
    """
    Handles the second step of signup: verify the provided OTP and return JWT token.
    """
    logger.info(f"OTP verification attempt for email: {request.email}")
    try:
        # Get user by email
        user = db.get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            
        # Check if already verified
        if user.get('is_email_verified'):
            logger.warning(f"Attempt to re-verify already verified email: {request.email}")
            # Maybe generate a new token instead of error?
            # For now, let's raise an error to prevent re-verification flow
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified. Please log in.")

        # Validate OTP (rest of the validation logic remains the same...
        stored_otp = user.get('otp')
        otp_expires_at_str = user.get('otp_expires_at')
        if not stored_otp or not otp_expires_at_str:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active OTP found for this user.")
        try:
            otp_expires_at = datetime.fromisoformat(otp_expires_at_str)
        except ValueError:
             try:
                 otp_expires_at = datetime.strptime(otp_expires_at_str, '%Y-%m-%dT%H:%M:%S.%f')
             except ValueError:
                 logger.error(f"Failed to parse OTP expiry timestamp: {otp_expires_at_str}")
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid OTP expiry format.")
        utc_now = datetime.now(otp_expires_at.tzinfo)
        if stored_otp != request.otp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP.")
        if utc_now > otp_expires_at:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP has expired.")
        # ... end of OTP validation)

        # OTP is valid - Mark user as verified
        verified = db.verify_user_email(user.get('id'))
        if not verified:
             raise HTTPException(
                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 detail="Failed to update user verification status."
             )

        # Generate JWT token including role
        token_data = {"sub": user["email"], "role": user.get("role", "user")} # Default to user role if missing
        access_token = create_access_token(data=token_data)

        logger.info(f"Email {request.email} verified successfully. JWT token generated.")
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error during OTP verification for {request.email}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
        
# --- Login Route ---
@router.post("/login", response_model=LoginResponse)
async def login_for_access_token(request: LoginRequest):
    """
    Authenticates a user and returns a JWT access token along with user details.
    """
    logger.info(f"Login attempt for email: {request.email}")
    user = db.get_user_by_email(request.email)
    
    if not user:
        logger.warning(f"Login failed: User not found for {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.get('hashed_password'):
         logger.error(f"Login failed: User {request.email} has no password set.")
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, # Or 401?
            detail="User account incomplete.",
         )
         
    if not user.get('is_email_verified'):
         logger.warning(f"Login failed: Email {request.email} is not verified.")
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified. Please complete the signup process.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(request.password, user['hashed_password']):
        logger.warning(f"Login failed: Incorrect password for {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token including role
    token_data = {"sub": user["email"], "role": user.get("role", "user")} # Default to user role if missing
    access_token = create_access_token(data=token_data)
    
    logger.info(f"Login successful for {request.email}. Token generated.")
    # Return the new response structure
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "name": user.get("name", ""), # Include name (with fallback)
        "email": user["email"], # Include email
        "role": user.get("role", "user"), # Include role
        "has_seen_tour": user.get("has_seen_tour", False) # Include has_seen_tour
    } 

@router.post("/update-tour-status")
async def update_tour_status(
    request: UpdateTourStatusRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Updates the has_seen_tour status for a user.
    This is used to track if a user has completed the onboarding tour.
    """
    logger.info(f"Updating tour status for user {current_user.get('id')} to {request.has_seen_tour}")
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update the has_seen_tour field in the Users table
        updated = db.update_user_tour_status(user_id, request.has_seen_tour)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update tour status."
            )
            
        return {"status": "success", "message": "Tour status updated successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error updating tour status for {user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) 

@router.post("/forgot-password/send-otp")
async def forgot_password_send_otp(request: ResetPasswordRequest):
    """Send OTP for password reset."""
    logger.info(f"Password reset OTP request for email: {request.email}")
    try:
        user = db.get_user_by_email(request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email not found."
            )

        # Generate OTP
        otp = generate_otp()
        otp_expiry = calculate_otp_expiry()
        
        # Update user record with OTP
        update_success = db.update_user_otp(user.get('id'), otp, otp_expiry)
        if not update_success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store OTP."
            )
        
        # Send OTP via email
        email_sent = await send_otp_email(request.email, otp)
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP email."
            )
            
        return {"message": f"OTP sent successfully to {request.email}"}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error during password reset OTP sending: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post("/forgot-password/verify-otp")
async def verify_reset_otp(request: VerifyResetOtpRequest):
    """Verify OTP and update password."""
    logger.info(f"Password reset verification for email: {request.email}")
    try:
        user = db.get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        # Validate OTP
        stored_otp = user.get('otp')
        otp_expires_at_str = user.get('otp_expires_at')
        
        if not stored_otp or not otp_expires_at_str:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active OTP found.")
            
        try:
            otp_expires_at = datetime.fromisoformat(otp_expires_at_str)
        except ValueError:
            try:
                otp_expires_at = datetime.strptime(otp_expires_at_str, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                logger.error(f"Failed to parse OTP expiry timestamp: {otp_expires_at_str}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid OTP expiry format.")

        utc_now = datetime.now(otp_expires_at.tzinfo)
        if stored_otp != request.otp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP.")
        if utc_now > otp_expires_at:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP has expired.")

        # Hash new password and update
        hashed_password = get_password_hash(request.new_password)
        password_updated = db.update_user_password(user.get('id'), hashed_password)
        
        if not password_updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password."
            )

        # Clear OTP after successful password reset
        db.update_user_otp(user.get('id'), None, None)
        
        return {"message": "Password reset successful. Please login with your new password."}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error during password reset verification: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) 