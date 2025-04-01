from django.urls import path, include
from .views import register, login_view, dashboard, message_display, student_list, add_student, edit_student, delete_student, dashboard, import_students, export_students
from django.contrib import admin
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('register/', register, name='register'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    
]

urlpatterns += [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('message/', message_display, name='message'),
]

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('students/', student_list, name='student_list'),
    path('students/add/', add_student, name='add_student'),
    path('students/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', delete_student, name='delete_student'),
]

urlpatterns += [
    path('dashboard/', dashboard, name='dashboard'),
]

urlpatterns += [
    path('import_students/', import_students, name='import_students'),
]
urlpatterns += [
    path('export_students/', export_students, name='export_students'),
]