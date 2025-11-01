from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm, LoginForm
from .models import (
    Course, Topic, Lesson, Quiz, Question, Choice, UserProgress, Attempt
)
# ==========================
# 🤖 AI Assistant (Web + API)
# ==========================
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline

# 🔹 Load model once at startup
ai_model = pipeline("text-generation", model="gpt2")

def ai_page(request):
    return render(request, "learning/ai_assistant.html")

@csrf_exempt
def ask_ai(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        user_message = data.get("message", "")

        try:
            # 🔹 Generate AI response
            result = ai_model(user_message, max_length=100, num_return_sequences=1)
            reply = result[0]["generated_text"]

            # Clean up extra tokens
            reply = reply.replace("\n", " ").strip()

        except Exception as e:
            reply = f"⚠️ Error: {e}"

        return JsonResponse({"reply": reply})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


# ==========================
# 🔹 Home & Authentication
# ==========================
def home(request):
    courses = Course.objects.all()
    return render(request, 'learning/home.html', {'courses': courses})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Account created successfully! You can log in now.")
            return redirect('learning:login')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'learning/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}! 👋")
                return redirect('learning:home')
            else:
                messages.error(request, "❌ Invalid username or password.")
        else:
            messages.error(request, "❌ Invalid login form data.")
    else:
        form = LoginForm()
    return render(request, 'learning/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "🚪 You have been logged out.")
    return redirect('learning:login')


# ==========================
# 🔹 Courses
# ==========================
@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    topics = course.topics.all()
    lesson_id = request.GET.get('lesson')
    selected_lesson = None
    if lesson_id:
        selected_lesson = get_object_or_404(Lesson, pk=lesson_id, topic__course=course)
    courses = Course.objects.all()
    return render(request, 'learning/course_detail.html', {
        'course': course,
        'courses': courses,
        'topics': topics,
        'selected_lesson': selected_lesson
    })


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'learning/course_list.html', {'courses': courses})


# ==========================
# 🔹 Topics & Lessons
# ==========================
@login_required
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    lessons = Lesson.objects.filter(topic=topic)
    return render(request, 'learning/topic_detail.html', {'topic': topic, 'lessons': lessons})


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    quiz = getattr(lesson, 'quiz', None)
    return render(request, 'learning/lesson_detail.html', {'lesson': lesson, 'quiz': quiz})


# ==========================
# 🔹 Quiz System
# ==========================
@login_required
def quiz_list(request):
    lessons_with_quiz = Lesson.objects.filter(questions__isnull=False).distinct()
    return render(request, 'learning/quiz_list.html', {'lessons': lessons_with_quiz})


@login_required
def quiz_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.prefetch_related('choices')

    if request.method == "POST":
        score = 0
        total = questions.count()
        Attempt.objects.filter(user=request.user, question__lesson=lesson).delete()
        for question in questions:
            selected_choice_id = request.POST.get(f"question_{question.id}")
            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += question.points
                Attempt.objects.create(
                    user=request.user,
                    question=question,
                    selected_choice=selected_choice,
                    is_correct=is_correct
                )
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'score': score, 'completed': True}
        )
        if not created:
            progress.score = score
            progress.completed = True
            progress.save()
        messages.success(request, f"You scored {score}/{total} on {lesson.title}!")
        return redirect('learning:quiz_result', lesson_id=lesson.id)

    return render(request, 'learning/quiz_detail.html', {'lesson': lesson, 'questions': questions})


@login_required
def quiz_question(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.prefetch_related('choices')

    if request.method == "POST":
        score = 0
        total = questions.count()
        Attempt.objects.filter(user=request.user, question__lesson=lesson).delete()
        for question in questions:
            selected_choice_id = request.POST.get(f"question_{question.id}")
            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += question.points
                Attempt.objects.create(
                    user=request.user,
                    question=question,
                    selected_choice=selected_choice,
                    is_correct=is_correct
                )
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'score': score, 'completed': True}
        )
        if not created:
            progress.score = score
            progress.completed = True
            progress.save()
        messages.success(request, f"You scored {score}/{total} on {lesson.title}!")
        return redirect('learning:quiz_result', lesson_id=lesson.id)

    return render(request, 'learning/quiz_question.html', {'lesson': lesson, 'questions': questions})


@login_required
def quiz_result(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    attempts = Attempt.objects.filter(user=request.user, question__lesson=lesson)
    total_questions = lesson.questions.count()
    correct_answers = attempts.filter(is_correct=True).count()
    return render(request, 'learning/quiz_result.html', {
        'lesson': lesson,
        'attempts': attempts,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
    })


# ==========================
# 🔹 User Progress
# ==========================
@login_required
def user_progress(request):
    progress = UserProgress.objects.filter(user=request.user)
    return render(request, 'learning/user_progress.html', {'progress': progress})
