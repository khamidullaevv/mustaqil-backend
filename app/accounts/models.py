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