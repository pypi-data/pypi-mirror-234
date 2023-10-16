# Django
from django.conf import settings

GATHER_STATISTICS_DURING_QUIZ = getattr(
    settings, "DJANGO_EASY_QUIZ_GATHER_STATISTICS_DURING_QUIZ", False
)

SAVE_QUIZZES_RESULTS = getattr(settings, "DJANGO_EASY_QUIZ_SAVE_QUIZZES_RESULTS", False)

GATHER_STATISTICS = getattr(settings, "DJANGO_EASY_QUIZ_GATHER_STATISTICS", False)

SAVE_PDF = getattr(settings, "DJANGO_EASY_QUIZ_SAVE_PDF", False)
