import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
from apps.customuser.models import CustomUser

class Command(BaseCommand):
    help = "Generate 10,000 fake users for CustomUser"

    def handle(self, *args, **options):
        fake = Faker()
        total_users = 10000
        batch_size = 1000

        departments = ["IT", "HR", "Sales", "Finance"]
        roles = ["admin", "manager", "employee"]

        # Предварительно хешируем пароль один раз
        hashed_password = make_password("12345")

        users_to_create = []

        for i in range(total_users):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            phone = fake.phone_number()
            city = fake.city()
            country = fake.country()
            department = random.choice(departments)
            role = random.choice(roles)
            birth_year = random.randint(1975, 2005)
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=50)

            user = CustomUser(
                username=email.split("@")[0] + str(i),  # уникальный username
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                city=city,
                country=country,
                department=department,
                role=role,
                birth_date=birth_date,
                salary=random.randint(30000, 150000),
                is_active=True,
                is_staff=(role == "admin"),
                password=hashed_password,
                date_joined=fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None),
            )
            users_to_create.append(user)

            # Если набрали batch_size, создаем пакет и очищаем список
            if len(users_to_create) >= batch_size:
                CustomUser.objects.bulk_create(users_to_create)
                self.stdout.write(f"Inserted {i + 1} users...")
                users_to_create = []

        # Создаем оставшихся пользователей
        if users_to_create:
            CustomUser.objects.bulk_create(users_to_create)
            self.stdout.write(f"Inserted remaining {len(users_to_create)} users.")

        self.stdout.write(self.style.SUCCESS("Successfully created 10,000 users!"))
