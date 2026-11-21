from django.conf import settings
from django.db import models
from django.utils import timezone
from zoneinfo import ZoneInfo

from app.models import Language

def get_tashkent_today():
    return timezone.now().astimezone(ZoneInfo("Asia/Tashkent")).date()