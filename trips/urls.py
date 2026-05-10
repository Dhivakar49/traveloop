from django.urls import path
from . import views, supabase_views

urlpatterns = [
    # Supabase Auth (Primary)
    path('login/', supabase_views.supabase_login_view, name='login'),
    path('signup/', supabase_views.supabase_signup_view, name='signup'),
    path('logout/', supabase_views.supabase_logout_view, name='logout'),
    
    # Traditional Auth (Backup)
    path('auth/django/login/', views.login_view, name='django_login'),
    path('auth/django/signup/', views.signup_view, name='django_signup'),
    path('auth/django/logout/', views.logout_view, name='django_logout'),
    
    # Supabase Auth (Alternative URLs)
    path('auth/supabase/login/', supabase_views.supabase_login_view, name='supabase_login'),
    path('auth/supabase/signup/', supabase_views.supabase_signup_view, name='supabase_signup'),
    path('auth/supabase/logout/', supabase_views.supabase_logout_view, name='supabase_logout'),
    path('auth/supabase/forgot-password/', supabase_views.supabase_forgot_password_view, name='supabase_forgot_password'),
    path('auth/supabase/reset-password/', supabase_views.supabase_reset_password_view, name='supabase_reset_password'),
    path('auth/supabase/password-reset/', supabase_views.supabase_password_reset_view, name='supabase_password_reset'),
    
    # Forgot Password (Primary URL)
    path('forgot-password/', supabase_views.supabase_forgot_password_view, name='forgot_password'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Trips
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/create/', views.trip_create, name='trip_create'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:trip_id>/edit/', views.trip_edit, name='trip_edit'),
    path('trips/<int:trip_id>/delete/', views.trip_delete, name='trip_delete'),

    # Itinerary Builder
    path('trips/<int:trip_id>/builder/', views.itinerary_builder, name='itinerary_builder'),
    path('trips/<int:trip_id>/add-stop/', views.add_stop, name='add_stop'),
    path('stops/<int:stop_id>/remove/', views.remove_stop, name='remove_stop'),
    path('stops/<int:stop_id>/add-activity/', views.add_activity_to_stop, name='add_activity_to_stop'),
    path('stop-activity/<int:stop_activity_id>/remove/', views.remove_activity_from_stop, name='remove_activity_from_stop'),

    # Search
    path('cities/', views.city_search, name='city_search'),
    path('activities/', views.activity_search, name='activity_search'),

    # Checklist
    path('trips/<int:trip_id>/checklist/', views.checklist, name='checklist'),
    path('checklist/<int:item_id>/toggle/', views.toggle_checklist_item, name='toggle_checklist_item'),
    path('checklist/<int:item_id>/delete/', views.delete_checklist_item, name='delete_checklist_item'),

    # Notes
    path('trips/<int:trip_id>/notes/', views.trip_notes, name='trip_notes'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),

    # Public Share
    path('share/<uuid:share_uuid>/', views.public_itinerary, name='public_itinerary'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # Budget API
    path('trips/<int:trip_id>/budget-data/', views.budget_data, name='budget_data'),
]
