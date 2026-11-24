from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone

from app.accounts.models import StudentProfile
from app.content.models import Problem

class Mistake(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="mistakes_items",
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="mistakes_items",
    )
    mistake_count = models.PositiveSmallIntegerField(default=1)
    review_stage = models.PositiveSmallIntegerField(default=0)
    next_review_at = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)
    last_mistake_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["is_resolved", "next_review_at"]
        unique_together = [("student", "problem")]

    def schedule_next_review(self) -> None:
        intervals_days = {0: 1, 1: 3, 2: 7}
        days = intervals_days.get(self.review_stage, 7)
        self.next_review_at = timezone.now() + timedelta(days=days)

    def __str__(self) -> str:
        return f"#{self.pk} [{self.student}] {self.problem} - Resolved: {self.is_resolved}"