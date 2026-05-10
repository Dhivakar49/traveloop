from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.views.decorators.http import require_POST
import json

from .models import Trip, Stop, City, Activity, StopActivity, ChecklistItem, TripNote, UserProfile
from .forms import SignupForm, LoginForm, TripForm, StopForm, ChecklistItemForm, TripNoteForm, UserProfileForm


# ─── Auth ───────────────────────────────────────────────────────────────────

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        UserProfile.objects.create(user=user)
        login(request, user)
        messages.success(request, f"Welcome to Traveloop, {user.first_name}! 🌍")
        return redirect('dashboard')
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(request.GET.get('next', 'dashboard'))
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    trips = Trip.objects.filter(user=request.user)[:5]
    indian_cities = City.objects.filter(country='India').order_by('-popularity')[:6]
    global_cities = City.objects.exclude(country='India').order_by('-popularity')[:6]
    return render(request, 'trips/dashboard.html', {
        'trips': trips,
        'indian_cities': indian_cities,
        'global_cities': global_cities,
    })


# ─── Trips ───────────────────────────────────────────────────────────────────

@login_required
def trip_list(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'trips/trip_list.html', {'trips': trips})


@login_required
def trip_create(request):
    form = TripForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        trip = form.save(commit=False)
        trip.user = request.user
        trip.save()
        messages.success(request, "Trip created! Now build your itinerary.")
        return redirect('itinerary_builder', trip_id=trip.pk)
    return render(request, 'trips/trip_create.html', {'form': form})


