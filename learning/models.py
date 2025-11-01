from django.db import models 
from django.contrib.auth.models import User
from django.utils.text import slugify

# --- Courses, Topics, Lessons ---
class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)


class Topic(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='topics'
    )
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    slug = models.SlugField(max_length=220)

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'slug')
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    def __str__(self):
        return f"{self.course.title} — {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]
        super().save(*args, **kwargs)


class Lesson(models.Model):
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='lessons'
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.IntegerField(default=1)
    code_example = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return self.title


# --- Quiz linked to Lesson ---
class Quiz(models.Model):
    lesson = models.OneToOneField(
        Lesson, on_delete=models.CASCADE, related_name='quiz'
    )
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        lesson_title = getattr(self.lesson, 'title', 'Unknown Lesson')
        return f"Quiz for {lesson_title}"


# --- Questions & Choices ---
QUESTION_TYPES = [
    ('mcq', 'Multiple Choice'),
    ('tf', 'True/False'),
    ('code', 'Code Fill'),
]

class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='questions'
    )
    text = models.TextField()
    qtype = models.CharField(max_length=10, choices=QUESTION_TYPES, default='mcq')
    points = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        lid = self.id if self.id is not None else '?'
        lesson_title = getattr(self.lesson, 'title', 'Unknown Lesson')
        return f"{lesson_title} - Q{lid}"

    def correct_choice(self):
        return self.choices.filter(is_correct=True).first()


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='choices'
    )
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

    def __str__(self):
        return self.text[:50]


# --- User Progress & Quiz Attempts ---
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresses')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progresses'

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'Done' if self.completed else 'Pending'}"


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attempts')
    answer_text = models.TextField(blank=True, null=True)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Attempt'
        verbose_name_plural = 'Attempts'

    def __str__(self):
        return f"{self.user.username} - Q{self.question.id if self.question_id else '?'} - {'Correct' if self.is_correct else 'Wrong'}"
