from django.db import models

from app.models import Language

class Topic(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255, blank=True, null=True)
    title_en = models.CharField(max_length=255, blank=True, null=True)
    exam_weight = models.PositiveSmallIntegerField(default=1)
    target_bank_count = models.PositiveSmallIntegerField(default=0)
    sort_order = models.PositiveSmallIntegerField(default=0)
    common_traps = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self) -> str:
        return self.title_uz or self.title_ru or self.title_en or self.slug