from django.db import models

from app.accounts import StudentProfile, get_tashkent_time
from app.content.models import Problem

class DailySeries(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="daily_series",
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="daily_series",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    series_date = models.DateField(default=get_tashkent_time().date)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    earned_points = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["id", "series_date"]
        unique_together = ("student", "problem", "series_date")

    def __str__(self) -> str:
        return f"#{self.pk} [{self.student}] {self.problem} - {self.series_date}"

class Attempt(models.Model):
    class Context(models.TextChoices):
        PRACTICE = "practice", "Practice"
        DAILY_SERIES = "daily_series", "Daily Series"
        MISTAKE_REVIEW = "mistake_review", "Mistake Review"
        EXAM = "exam", "Exam"
        DIAGNOSTIC = "diagnostic", "Diagnostic"

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    context = models.CharField(max_length=50, choices=Context.choices, default=Context.PRACTICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_correct = models.BooleanField(default=False)
    earned_points = models.PositiveSmallIntegerField(default=0)
    submitted_answer = models.TextField(blank=True, null=True)
    solved_independently = models.BooleanField(default=False)
    points_awarded = models.BooleanField(default=False)
    time_spent_seconds = models.PositiveIntegerField(default=0)
    hint_used_count = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ["id", "created_at"]

    def __str__(self) -> str:
        status = "OK" if self.is_correct else "ERR"
        return f"{self.student.nickname} | #{self.problem} | {status}"