@login_required
def trip_edit(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    form = TripForm(request.POST or None, request.FILES or None, instance=trip)
    if form.is_valid():
        form.save()
        messages.success(request, "Trip updated!")
        return redirect('trip_detail', trip_id=trip.pk)
    return render(request, 'trips/trip_create.html', {'form': form, 'trip': trip, 'editing': True})


@login_required
def trip_delete(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    if request.method == 'POST':
        trip.delete()
        messages.success(request, "Trip deleted.")
        return redirect('trip_list')
    return render(request, 'trips/trip_confirm_delete.html', {'trip': trip})


@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    stops = trip.stops.prefetch_related('stop_activities__activity', 'city').all()

    # Budget breakdown
    transport_total = sum(float(s.transport_cost) for s in stops)
    accommodation_total = sum(float(s.accommodation_cost) for s in stops)
    meal_total = sum(float(s.meal_cost_per_day) * s.days() for s in stops)
    activity_total = sum(float(s.activity_cost()) for s in stops)
    grand_total = transport_total + accommodation_total + meal_total + activity_total

    return render(request, 'trips/trip_detail.html', {
        'trip': trip,
        'stops': stops,
        'transport_total': transport_total,
        'accommodation_total': accommodation_total,
        'meal_total': meal_total,
        'activity_total': activity_total,
        'grand_total': grand_total,
    })


# ─── Itinerary Builder ───────────────────────────────────────────────────────

@login_required
def itinerary_builder(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    stops = trip.stops.prefetch_related('city', 'stop_activities__activity').all()
    stop_form = StopForm()
    cities = City.objects.all()
    return render(request, 'trips/itinerary_builder.html', {
        'trip': trip,
        'stops': stops,
        'stop_form': stop_form,
        'cities': cities,
    })


@login_required
def add_stop(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    if request.method == 'POST':
        form = StopForm(request.POST)
        if form.is_valid():
            stop = form.save(commit=False)
            stop.trip = trip
            stop.order = trip.stops.count()
            stop.save()
            messages.success(request, f"Stop added: {stop.city.name}")
        else:
            messages.error(request, "Error adding stop. Check dates.")
    return redirect('itinerary_builder', trip_id=trip_id)


@login_required
def remove_stop(request, stop_id):
    stop = get_object_or_404(Stop, pk=stop_id, trip__user=request.user)
    trip_id = stop.trip_id
    stop.delete()
    messages.success(request, "Stop removed.")
    return redirect('itinerary_builder', trip_id=trip_id)


@login_required
def add_activity_to_stop(request, stop_id):
    stop = get_object_or_404(Stop, pk=stop_id, trip__user=request.user)
    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        day_offset = int(request.POST.get('day_offset', 0))
        activity = get_object_or_404(Activity, pk=activity_id)
        StopActivity.objects.get_or_create(stop=stop, activity=activity, defaults={'day_offset': day_offset})
        messages.success(request, f"Added: {activity.name}")
    return redirect('itinerary_builder', trip_id=stop.trip_id)


@login_required
def remove_activity_from_stop(request, stop_activity_id):
    sa = get_object_or_404(StopActivity, pk=stop_activity_id, stop__trip__user=request.user)
    trip_id = sa.stop.trip_id
    sa.delete()
    return redirect('itinerary_builder', trip_id=trip_id)


# ─── City / Activity Search ──────────────────────────────────────────────────

@login_required
def city_search(request):
    q = request.GET.get('q', '')
    region = request.GET.get('region', '')
    cities = City.objects.all()
    if q:
        cities = cities.filter(Q(name__icontains=q) | Q(country__icontains=q))
    if region:
        cities = cities.filter(region__icontains=region)
    return render(request, 'trips/city_search.html', {'cities': cities, 'q': q})


@login_required
def activity_search(request):
    q = request.GET.get('q', '')
    city_id = request.GET.get('city_id', '')
    activity_type = request.GET.get('type', '')
    activities = Activity.objects.select_related('city').all()
    if q:
        activities = activities.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if city_id:
        activities = activities.filter(city_id=city_id)
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    cities = City.objects.all()
    return render(request, 'trips/activity_search.html', {
        'activities': activities,
        'cities': cities,
        'q': q,
        'selected_city': city_id,
        'selected_type': activity_type,
        'type_choices': Activity.TYPE_CHOICES,
    })


# ─── Checklist ───────────────────────────────────────────────────────────────

@login_required
def checklist(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    form = ChecklistItemForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.trip = trip
        item.save()
        return redirect('checklist', trip_id=trip_id)
    items = trip.checklist_items.all()
    by_category = {}
    for item in items:
        by_category.setdefault(item.get_category_display(), []).append(item)
    return render(request, 'trips/checklist.html', {
        'trip': trip,
        'form': form,
        'by_category': by_category,
        'total': items.count(),
        'packed': items.filter(is_packed=True).count(),
    })


@login_required
def toggle_checklist_item(request, item_id):
    item = get_object_or_404(ChecklistItem, pk=item_id, trip__user=request.user)
    item.is_packed = not item.is_packed
    item.save()
    return redirect('checklist', trip_id=item.trip_id)


@login_required
def delete_checklist_item(request, item_id):
    item = get_object_or_404(ChecklistItem, pk=item_id, trip__user=request.user)
    trip_id = item.trip_id
    item.delete()
    return redirect('checklist', trip_id=trip_id)


# ─── Notes ───────────────────────────────────────────────────────────────────

@login_required
def trip_notes(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    form = TripNoteForm(trip, request.POST or None)
    if form.is_valid():
        note = form.save(commit=False)
        note.trip = trip
        note.save()
        return redirect('trip_notes', trip_id=trip_id)
    notes = trip.notes.all()
    return render(request, 'trips/trip_notes.html', {'trip': trip, 'form': form, 'notes': notes})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(TripNote, pk=note_id, trip__user=request.user)
    trip_id = note.trip_id
    note.delete()
    return redirect('trip_notes', trip_id=trip_id)


# ─── Public Share ────────────────────────────────────────────────────────────

def public_itinerary(request, share_uuid):
    trip = get_object_or_404(Trip, share_uuid=share_uuid, is_public=True)
    stops = trip.stops.prefetch_related('stop_activities__activity', 'city').all()
    return render(request, 'trips/public_itinerary.html', {'trip': trip, 'stops': stops})


# ─── Profile ─────────────────────────────────────────────────────────────────

@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(request.user, request.POST or None, request.FILES or None, instance=profile_obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated!")
        return redirect('profile')
    return render(request, 'trips/profile.html', {'form': form, 'profile': profile_obj})


# ─── Budget (AJAX) ────────────────────────────────────────────────────────────

@login_required
def budget_data(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    stops = trip.stops.all()
    data = {
        'labels': ['Transport', 'Accommodation', 'Meals', 'Activities'],
        'values': [
            sum(float(s.transport_cost) for s in stops),
            sum(float(s.accommodation_cost) for s in stops),
            sum(float(s.meal_cost_per_day) * s.days() for s in stops),
            sum(float(s.activity_cost()) for s in stops),
        ],
        'budget': float(trip.budget),
        'total': float(trip.total_cost()),
    }
    return JsonResponse(data)
