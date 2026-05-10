"""
Management command to delete all user data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from trips.models import UserProfile, Trip


class Command(BaseCommand):
    help = 'Delete all users and their related data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion of all users',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL users and their data!\n'
                    'Run with --confirm flag to proceed:\n'
                    'python manage.py clear_users --confirm'
                )
            )
            return

        # Count before deletion
        user_count = User.objects.count()
        trip_count = Trip.objects.count()
        profile_count = UserProfile.objects.count()

        # Delete all trips (will cascade delete stops, activities, etc.)
        Trip.objects.all().delete()
        
        # Delete all user profiles
        UserProfile.objects.all().delete()
        
        # Delete all users
        User.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted:\n'
                f'  - {user_count} users\n'
                f'  - {profile_count} user profiles\n'
                f'  - {trip_count} trips (and related data)'
            )
        )
