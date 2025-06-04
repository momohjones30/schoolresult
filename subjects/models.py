from results.models import Grade, Term, Session
from student.models import Teacher, Students_file
from django.db import models





class Subject(models.Model):
    sesssion = models.ManyToManyField(Session, verbose_name = 'Session')
    Grade = models.ManyToManyField(Grade, verbose_name='Grades')
    Term = models.ManyToManyField(Term , verbose_name= 'Term')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    NameOfSubject = models.CharField(max_length=70, blank= False, verbose_name='Subject')
    students = models.ManyToManyField(Students_file, related_name='students')
   
    def __str__(self):
        return f'{self.NameOfSubject} for {self.Grade} of {self.sesssion} {self.Term}' 



class StudentResult(models.Model):
    student = models.ForeignKey(Students_file, on_delete=models.CASCADE, related_name='results')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='results')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='results')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    first_ca = models.FloatField(default=0, verbose_name='First CA')
    second_ca = models.FloatField(default=0, verbose_name='Second CA')
    exam = models.FloatField(default=0, verbose_name='Exam')
    total = models.FloatField(default=0, verbose_name='Total')

    def __str__(self):
        return f"Result for {self.student.FirstName} {self.student.LastName} in {self.subject.NameOfSubject} ({self.grade.Gradelevel} {self.grade.Arm}, {self.term.Term}, {self.session.AcademicSession})"

    def save(self, *args, **kwargs):
        # Calculate the total before saving
        self.total = self.first_ca + self.second_ca + self.exam
        
        # Call the parent class's save method to actually save the instance
        super().save(*args, **kwargs)
