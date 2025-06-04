from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from results.models import Session, Term, Grade
from student.models import Students_file
from django.contrib import messages

def promotion_home(request):
    sessions = Session.objects.all()
    return render(request, 'promotion/home.html', {'sessions': sessions})

def session_grades(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    # Get third term grades for this session
    third_term = Term.objects.filter(Session=session, Term='Third Term').first()
    grades = Grade.objects.filter(Term=third_term) if third_term else []
    return render(request, 'promotion/grades.html', {
        'grades': grades,
        'session': session
    })

def grade_students(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    students = Students_file.objects.filter(Grade=grade)
    return render(request, 'promotion/students.html', {
        'students': students,
        'grade': grade
    })

def new_session_selection(request):
    if request.method == 'POST':
        request.session['selected_students'] = request.POST.getlist('students')
        sessions = Session.objects.all()
        return render(request, 'promotion/new_session.html', {'sessions': sessions})
    return redirect('promotion_home')

def new_grade_selection(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    grades = Grade.objects.filter(Term__Session=session)
    return render(request, 'promotion/new_grades.html', {
        'grades': grades,
        'session': session
    })

def promotionsuccess(request):
    return render(request, 'promotion/success.html', {
        'message': 'If you are seeing this page, promotion was successful',
        'buttons': [
            {'text': 'Return to Homepage', 'url': 'main_page'},
            {'text': 'Promote Another Set of Students', 'url': 'promotion_home'}
        ]
    })



def promote_students(request):
    if request.method == 'POST':
        student_ids = request.session.get('selected_students', [])
        new_grade_ids = request.POST.getlist('new_grades')
        
        if not student_ids or not new_grade_ids:
            messages.error(request, "No students or grades selected")
            return redirect('promotion_home')
        
        students = Students_file.objects.filter(id__in=student_ids)
        new_grades = Grade.objects.filter(id__in=new_grade_ids)
        
        for student in students:
            student.Grade.add(*new_grades)
        
        messages.success(request, f"Successfully promoted {len(students)} students to {len(new_grades)} new grades")
        return redirect('promotionsuccess')
    
    return redirect('promotion_home')