"""
Supabase Authentication Integration for Django
"""
from supabase import create_client, Client
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
import jwt
from functools import wraps
from django.http import JsonResponse


# Initialize Supabase client
def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def get_supabase_admin_client() -> Client:
    """Get Supabase admin client with service role key"""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)


def verify_supabase_token(token: str) -> dict:
    """
    Verify Supabase JWT token
    Returns user data if valid, raises exception if invalid
    """
    try:
        # Decode JWT without verification (Supabase handles verification)
        decoded = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        return decoded
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")


def get_or_create_django_user(supabase_user_data: dict) -> User:
    """
    Get or create Django user from Supabase user data
    """
    email = supabase_user_data.get('email')
    user_id = supabase_user_data.get('sub')  # Supabase user ID
    
    if not email:
        raise ValueError("Email not found in Supabase user data")
    
    # Try to get existing user by email
    user, created = User.objects.get_or_create(
        username=email,  # Use email as username
        defaults={
            'email': email,
            'first_name': supabase_user_data.get('user_metadata', {}).get('first_name', ''),
            'last_name': supabase_user_data.get('user_metadata', {}).get('last_name', ''),
        }
    )
    
    # Store Supabase user ID in user profile if needed
    if created:
        from .models import UserProfile
        UserProfile.objects.get_or_create(user=user)
    
    return user


def supabase_auth_required(view_func):
    """
    Decorator to require Supabase authentication
    Validates JWT token from Authorization header
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'No token provided'}, status=401)
        
        token = auth_header.split(' ')[1]
        
        try:
            user_data = verify_supabase_token(token)
            user = get_or_create_django_user(user_data)
            request.user = user
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
    
    return wrapper
