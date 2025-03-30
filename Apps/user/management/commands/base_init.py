from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from Apps.books.models import User


class Command(BaseCommand):
    help = 'Create Initial User'

    def handle(self, *args, **options):
        password = make_password("admin@123")
        user, created = User.objects.get_or_create(name="admin", defaults={"password": password})
        print(f"user:{user.name}")
