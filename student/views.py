from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Avg
from student.models import Students_file
from results.models import Session, Term, Grade
from subjects.models import StudentResult
from .forms import StudentLoginForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from subjects.models import Subject

def is_student(user):
    return user.groups.filter(name='Student').exists()

# Authentication views
def student_login(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if is_student(user):
                login(request, user)
                return redirect('student_dashboard')
        messages.error(request, "Invalid credentials")
    return render(request, 'student_login.html', {'form': StudentLoginForm()})

def student_logout(request):
    logout(request)
    return redirect('main_page')

# Main dashboard view
@login_required
def student_dashboard(request):
    try:
        student = Students_file.objects.get(user=request.user)
        sessions = Session.objects.filter(
            terms__grade__profile=student
        ).distinct().order_by('-AcademicSession')
        return render(request, 'dashboard/student_dashboard.html', {
            'student': student,
            'sessions': sessions
        })
    except Students_file.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect('main_page')

# Academic hierarchy views
@login_required
def session_terms(request, session_id):
    studentname = Students_file.objects.get(user=request.user)
    student = get_object_or_404(Students_file, user=request.user)
    session = get_object_or_404(Session, id=session_id)
    terms = Term.objects.filter(Session=session, grade__profile=student).distinct()
    return render(request, 'dashboard/session_terms.html', {
        'student': student,
        'session': session,
        'terms': terms
    })      

@login_required
def term_grades(request, session_id, term_id):
        student = get_object_or_404(Students_file, user=request.user)
        session = get_object_or_404(Session, id=session_id)
        term = get_object_or_404(Term, id=term_id, Session=session)
        grades = Grade.objects.filter(Term=term, profile=student)
        return render(request, 'dashboard/term_grades.html', {
            'student': student,
            'session_id': session.id,
            'session': session,
            'term': term,
            'grades': grades
        })






def get_letter_grade(score):
    if score is None: return '-'
    if score >= 75: return 'A'
    elif score >= 60: return 'B'
    elif score >= 50: return 'C'
    elif score >= 40: return 'D'
    else: return 'F'

def get_letter_grade(score):
    if score is None: return '-'
    if score >= 75: return 'A'
    elif score >= 60: return 'B'
    elif score >= 50: return 'C'
    elif score >= 40: return 'D'
    else: return 'F'


@login_required
def grade_performance(request, session_id, term_id, grade_id):
    student = get_object_or_404(Students_file, user=request.user)
    grade = get_object_or_404(Grade, id=grade_id, Term_id=term_id)
    
    # Get all subjects for this grade
    all_subjects = Subject.objects.filter(Grade=grade)
    
    # Get existing results for this student
    existing_results = StudentResult.objects.filter(
        student=student,
        grade=grade
    ).select_related('subject', 'term', 'session')
    
    # Create a dictionary of existing results for quick lookup
    results_dict = {result.subject.id: result for result in existing_results}
    
    # Prepare performance data for all subjects
    performance_data = []
    subjects_with_scores = []
    
    for subject in all_subjects:
        result = results_dict.get(subject.id)
        
        if result:
            # Student has results for this subject
            performance_data.append({
                'subject': subject,
                'subject_id': subject.id,
                'first_ca': result.first_ca,
                'second_ca': result.second_ca,
                'exam': result.exam,
                'total': result.total,
                'grade': get_letter_grade(result.total),
                'has_score': True
            })
            subjects_with_scores.append(result.total)
        else:
            # Student doesn't have results for this subject
            performance_data.append({
                'subject': subject,
                'subject_id': subject.id,
                'first_ca': '-',
                'second_ca': '-',
                'exam': '-',
                'total': None,
                'grade': '-',
                'has_score': False
            })
    
    # Calculate summary statistics only for subjects with scores
    summary = {
        'average': sum(subjects_with_scores)/len(subjects_with_scores) if subjects_with_scores else None,
        'best_subject': max(performance_data, key=lambda x: x['total'] if x['has_score'] else -1) if subjects_with_scores else None,
        'weakest_subject': min(performance_data, key=lambda x: x['total'] if x['has_score'] else 101) if subjects_with_scores else None
    }

    if request.GET.get('format') == 'pdf':
        return generate_pdf_report(student, grade, performance_data, summary)
    elif request.GET.get('format') == 'excel':
        return generate_excel_report(student, grade, performance_data, summary)

    return render(request, 'dashboard/grade_performance.html', {
        'student': student,
        'grade': grade,
        'performance_data': performance_data,
        'summary': summary,
        'session_id': session_id,
        'term_id': term_id,
        'grade_id': grade_id
    })


'''
@login_required
def grade_performance(request, session_id, term_id, grade_id):
    student = get_object_or_404(Students_file, user=request.user)
    grade = get_object_or_404(Grade, id=grade_id, Term_id=term_id)
    results = StudentResult.objects.filter(
        student=student,
        grade=grade
    ).select_related('subject', 'term', 'session')

    performance_data = []
    subjects_seen = set()

    for result in results:
        if result.subject.id in subjects_seen:
            continue
        subjects_seen.add(result.subject.id)

        performance_data.append({
            'subject': result.subject,
            'subject_id': result.subject.id,
            'first_ca': result.first_ca,
            'second_ca': result.second_ca,
            'exam': result.exam,
            'total': result.total,
      
            'grade': get_letter_grade(result.total),
            'session_id': session_id,
            'term_id': term_id,
            'grade_id': grade_id
        })

    summary = {
        'average': results.aggregate(Avg('total'))['total__avg'],
        'best_subject': max(performance_data, key=lambda x: x['total']) if performance_data else None,
        'weakest_subject': min(performance_data, key=lambda x: x['total']) if performance_data else None
    }

    if request.GET.get('format') == 'pdf':
        return generate_pdf_report(student, grade, performance_data, summary)
    elif request.GET.get('format') == 'excel':
        return generate_excel_report(student, grade, performance_data, summary)

    return render(request, 'dashboard/grade_performance.html', {
        'student': student,
        'grade': grade,
        'performance_data': performance_data,
        'summary': summary,
        'session_id': session_id,
        'term_id': term_id,
        'grade_id': grade_id

    })
'''


def generate_pdf_report(student, grade, performance_data, summary):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.LastName}_{student.FirstName}_{grade}_performance.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title and Student Info
    story.append(Paragraph(f"Student Performance Report", styles['h1']))
    story.append(Paragraph(f"Student: {student.FirstName} {student.LastName}", styles['h2']))
    story.append(Paragraph(f"Grade: {grade.Gradelevel} {grade.Arm}", styles['h2']))
    story.append(Paragraph(f"Term: {grade.Term.Term}, Session: {grade.Term.Session.AcademicSession}", styles['h2']))
    story.append(Paragraph(" ", styles['Normal']))  # Add some space

    # Summary Table
    summary_data = [
        ['Metric', 'Value'],
        ['Average Score', f"{summary['average']:.2f}" if summary['average'] else "-"],
        ['Best Subject', summary['best_subject']['subject'].NameOfSubject if summary['best_subject'] else "-"],
        ['Weakest Subject', summary['weakest_subject']['subject'].NameOfSubject if summary['weakest_subject'] else "-"]
    ]
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(summary_table)
    story.append(Paragraph(" ", styles['Normal']))

    # Performance Data Table
    data = [['Subject', 'First CA', 'Second CA', 'Exam', 'Total', 'Grade']]
    for result in performance_data:
        data.append([
            result['subject'].NameOfSubject,
            result['first_ca'] if result['first_ca'] is not None else "-",
            result['second_ca'] if result['second_ca'] is not None else "-",
            result['exam'] if result['exam'] is not None else "-",
            result['total'] if result['total'] is not None else "-",
            result['grade'] if result['grade'] else "-"
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.royalblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)

    doc.build(story)
    return response

def generate_excel_report(student, grade, performance_data, summary):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{student.LastName}_{student.FirstName}_{grade}_performance.xlsx"'
    wb = Workbook()
    sheet = wb.active

    # Title and Student Info
    sheet.append([f"Student Performance Report"])
    sheet.append([f"Student: {student.FirstName} {student.LastName}"])
    sheet.append([f"Grade: {grade.Gradelevel} {grade.Arm}"])
    sheet.append([f"Term: {grade.Term.Term}, Session: {grade.Term.Session.AcademicSession}"])
    sheet.append([])  # Empty row for spacing

    # Summary Table
    sheet.append(["Performance Summary"])
    sheet.append(['Metric', 'Value'])
    sheet.append(['Average Score', f"{summary['average']:.2f}" if summary['average'] else "-"])
    sheet.append(['Best Subject', summary['best_subject']['subject'].NameOfSubject if summary['best_subject'] else "-"])
    sheet.append(['Weakest Subject', summary['weakest_subject']['subject'].NameOfSubject if summary['weakest_subject'] else "-"])
    sheet.append([])

    # Performance Data Table
    sheet.append(["Subject Results"])
    header = ['Subject', 'First CA', 'Second CA', 'Exam', 'Total', 'Grade']
    sheet.append(header)

    for result in performance_data:
        row = [
            result['subject'].NameOfSubject,
            result['first_ca'] if result['first_ca'] is not None else "-",
            result['second_ca'] if result['second_ca'] is not None else "-",
            result['exam'] if result['exam'] is not None else "-",
            result['total'] if result['total'] is not None else "-",
            result['grade'] if result['grade'] else "-"
        ]
        sheet.append(row)

    # Styling (Basic)
    for cell in sheet["1:1"]:
        cell.font = Font(bold=True, size=16)
    for cell in sheet["6:6"]:
        cell.font = Font(bold=True)
    for cell in sheet["11:11"]:
        cell.font = Font(bold=True)

    wb.save(response)
    return response

