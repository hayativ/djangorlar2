# -----------------------------
# 50 ORM Queries
# COPY AND PASTE TO SHELL
# -----------------------------

from django.db.models import Q, Count, Avg, Max, Min, F, Value, Case, When, IntegerField
from django.db.models.functions import Concat, ExtractYear, Now
from apps.customuser.models import CustomUser
from datetime import timedelta, date
from django.utils import timezone

# 2.1 Get all active users
CustomUser.objects.filter(is_active=True)

# 2.2 Get all users whose email ends with @gmail.com
CustomUser.objects.filter(email__endswith='@gmail.com')

# 2.3 Get all users from the city "Almaty"
CustomUser.objects.filter(city='Almaty')

# 2.4 Get all users not from the city "Almaty"
CustomUser.objects.exclude(city='Almaty')

# 2.5 Get all users with salary > 500000
CustomUser.objects.filter(salary__gt=500000)

# 2.6 Get all users from department "IT" and country "Kazakhstan"
CustomUser.objects.filter(department='IT', country='Kazakhstan')

# 2.7 Get all users where birth_date is NULL
CustomUser.objects.filter(birth_date__isnull=True)

# 2.8 Get all users whose first_name starts with "A" (case-insensitive)
CustomUser.objects.filter(first_name__istartswith='A')

# 2.9 Get the total number of users
CustomUser.objects.count()

# 2.10 Get the first 20 users ordered by date_joined descending
CustomUser.objects.order_by('-date_joined')[:20]

# 2.11 Get distinct list of cities
CustomUser.objects.values_list('city', flat=True).distinct()

# 2.12 Count how many users belong to department "Sales"
CustomUser.objects.filter(department='Sales').count()

# 2.13 Get all users who have logged in during the last 7 days
CustomUser.objects.filter(last_login__gte=timezone.now()-timedelta(days=7))

# 2.14 Name or surname contains "bek" (case-insensitive)
CustomUser.objects.filter(Q(first_name__icontains='bek') | Q(last_name__icontains='bek'))

# 2.15 Salary between 300000 and 700000
CustomUser.objects.filter(salary__gte=300000, salary__lte=700000)

# 2.16 Department in ["IT", "HR", "Finance"]
CustomUser.objects.filter(department__in=['IT','HR','Finance'])

# 2.17 Group users by department and count
CustomUser.objects.values('department').annotate(user_count=Count('id'))

# 2.18 Same as above but ordered descending
CustomUser.objects.values('department').annotate(user_count=Count('id')).order_by('-user_count')

# 2.19 Top 5 cities by user count
CustomUser.objects.values('city').annotate(user_count=Count('id')).order_by('-user_count')[:5]

# 2.20 Users who never logged in
CustomUser.objects.filter(last_login__isnull=True)

# 2.21 Average salary
CustomUser.objects.aggregate(Avg('salary'))

# 2.22 Max and Min salary
CustomUser.objects.aggregate(max_salary=Max('salary'), min_salary=Min('salary'))

# 2.23 Users with phone containing "+7"
CustomUser.objects.filter(phone__contains='+7')

# 2.24 Annotate full_name
CustomUser.objects.annotate(full_name=Concat(F('first_name'), Value(' '), F('last_name')))

# 2.25 Annotate birth year
CustomUser.objects.annotate(birth_year=ExtractYear('birth_date')).order_by('birth_year')

# 2.26 Users born in May
CustomUser.objects.filter(birth_date__month=5)

# 2.27 Role="manager" and salary>400000
CustomUser.objects.filter(role='manager', salary__gt=400000)

# 2.28 Role="employee" or department "HR"
CustomUser.objects.filter(Q(role='employee') | Q(department='HR'))

# 2.29 Count active users per city
CustomUser.objects.filter(is_active=True).values('city').annotate(active_count=Count('id'))

# 2.30 10 earliest registered users
CustomUser.objects.order_by('date_joined')[:10]

# 2.31 City starts with "A" and salary>300000
CustomUser.objects.filter(city__istartswith='A', salary__gt=300000)

# 2.32 Empty or null department
CustomUser.objects.filter(Q(department__isnull=True) | Q(department=''))

# 2.33 Stats by country
CustomUser.objects.values('country').annotate(user_count=Count('id'), avg_salary=Avg('salary'))

# 2.34 Staff users ordered by last_login descending
CustomUser.objects.filter(is_staff=True).order_by('-last_login')

# 2.35 Emails not containing "example.com"
CustomUser.objects.exclude(email__icontains='example.com')

# 2.36 Users with salary higher than average
avg_salary = CustomUser.objects.aggregate(avg=Avg('salary'))['avg']
CustomUser.objects.filter(salary__gt=avg_salary)

# 2.37 Emails used by more than one user
CustomUser.objects.values('email').annotate(email_count=Count('id')).filter(email_count__gt=1)

# 2.38 Annotate salary_level
CustomUser.objects.annotate(
    salary_level=Case(
        When(salary__lt=300000, then=Value('low')),
        When(salary__gte=300000, salary__lte=700000, then=Value('medium')),
        When(salary__gt=700000, then=Value('high')),
        output_field=models.CharField()
    )
).order_by('salary_level')

# 2.39 Users joined in current year
CustomUser.objects.filter(date_joined__year=timezone.now().year)

# 2.40 Total payroll per department
CustomUser.objects.values('department').annotate(total_salary=Sum('salary'))

# 2.41 IT department users never logged in
CustomUser.objects.filter(department='IT', last_login__isnull=True)

# 2.42 Kazakhstan users with null or empty city
CustomUser.objects.filter(country='Kazakhstan').filter(Q(city__isnull=True) | Q(city=''))

# 2.43 Users born before 1990-01-01 with salary not null
CustomUser.objects.filter(birth_date__lt=date(1990,1,1), salary__isnull=False)

# 2.44 Annotate years_since_joined
CustomUser.objects.annotate(
    years_since_joined=ExpressionWrapper((Now() - F('date_joined'))/365, output_field=IntegerField())
)

# 2.45 Sales users with gmail and salary>350000
CustomUser.objects.filter(department='Sales', email__endswith='@gmail.com', salary__gt=350000)

# 2.46 Order by country then salary descending
CustomUser.objects.order_by('country', '-salary')

# 2.47 Number of users per role with more than 100 users
CustomUser.objects.values('role').annotate(role_count=Count('id')).filter(role_count__gt=100)

# 2.48 Users whose last_login < date_joined
CustomUser.objects.filter(last_login__lt=F('date_joined'))

# 2.49 Annotate is_senior
CustomUser.objects.annotate(
    is_senior=Case(
        When(birth_date__lt=date(1985,1,1), then=Value(True)),
        default=Value(False),
        output_field=models.BooleanField()
    )
)

# 2.50 Departments sorted by average salary, only if users>=20
CustomUser.objects.values('department').annotate(user_count=Count('id'), avg_salary=Avg('salary')).filter(user_count__gte=20).order_by('-avg_salary')
