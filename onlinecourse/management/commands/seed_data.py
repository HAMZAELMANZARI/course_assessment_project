"""Seed the database with demo data for experimenting.

Usage:
    python manage.py seed_data

Creates:
  * superuser:   username `admin`,   password `p@ssword123`
  * learner:     username `learner`, password `p@ssword123` (enrolled + can take the exam)
  * course:      "Learning Django" with one lesson
  * exam:        "Is Django a Python framework?" (grade 100) with choices Yes (correct) / No
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import now

from onlinecourse.models import (
    Instructor, Learner, Course, Lesson, Enrollment, Question, Choice
)

PASSWORD = 'p@ssword123'


class Command(BaseCommand):
    help = 'Create demo users, course, lesson, and exam data.'

    def handle(self, *args, **options):
        # --- Users ---
        admin_user, created = User.objects.get_or_create(
            username='admin', defaults={'email': 'admin@example.com',
                                        'is_staff': True, 'is_superuser': True})
        if created:
            admin_user.set_password(PASSWORD)
            admin_user.save()

        learner_user, created = User.objects.get_or_create(
            username='learner', defaults={'email': 'learner@example.com',
                                          'first_name': 'Demo'})
        if created:
            learner_user.set_password(PASSWORD)
            learner_user.save()

        instructor, _ = Instructor.objects.get_or_create(
            user=admin_user, defaults={'total_learners': 1})
        learner, _ = Learner.objects.get_or_create(
            user=learner_user, defaults={'social_link': 'https://example.com/learner'})

        # --- Course + Lesson ---
        course, created = Course.objects.get_or_create(
            name='Learning Django',
            defaults={
                'description': 'Django is an extremely popular and fully featured '
                               'server-side web framework, written in Python',
                'pub_date': now().date(),
                'total_enrollment': 1,
            })
        if created:
            course.instructors.add(instructor)

        Lesson.objects.get_or_create(
            course=course, title='What is Django', order=0,
            defaults={
                'content': 'Django is a high-level Python web framework that '
                           'encourages rapid development and clean, pragmatic '
                           'design. Built by experienced developers, it takes '
                           'care of much of the hassle of web development, so '
                           'you can focus on writing your app without needing '
                           'to reinvent the wheel. It is free and open source.'
            })

        # --- Exam: Question + Choices ---
        question, _ = Question.objects.get_or_create(
            course=course, content='Is Django a Python framework',
            defaults={'grade': 100})
        Choice.objects.get_or_create(
            question=question, content='Yes', defaults={'is_correct': True})
        Choice.objects.get_or_create(
            question=question, content='No', defaults={'is_correct': False})

        # --- Enrollment for the demo learner ---
        Enrollment.objects.get_or_create(user=learner_user, course=course)

        self.stdout.write(self.style.SUCCESS(
            'Seed data created.\n'
            '  superuser: admin / {pwd}\n'
            '  learner:   learner / {pwd}\n'
            '  course:    Learning Django (with 1 question exam)'.format(pwd=PASSWORD)))
