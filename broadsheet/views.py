from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from results.models import Session, Term, Grade
from student.models import Students_file
from subjects.models import Subject, StudentResult
from django.views.generic import View
from django.template.loader import get_template
from xhtml2pdf import pisa
import openpyxl
from io import BytesIO
from django.db.models import Sum, Avg

def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'broadsheet/session_list.html', {'sessions': sessions})

def term_list(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    terms = session.terms.all()
    return render(request, 'broadsheet/term_list.html', {'terms': terms, 'session': session})

def grade_list(request, session_id, term_id):
    term = get_object_or_404(Term, pk=term_id)
    grades = term.grade.all()
    return render(request, 'broadsheet/grade_list.html', {'grades': grades, 'term': term, 'session_id': session_id})

def broadsheet_view(request, session_id, term_id, grade_id):
    grade = get_object_or_404(Grade, pk=grade_id)
    students = Students_file.objects.filter(Grade=grade)
    subjects = Subject.objects.filter(Grade=grade, Term__id=term_id)
    
    # Prepare student data with their results
    student_data = []
    for student in students:
        student_results = []
        total_score = 0
        subject_count = 0
        
        for subject in subjects:
            try:
                result = StudentResult.objects.get(
                    student=student,
                    grade=grade,
                    term_id=term_id,
                    subject=subject
                )
                student_results.append(result.total)
                total_score += result.total
                subject_count += 1
            except StudentResult.DoesNotExist:
                student_results.append('-')
        
        average = total_score / subject_count if subject_count > 0 else 0
        student_data.append({
            'student': student,
            'results': student_results,
            'total': total_score,
            'average': round(average, 2)
        })
    
    context = {
        'grade': grade,
        'subjects': subjects,
        'student_data': student_data,
        'session_id': session_id,
        'term_id': term_id,
        'grade_id': grade_id,

    }
    
    return render(request, 'broadsheet/broadsheet.html', context)

class DownloadBroadsheetPDF(View):
    def get(self, request, session_id, term_id, grade_id):
        grade = get_object_or_404(Grade, pk=grade_id)
        students = Students_file.objects.filter(Grade=grade)
        subjects = Subject.objects.filter(Grade=grade, Term__id=term_id)
        
        # Prepare student data (same as broadsheet_view)
        student_data = []
        for student in students:
            student_results = []
            total_score = 0
            subject_count = 0
            
            for subject in subjects:
                try:
                    result = StudentResult.objects.get(
                        student=student,
                        grade=grade,
                        term_id=term_id,
                        subject=subject
                    )
                    student_results.append(result.total)
                    total_score += result.total
                    subject_count += 1
                except StudentResult.DoesNotExist:
                    student_results.append('-')
            
            average = total_score / subject_count if subject_count > 0 else 0
            student_data.append({
                'student': student,
                'results': student_results,
                'total': total_score,
                'average': round(average, 2)
            })
        
        context = {
            'grade': grade,
            'subjects': subjects,
            'student_data': student_data,
        }
        
        template = get_template('broadsheet/broadsheet_pdf.html')
        html = template.render(context)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{grade}_broadsheet.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF')
        
        return response

class DownloadBroadsheetExcel(View):
    def get(self, request, session_id, term_id, grade_id):
        grade = get_object_or_404(Grade, pk=grade_id)
        students = Students_file.objects.filter(Grade=grade)
        subjects = Subject.objects.filter(Grade=grade, Term__id=term_id)
        
        # Create workbook and worksheet
        output = BytesIO()
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = f"{grade.Gradelevel} {grade.Arm}"
        
        # Create headers
        headers = ["Student Name"]
        for subject in subjects:
            headers.append(subject.NameOfSubject)
        headers.extend(["Total", "Average"])
        
        worksheet.append(headers)
        
        # Add student data
        for student in students:
            row = [f"{student.FirstName} {student.LastName}"]
            total_score = 0
            subject_count = 0
            
            for subject in subjects:
                try:
                    result = StudentResult.objects.get(
                        student=student,
                        grade=grade,
                        term_id=term_id,
                        subject=subject
                    )
                    row.append(result.total)
                    total_score += result.total
                    subject_count += 1
                except StudentResult.DoesNotExist:
                    row.append('-')
            
            average = total_score / subject_count if subject_count > 0 else 0
            row.extend([total_score, round(average, 2)])
            
            worksheet.append(row)
        
        workbook.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{grade}_broadsheet.xlsx"'
        
        return response