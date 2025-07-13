from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings.'

    def handle(self, *args, **kwargs):
        if not User.objects.exists():
            user = User.objects.create_user(username='demo', password='demo1234')
        else:
            user = User.objects.first()
        cities = ['Paris', 'London', 'New York', 'Tokyo', 'Berlin']
        for i in range(10):
            Listing.objects.create(
                title=f'Sample Listing {i+1}',
                description='A wonderful place to stay.',
                address=f'{i+1} Main St',
                city=random.choice(cities),
                country='Country',
                price_per_night=random.randint(50, 500),
                listing_type='hotel',
                max_guests=random.randint(1, 8),
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 3),
                available=True,
                owner=user
            )
        self.stdout.write(self.style.SUCCESS('Database seeded with sample listings.'))