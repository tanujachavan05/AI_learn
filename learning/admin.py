# learning/admin.py
from django.contrib import admin
from .models import (
    Course, Topic, Lesson, Quiz, Question, Choice, UserProgress, Attempt
)

# --- Courses ---
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'description')
    search_fields = ('title', 'description')


# --- Topics ---
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')
    search_fields = ('title', 'course__title')


# --- Lessons ---
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'order')
    list_filter = ('topic__course', 'topic')
    ordering = ('topic__course', 'order')
    search_fields = ('title', 'topic__title', 'topic__course__title')


# --- Quizzes ---
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson')
    search_fields = ('title', 'lesson__title')


# --- Choices inline for Questions ---
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2  # 2 default rows instead of 4
    min_num = 1  # At least one choice
    can_delete = True


# --- Questions ---
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'lesson', 'qtype', 'points')
    list_filter = ('lesson__topic__course', 'qtype')
    search_fields = ('text', 'lesson__title')
    inlines = [ChoiceInline]


# --- User Progress ---
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'score', 'last_attempt')
    list_filter = ('completed', 'lesson__topic__course')
    search_fields = ('user__username', 'lesson__title')


# --- Attempts ---
@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_choice', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'question__lesson__topic__course')
    search_fields = ('user__username', 'question__text')
