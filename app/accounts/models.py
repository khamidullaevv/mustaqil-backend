from django.conf import settings
from django.db import models
from django.utils import timezone
from zoneinfo import ZoneInfo

from app.models import Language

def get_tashkent_today():
    return timezone.now().astimezone(ZoneInfo("Asia/Tashkent")).date()

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=2, choices=Language.choices, default=Language.UZBEK)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    telegram_username = models.CharField(max_length=64, blank=True, null=True, unique=True, default=None)
    telegram_id = models.BigIntegerField(blank=True, null=True, unique=True, default=None)
    nickname = models.CharField(max_length=64, blank=True, unique=True)
    grade = models.PositiveSmallIntegerField(blank=True, null=True)
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='students')
    preferred_language = models.CharField(max_length=2, choices=Language.choices, default=Language.UZBEK)
    reminder_enabled = models.BooleanField(default=True)
    reminder_time = models.TimeField(default=timezone.now().astimezone(ZoneInfo("Asia/Tashkent")).time())

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"{self.user.username} - {self.nickname if self.nickname else 'No Nickname'}"


class Streak(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='streaks')
    start_date = models.DateField(default=get_tashkent_today)
    end_date = models.DateField(blank=True, null=True)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-current_streak']

    def __str__(self) -> str:
        return f"{self.student_profile.user.username} - Current Streak: {self.current_streak}, Longest Streak: {self.longest_streak}"