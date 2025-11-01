# learning/urls.py
from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    # ======================
    # 🔹 Home & Auth
    # ======================
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # ======================
    # 🔹 Courses & Topics
    # ======================
    path('courses/', views.course_list, name='course_list'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),

    # ======================
    # 🔹 Lessons
    # ======================
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),

    # ======================
    # 🔹 Quizzes
    # ======================
    path('quiz/', views.quiz_list, name='quiz_list'),  # All available quizzes
    path('quiz/<int:lesson_id>/', views.quiz_question, name='quiz_question'),  # Take quiz for lesson
    path('quiz/<int:lesson_id>/result/', views.quiz_result, name='quiz_result'),  # Show result

    # ======================
    # 🔹 User Progress
    # ======================
    path('progress/', views.user_progress, name='user_progress'),


    # ======================
    # 🔹 AI
    # ======================
    path("ai-assistant/", views.ai_page, name="ai_assistant"),
    path("api/ask_ai/", views.ask_ai, name="ask_ai"),
]


