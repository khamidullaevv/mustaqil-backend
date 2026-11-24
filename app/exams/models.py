from datetime import datetime
from django.db import models
from django.utils import timezone

from app.accounts.models import StudentProfile, get_tashkent_today
from app.content.models import Problem

class Exam(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="exams",
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="exams",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exam_date = models.DateField(default=get_tashkent_today)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    earned_points = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["id", "exam_date"]
        unique_together = ("student", "problem", "exam_date")

    def __str__(self) -> str:
        return f"#{self.pk} [{self.student}] {self.problem} - {self.exam_date}"