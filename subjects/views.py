from django.shortcuts import render, get_object_or_404
from .models import Subject, StudentResult
from student.models import Students_file
from results.models import Session, Term, Grade
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# Create your views here.

@login_required
def subject_sessions(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if not request.user.has_perm('view_subject', subject):
        return render(request, '403.html', status=403)
    
    sessions = subject.sesssion.all()
    
    return render(request, 'staff/subject_sessions.html', {
        'subject': subject,
        'sessions': sessions
    })

@login_required
def session_terms(request, subject_id, session_id):
    subject = get_object_or_404(Subject, id=subject_id)
    session = get_object_or_404(Session, id=session_id)
    if not request.user.has_perm('view_subject', subject):
        return render(request, '403.html', status=403)
    
    terms = subject.Term.filter(Session=session)
    for term in terms:
        term_id = term.id  
    return render(request, 'staff/session_terms.html', {
        'subject': subject,
        'session': session,
        'terms': terms,
        'subject_id': subject_id,  # Passing explicitly for URL construction
        'session_id': session_id,    # Passing explicitly for URL construction
        'term_id': term_id  # Ensure term_id is set for each term
    })

@login_required
def term_grades(request, subject_id, session_id, term_id):
    subject = get_object_or_404(Subject, id=subject_id)
    session = get_object_or_404(Session, id=session_id)
    term = get_object_or_404(Term, id=term_id)
    if not request.user.has_perm('view_subject', subject):
        return render(request, '403.html', status=403)
    
    grades = subject.Grade.filter(Term=term)
    
    return render(request, 'staff/term_grades.html', {
        'subject': subject,
        'session': session,
        'term': term,
        'grades': grades
    })

@login_required
def grade_scores(request, subject_id, session_id, term_id, grade_id):
    subject = get_object_or_404(Subject, id=subject_id)
    session = get_object_or_404(Session, id=session_id)
    term = get_object_or_404(Term, id=term_id)
    grade = get_object_or_404(Grade, id=grade_id)
    if not request.user.has_perm('view_subject', subject):
        return render(request, '403.html', status=403)
    
    students = Students_file.objects.filter(Grade=grade)
    results = StudentResult.objects.filter(
        subject=subject,
        grade=grade,
        term=term,
        session=session
    )

    # Create missing results (this ensures all students have a result entry)
    student_ids_with_results = results.values_list('student_id', flat=True)
    students_without_results = students.exclude(id__in=student_ids_with_results)
    for student in students_without_results:
        StudentResult.objects.create(
            student=student,
            subject=subject,
            grade=grade,
            term=term,
            session=session,
            first_ca=0,
            second_ca=0,
            exam=0
        )

    results = StudentResult.objects.filter(
        subject=subject,
        grade=grade,
        term=term,
        session=session
    )
    
    return render(request, 'staff/subjectgrade_scores.html', {
        'subject': subject,
        'session': session,
        'term': term,
        'grade': grade,
        'results': results
    })


@login_required
@require_POST
def save_scores(request):
    try:
        data = json.loads(request.body)
        response_data = []

        for score_data in data:
            result = StudentResult.objects.get(
                id=score_data['result_id']
            )
            result.first_ca = float(score_data['first_ca']) if score_data['first_ca'] else 0
            result.second_ca = float(score_data['second_ca']) if score_data['second_ca'] else 0
            result.exam = float(score_data['exam']) if score_data['exam'] else 0
            result.save()

            # If all scores are 0, delete the record (student not taking this subject)
            if result.first_ca == 0 and result.second_ca == 0 and result.exam == 0:
                result.delete()
                continue
            
            response_data.append({
                'result_id': result.id,
                'total': result.total
            })

        return JsonResponse({'status': 'success', 'results': response_data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)