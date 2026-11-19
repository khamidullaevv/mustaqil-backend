from django.db import models

class Language(models.TextChoices):
    ENGLISH = "en", "English"
    UZBEK = "uz", "Uzbek"
    RUSSIAN = "ru", "Russian"