AI Learn - AI-Based Programming Language Learning Platform

Project Overview

AI Learn is an innovative web-based e-learning platform designed to help users learn programming languages (Python, JavaScript, HTML, Django, and more) in an interactive, personalized, and intelligent way.

The platform integrates DistilGPT-2 (a lightweight version of GPT-2) to provide real-time AI assistance, allowing users to ask programming-related questions and receive instant explanations, code suggestions, and debugging help.

This project was developed as a Mini Project for the Bachelor of Engineering in Information Technology at Indala College of Engineering, Kalyan, Maharashtra (Affiliated to University of Mumbai).

Key Features

User Authentication: Secure registration and login using Django's built-in authentication system.

Personalized Dashboard: Tracks user progress, completed lessons, and quiz scores.

Structured Lessons: Step-by-step tutorials for multiple programming languages.

Interactive Quizzes: Assess knowledge with instant scoring and feedback.

AI Chatbot: Powered by DistilGPT-2 – ask questions in natural language and get intelligent responses.

Responsive Design: Built with Bootstrap for seamless experience on desktop, tablet, and mobile.

Progress Tracking: Adaptive learning path based on performance.

<img width="1024" height="768" alt="Screenshot (49)" src="https://github.com/user-attachments/assets/97b7b17d-76b9-4139-b6fd-13a9d9e4809a" />
<img width="1024" height="768" alt="Screenshot (50)" src="https://github.com/user-attachments/assets/63181e18-b570-4c31-84da-ad09db5865d0" />
<img width="1024" height="768" alt="Screenshot (51)" src="https://github.com/user-attachments/assets/e464d462-21f8-4efd-b88f-e2974262d4c8" />
<img width="1024" height="768" alt="Screenshot (52)" src="https://github.com/user-attachments/assets/1536a226-d5ea-4c7b-99a1-99d88c7dcd8b" />
<img width="1024" height="768" alt="Screenshot (54)" src="https://github.com/user-attachments/assets/b2735a0e-f61c-4960-a272-27570818d1df" />

<img width="1024" height="768" alt="Screenshot (47)" src="https://github.com/user-attachments/assets/0446160c-9385-48ea-9b99-1cc6ce4e212d" />


Tech Stack
Backend

Python 3.10+

Django 5.0 (MVT architecture)

SQLite3 (default Django database)

Frontend

HTML5, CSS3, JavaScript

Bootstrap 5

AI Integration

Hugging Face Transformers library

DistilGPT-2 model (with PyTorch)

Development Tools

Visual Studio Code

Git (recommended for version control)

Installation & Setup
Prerequisites

Python 3.10 or higher

pip (Python package manager)

virtualenv (recommended)

Steps

Clone the repository

git clone https://github.com/tanujachavan05/ai-learn.git
cd ai-learn


Create a virtual environment

python -m venv venv


Activate the virtual environment

# On macOS/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate


Install dependencies

pip install django transformers torch numpy


Run database migrations

python manage.py migrate


Create a superuser (for admin panel)

python manage.py createsuperuser


Start the development server

python manage.py runserver


Open the app in your browser
Visit http://127.0.0.1:8000/

Note on AI Model

The first time you use the AI chatbot, the DistilGPT-2 model will be downloaded automatically (~300 MB). Ensure a stable internet connection.

Usage

Register a new account or log in.

Select programming languages to learn.

Explore lessons, take quizzes, and chat with the AI tutor anytime.
