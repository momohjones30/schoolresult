from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, StudentRegistrationForm, TeacherLoginForm, TeacherCustomUserCreationForm
from django.urls import reverse
from django.http import JsonResponse
from results.models import Session, Grade, Term
from student.models import Students_file, Teacher
from subjects.models import Subject
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.contrib.auth import get_backends


def main_page(request):
    return render(request, 'main.html') 

'''For teacher and student registration'''
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend' #Set the backend attribute
            login(request, user, backend=user.backend)
            messages.success(request, "Congratulations, your username has been registered. Fill the displayed form")
            return redirect('student_registration')
    else:
        form = CustomUserCreationForm()
    return render(request, 'bootstrap5/uni_form.html', {'form': form})



def student_registration(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login/?next=/')

    initial_data = {'username': request.user.username}
    form = StudentRegistrationForm(initial=initial_data)

    if request.method == 'POST':
        # initial_data = {'username': request.user.username}
        # form = StudentRegistrationForm(initial=initial_data)
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Process the form data
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            messages.success(request, "Student registration form successfully filled!")
            # Automatically log the student into their dashboard
            # Ensure the user is logged in (though they should already be authenticated)
            backend = 'django.contrib.auth.backends.ModelBackend'  # Use the default backend
            login(request, request.user, backend=backend)

            # Redirect to the student dashboard
            return redirect(reverse('StudentAdmin:student_dashboard'))  # Use the URL name of the student dashboard:
        # form.fields['username'].widget.attrs['readonly'] = True # makes the username field read only
    return render(request, 'student_registration.html', {'form': form})





'''TEACHERS DASHBOARD'''
# Function to check if user is in "Teachers" group
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

# Login Page
def teacher_login(request):
    if request.user.is_authenticated:
        return redirect('teacher_dashboard')  # Redirect already logged-in users

    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user and is_teacher(user):
                login(request, user)
                return redirect('teacher_dashboard')
            else:
                messages.error(request, "Invalid credentials or not authorized")
    else:
        form = TeacherLoginForm()
    
    return render(request, 'staff/teacher_login.html', {'form': form})

#Careful this is not the same as the one in the studentviews.py
def sessionlist(request):
    sessions = Session.objects.all()
    return render(request, 'promote_students.html', {'sessions': sessions})



def teacher_logout(request):
    logout(request)
    return redirect('main_page')  # Redirect to login page after logout



@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    # Check if the user is authenticated and is a teacher
    if not request.user.is_authenticated or not is_teacher(request.user):
        messages.error(request, "You are not authorized to access this page.")
        return redirect('main_page')  # Redirect to home or login page

    try:
        # Retrieve the Teacher instance associated with the logged-in user
        teacher = request.user.teacher
    except Teacher.DoesNotExist:
        # Handle the case where the user is not associated with a Teacher instance
        messages.error(request, "No teacher profile found for this user.")
        return redirect('main_page')  # Redirect to home or login page

     # Use Django Guardian to get subjects assigned to the teacher based on object-level permissions
    subjects = get_objects_for_user(request.user, 'subjects.view_subject', klass=Subject).filter(teacher=teacher)

    return render(request, 'staff/teacher_dashboard.html', {'subjects': subjects})


# List sessions related to a subject
@login_required
@user_passes_test(is_teacher)
def subjectsession_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    sessions = subject.sesssion.all()  # Get sessions linked to the subject
    return render(request, 'session_list.html', {'sessions': sessions, 'subject': subject})

# List terms related to a session and subject
@login_required
@user_passes_test(is_teacher)
def term_list(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    terms = Term.objects.filter(Session=session)
    return render(request, 'term_list.html', {'terms': terms, 'session': session})

# List grades related to a term and subject
@login_required
@user_passes_test(is_teacher)
def grade_list(request, term_id):
    term = get_object_or_404(Term, id=term_id)
    grades = Grade.objects.filter(Term=term)
    return render(request, 'grade_list.html', {'grades': grades, 'term': term})

# Display student scores for a grade
@login_required
@user_passes_test(is_teacher)
def student_scores(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    subject_details = Subject.objects.filter(Grade=grade)
    
    if request.method == 'POST':
        for detail in subject_details:
            detail.FirstCA = request.POST.get(f'first_ca_{detail.id}', detail.FirstCA)
            detail.SecondCA = request.POST.get(f'second_ca_{detail.id}', detail.SecondCA)
            detail.Exam = request.POST.get(f'exam_{detail.id}', detail.Exam)
            detail.save()
        messages.success(request, "Scores updated successfully!")
    
    return render(request, 'student_scores.html', {'subject_details': subject_details, 'grade': grade})





