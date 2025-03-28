from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm

def student_list(request):
    students = Student.objects.all()
    form = StudentForm()
    

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('student_list')

    return render(request, 'students/student_list.html', {'students': students})