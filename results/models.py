from django.db import models
#from student.models import Students_file
#from subjects.models import Subject
# Create your models here.


GRADE = (
    ('Grade 1', 'Grade 1'),
    ('Grade 2', 'Grade 2'),
    ('Grade 3', 'Grade 3'),
    ('Grade 4', 'Grade 4'),
    ('Grade 5', 'Grade 5'),
    ('Grade 6', 'Grade 6'),
    ('Grade 7', 'Grade 7'),
    ('Grade 8', 'Grade 8'),
    ('Grade 9', 'Grade 9'),
    ('Grade 10', 'Grade 10'),
    ('Grade 11', 'Grade 11'),
    ('Grade 12', 'Grade 12'),
)


Term = (
    ('First Term', 'First Term'),
    ('Second Term', 'Second Term'),
    ('Third Term', 'Third Term'),
)

class Session(models.Model):
    AcademicSession = models.CharField(max_length=200, null = True, default='2023/2024', blank= False, help_text='Example, 2023/2024', verbose_name='Academic Session' )
    
    def __str__(self):
        return self.AcademicSession

class Term(models.Model):
    Session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, related_name='terms')
    Term = models.TextField(choices= Term, help_text='Term', verbose_name= 'Term', default='First Term')

    def __str__(self):
        return f'{self.Term} of {self.Session}' 


class Grade(models.Model):
    Term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='grade')
    Gradelevel = models.TextField(choices= GRADE, help_text='Grade or Class', verbose_name= 'Grade')
    Arm = models.TextField(help_text='Arm of grade if any')
    
    def __str__(self):
        return f'{self.Gradelevel} {self.Arm} of {self.Term}'


