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
        problem_type_display = self.get_problem_type_display()
        return f"#{self.pk} [{problem_type_display}] {self.topic}"


class ChoiceOption(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="choice_options",
    )
    text = models.TextField()
    label = models.CharField(max_length=1, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"#{self.pk} [{self.problem}] {self.text[:30]}{'...' if len(self.text) > 30 else ''}"



class MatchingPair(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="matching_pairs",
    )
    left_item = models.TextField()
    right_item = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"#{self.pk} [{self.problem}] {self.left_item[:30]}{'...' if len(self.left_item) > 30 else ''} - {self.right_item[:30]}{'...' if len(self.right_item) > 30 else ''}"

class ProblemSolution(models.Model):
    class AnswerMode(models.TextChoices):
        CHOICE_LABEL = "choice_label", "Choice Label"
        MATCHING_MAP = "matching_map", "Matching Pair"
        NUMERIC = "numeric", "Numerical"
        SYMBOLIC = "symbolic", "Symbolic"


    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="solutions",
    )
    answer_mode = models.CharField(max_length=20, choices=AnswerMode.choices, default=AnswerMode.NUMERIC)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    correct_answer = models.TextField(blank=True)
    solution_steps = models.TextField(blank=True)
    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"#{self.pk} [{self.problem}] {self.solution_steps[:30]}{'...' if len(self.solution_steps) > 30 else ''}"

class Hint(models.Model):
    class Level(models.PositiveSmallIntegerField):
        LEVEL_CHOICES = [
            (1, "Level 1"),
            (2, "Level 2"),
            (3, "Level 3"),
        ]




    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="hints",
    )
    text = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    level = models.PositiveSmallIntegerField(choices=Level.LEVEL_CHOICES, default=1)
    content = models.TextField(blank=True, null=True)
    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"#{self.pk} [{self.problem}] {self.text[:30]}{'...' if len(self.text) > 30 else ''}"