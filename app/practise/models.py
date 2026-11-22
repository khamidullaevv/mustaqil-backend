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