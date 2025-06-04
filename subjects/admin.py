from django.contrib import admin
from .forms import SubjectAdminForm
from results.forms import StudentAdminForm
from django.conf import settings
from student.models import Students_file
from .models import Subject
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user


''''
#subject model student/model
class SubjectAdmin(admin.ModelAdmin): 
    form = SubjectAdminForm    #from subject/forms 
    list_display = ('NameOfSubject', 'get_student')
    list_filter = ('NameOfSubject', 'teacher')
    
    def get_student(self, obj):
        # Return a comma-separated string of student associated with the subject
        return ", ".join(student.Name for student in obj.students.all())
    get_student.short_description = 'Enrolled Students'
admin.site.register(sub.Subject, SubjectAdmin) 
'''

@admin.register(Subject)
class SubjectAdmin(GuardedModelAdmin):
    form = SubjectAdminForm  # Use the custom form
    list_display = ('NameOfSubject', 'teacher')
    list_filter = ('teacher', 'Grade', 'Term')
    search_fields = ('NameOfSubject',)



class Students_fileAdmin(admin.ModelAdmin):
    form = StudentAdminForm   #from results/form
    list_display = ('FirstName', 'LastName', 'parents')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Add a help text to the firstname field
        form.base_fields['FirstName'].help_text = 'Ensure the student is already registered as a user befor filling his/her details.'
        return form
    
admin.site.register(Students_file, Students_fileAdmin)

