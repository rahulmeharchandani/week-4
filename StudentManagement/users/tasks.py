from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(student_name, student_email):
    send_mail(
        'Welcome to the Student Management System',
        f'Hello {student_name},\n\nWelcome to our Student Management System! We are glad to have you.',
        settings.EMAIL_HOST_USER,
        [student_email],
        fail_silently=False,
    )