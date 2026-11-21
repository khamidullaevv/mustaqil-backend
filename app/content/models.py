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

class Problem(models.Model):
    class ProblemType(models.TextChoices):
        SINGLE_CHOICE = "single_choice", "Single Choice"
        MATCHING = "matching", "Matching"
        OPEN_ENDED = "open_ended", "Open Ended"

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"
     
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="problems",
    )
    language = models.CharField(
        max_length=5,
        choices=Language.choices,
        default=Language.UZBEK,
    )
    problem_type = models.CharField(
        max_length=20,
        choices=ProblemType.choices,
        default=ProblemType.SINGLE_CHOICE,
    )
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
    )
    statement = models.TextField()
    points = models.PositiveSmallIntegerField(default=10)
    is_original = models.BooleanField(default=True)
    is_verified_second_way = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    generator_key = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"#{self.pk} [{self.get_problem_type_display()}] {self.topic}"