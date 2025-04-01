from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
import csv
from django.http import HttpResponse
from .tasks import send_welcome_email

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')

def message_display(request):
    messages.success(request, "Registration successful. Welcome!")
    messages.error(request, "Something went wrong.")

# List Students
def student_list(request):
    students = Student.objects.all()
    paginator = Paginator(students, 5)  # Show 5 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/student_list.html', {'page_obj': page_obj})

# Add Student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Student added successfully!')
            
            # Send welcome email
            send_mail(
                'Welcome to the Student Management System',
                f'Hello {student.name},\n\nWelcome to our Student Management System! We are glad to have you.',
                settings.EMAIL_HOST_USER,
                [student.email],
                fail_silently=False,
            )

            # Send welcome email asynchronously
            send_welcome_email.delay(student.name, student.email)
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'users/add_student.html', {'form': form})

# Edit Student
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student details updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'users/edit_student.html', {'form': form})

# Delete Student
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'users/delete_student.html', {'student': student})

#Create the Dashboard View
def dashboard(request):
    total_students = Student.objects.count()
    students_above_60 = Student.objects.filter(marks__gte=60).count()
    students_below_60 = Student.objects.filter(marks__lt=60).count()
    recent_students = Student.objects.order_by('-id')[:5]  # Get the latest 5 students

    context = {
        'total_students': total_students,
        'students_above_60': students_above_60,
        'students_below_60': students_below_60,
        'recent_students': recent_students,
    }
    return render(request, 'users/dashboard.html', context)

def import_students(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file')
            return redirect('import_students')

        # Read the CSV file
        df = pd.read_csv(csv_file)
        for index, row in df.iterrows():
            Student.objects.create(
                name=row['name'],
                email=row['email'],
                age=row['age'],
                marks=row['marks']
            )
        messages.success(request, 'Students imported successfully!')
        return redirect('student_list')
    return render(request, 'users/import_students.html')

def export_students(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Age', 'Marks'])

    students = Student.objects.all().values_list('name', 'email', 'age', 'marks')
    for student in students:
        writer.writerow(student)

    return response
# Create your views here.
