from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone

from app.accounts.models import StudentProfile, get_tashkent_today
from app.content.models import Problem

class ExamSession(models.Model):
    class SessionType(models.TextChoices):
        PRACTICE = "practice", "Практика"
        EXAM = "exam", "Экзамен"
        DIOGNOSTIC = "diagnostic", "Диагностический"
    class SessionStatus(models.TextChoices):
        IN_PROGRESS = "in_progress", "В процессе"
        COMPLETED = "completed", "Завершён"
        EXPIRED = "expired", "Время вышло"
    
    session_type = models.CharField(
        max_length=20,
        choices=SessionType.choices,
        default=SessionType.PRACTICE,
    )
    session_status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.IN_PROGRESS,
    )
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

    def save(self, *args, **kwargs):
        if not self.expires_at:
            start = timezone.now()
            minutes = 150 if self.session_type == self.SessionType.EXAM else 20
            self.expires_at = start + timedelta(minutes=minutes)
        if not self.total_questions:
            self.total_questions = 45 if self.session_type == self.SessionType.EXAM else 15
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"#{self.pk} [{self.student}] {self.problem} - {self.exam_date}"

class ExamQuestion(models.Model):
    exam_session = models.ForeignKey(
        ExamSession,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_number = models.PositiveSmallIntegerField()
    is_answered = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["question_number"]
        unique_together = ("exam_session", "question_number")

    def __str__(self) -> str:
        return f"#{self.pk} [{self.exam_session}] Question {self.question_number}"