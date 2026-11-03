
from django.contrib.auth.models import AbstractUser
from django.db import models
from departments.models import Department


class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]

    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )

    email = models.EmailField(unique=True)

    student_id = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    year = models.CharField(
        max_length=1,
        choices=YEAR_CHOICES,
        blank=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"
