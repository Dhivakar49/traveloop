from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    language = models.CharField(max_length=10, default='en')
    saved_destinations = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Profile of {self.user.username}"


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    cost_index = models.DecimalField(max_digits=8, decimal_places=2, default=1.0,
                                     help_text="Daily cost estimate in INR")
    popularity = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['-popularity']

    def __str__(self):
        return f"{self.name}, {self.country}"


class Activity(models.Model):
    TYPE_CHOICES = [
        ('sightseeing', 'Sightseeing'),
        ('food', 'Food & Dining'),
        ('adventure', 'Adventure'),
        ('culture', 'Culture'),
        ('shopping', 'Shopping'),
        ('relaxation', 'Relaxation'),
        ('nightlife', 'Nightlife'),
        ('transport', 'Transport'),
    ]
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='sightseeing')
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    image_url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    cover_photo = models.ImageField(upload_to='trip_covers/', blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_public = models.BooleanField(default=False)
    share_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} by {self.user.username}"

    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def total_cost(self):
        return sum(stop.total_cost() for stop in self.stops.all())

    def stop_count(self):
        return self.stops.count()


class Stop(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='stops')
    arrival_date = models.DateField()
    departure_date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    accommodation_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    transport_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    meal_cost_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=30)

    class Meta:
        ordering = ['order', 'arrival_date']

    def __str__(self):
        return f"{self.city.name} - {self.trip.name}"

    def days(self):
        return (self.departure_date - self.arrival_date).days + 1

    def activity_cost(self):
        return sum(sa.activity.cost for sa in self.stop_activities.all())

    def total_cost(self):
        meal_total = self.meal_cost_per_day * self.days()
        return float(self.accommodation_cost) + float(self.transport_cost) + float(meal_total) + float(self.activity_cost())


class StopActivity(models.Model):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='stop_activities')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    scheduled_time = models.TimeField(blank=True, null=True)
    day_offset = models.PositiveIntegerField(default=0, help_text="Day 0 = arrival day")

    class Meta:
        ordering = ['day_offset', 'scheduled_time']

    def __str__(self):
        return f"{self.activity.name} @ {self.stop.city.name}"


class ChecklistItem(models.Model):
    CATEGORY_CHOICES = [
        ('clothing', 'Clothing'),
        ('documents', 'Documents'),
        ('electronics', 'Electronics'),
        ('toiletries', 'Toiletries'),
        ('medicine', 'Medicine'),
        ('other', 'Other'),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='checklist_items')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_packed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({'✓' if self.is_packed else '○'})"


class TripNote(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='notes')
    stop = models.ForeignKey(Stop, on_delete=models.SET_NULL, null=True, blank=True, related_name='trip_notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.trip.name}"
