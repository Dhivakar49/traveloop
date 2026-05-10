"""
Supabase Authentication Views
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
import logging

from .supabase_auth import get_supabase_client, get_or_create_django_user, verify_supabase_token
from .models import UserProfile

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def supabase_signup_view(request):
    """Handle Supabase signup"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            
            if not email or not password:
                error_msg = 'Email and password required'
                if request.content_type == 'application/json':
                    return JsonResponse({'error': error_msg}, status=400)
                messages.error(request, error_msg)
                return render(request, 'registration/supabase_signup.html')
            
            # Sign up with Supabase
            try:
                supabase = get_supabase_client()
                response = supabase.auth.sign_up({
                    'email': email,
                    'password': password,
                    'options': {
                        'data': {
                            'first_name': first_name,
                            'last_name': last_name,
                        }
                    }
                })
            except Exception as supabase_error:
                logger.error(f"Supabase connection error: {supabase_error}")
                error_msg = f"Cannot connect to Supabase. Please check your internet connection or try again later. Error: {str(supabase_error)}"
                if request.content_type == 'application/json':
                    return JsonResponse({'error': error_msg}, status=503)
                messages.error(request, error_msg)
                return render(request, 'registration/supabase_signup.html')
            
            if response.user:
                # Create Django user
                user_data = {
                    'email': email,
                    'sub': response.user.id,
                    'user_metadata': {
                        'first_name': first_name,
                        'last_name': last_name,
                    }
                }
                django_user = get_or_create_django_user(user_data)
                django_login(request, django_user)
                
                messages.success(request, f"Welcome to Traveloop, {first_name}! 🌍")
                
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': True,
                        'access_token': response.session.access_token if response.session else None,
                        'user': {'email': email, 'id': response.user.id}
                    })
                return redirect('dashboard')
            else:
                error_msg = 'Signup failed. Please try again.'
                if request.content_type == 'application/json':
                    return JsonResponse({'error': error_msg}, status=400)
                messages.error(request, error_msg)
                
        except Exception as e:
            logger.error(f"Signup error: {e}")
            error_msg = f"An error occurred: {str(e)}"
            if request.content_type == 'application/json':
                return JsonResponse({'error': error_msg}, status=400)
            messages.error(request, error_msg)
    
    return render(request, 'registration/supabase_signup.html')


@require_http_methods(["GET", "POST"])
def supabase_login_view(request):
    """Handle Supabase login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                error_msg = 'Email and password required'
                if request.content_type == 'application/json':
                    return JsonResponse({'error': error_msg}, status=400)
                messages.error(request, error_msg)
                return render(request, 'registration/supabase_login.html')
            
            # Sign in with Supabase
            try:
                supabase = get_supabase_client()
                response = supabase.auth.sign_in_with_password({
                    'email': email,
                    'password': password
                })
            except Exception as supabase_error:
                logger.error(f"Supabase connection error: {supabase_error}")
                error_msg = f"Cannot connect to Supabase. Please check your internet connection. Error: {str(supabase_error)}"
                if request.content_type == 'application/json':
                    return JsonResponse({'error': error_msg}, status=503)
                messages.error(request, error_msg)
                return render(request, 'registration/supabase_login.html')
            
            if response.user and response.session:
                # Get or create Django user
                user_data = {
                    'email': response.user.email,
                    'sub': response.user.id,
                    'user_metadata': response.user.user_metadata or {}
                }
                django_user = get_or_create_django_user(user_data)
                django_login(request, django_user)
                
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': True,
                        'access_token': response.session.access_token,
                        'refresh_token': response.session.refresh_token,
                        'user': {'email': email, 'id': response.user.id}
                    })
                
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                error_msg = 'Invalid credentials'
                if request.content_type == 'application/json':
                    return JsonResponse({'error': error_msg}, status=401)
                messages.error(request, error_msg)
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            error_msg = f"Login failed: {str(e)}"
            if request.content_type == 'application/json':
                return JsonResponse({'error': error_msg}, status=401)
            messages.error(request, error_msg)
    
    return render(request, 'registration/supabase_login.html')


def supabase_logout_view(request):
    """Handle Supabase logout"""
    try:
        # Sign out from Supabase
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except Exception as e:
        logger.warning(f"Supabase logout error: {e}")
        pass  # Continue even if Supabase logout fails
    
    # Django logout
    django_logout(request)
    messages.success(request, "You've been logged out successfully")
    return redirect('login')


@require_http_methods(["POST"])
def supabase_password_reset_view(request):
    """Request password reset email"""
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        email = data.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)
        
        supabase = get_supabase_client()
        supabase.auth.reset_password_email(email)
        
        return JsonResponse({
            'success': True,
            'message': 'Password reset email sent'
        })
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["GET", "POST"])
def supabase_forgot_password_view(request):
    """Forgot password page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, 'Please enter your email address')
            return render(request, 'registration/supabase_forgot_password.html')
        
        try:
            supabase = get_supabase_client()
            # Supabase will send password reset email
            supabase.auth.reset_password_email(
                email,
                options={
                    'redirect_to': request.build_absolute_uri('/auth/supabase/reset-password/')
                }
            )
            messages.success(
                request, 
                f'Password reset instructions have been sent to {email}. Please check your inbox.'
            )
            return redirect('login')
        except Exception as e:
            logger.error(f"Forgot password error: {e}")
            messages.error(request, 'Unable to send reset email. Please try again.')
    
    return render(request, 'registration/supabase_forgot_password.html')


@require_http_methods(["GET", "POST"])
def supabase_reset_password_view(request):
    """Reset password page (after clicking email link)"""
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not new_password or not confirm_password:
            messages.error(request, 'Please fill in all fields')
            return render(request, 'registration/supabase_reset_password.html')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'registration/supabase_reset_password.html')
        
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return render(request, 'registration/supabase_reset_password.html')
        
        try:
            # Get access token from URL (Supabase sends it)
            access_token = request.GET.get('access_token')
            
            if not access_token:
                messages.error(request, 'Invalid or expired reset link')
                return redirect('login')
            
            supabase = get_supabase_client()
            # Update password
            supabase.auth.update_user({
                'password': new_password
            })
            
            messages.success(request, 'Password updated successfully! Please login with your new password.')
            return redirect('login')
        except Exception as e:
            logger.error(f"Reset password error: {e}")
            messages.error(request, 'Unable to reset password. Please try again or request a new reset link.')
    
    return render(request, 'registration/supabase_reset_password.html')
