from django.contrib import admin
from .forms import GradeAdminForm, SessionAdminForm
from .models import Session, Grade, Term
from django.utils.html import format_html
from django.urls import reverse




class SessionAdmin(admin.ModelAdmin):#shows the sessions in the admin panel, registered below, from results/models
    form = SessionAdminForm   #from results/forms
    list_display = ('AcademicSession', 'terms_link', 'grades_link')  
    
    def terms_link(self, obj):
        url = reverse('admin:results_term_changelist')  # Replace app_name with your app's name
        return format_html('<a href="{}?Session__id__exact={}">View Terms</a>', url, obj.id)
    terms_link.short_description = 'Terms for the Academic Session'

    def grades_link(self, obj):
        url = reverse('admin:results_grade_changelist')  # Replace app_name with your app's name
        return format_html('<a href="{}?Term__id__exact={}">View Grades</a>', url, obj.id)
        #return format_html('<a href="{}?Session__id__exact={}">View Grades</a>', url, obj.id)

    grades_link.short_description = 'Grades'





class TermAdmin(admin.ModelAdmin):
    list_display = ('Session', 'Term')
    ordering = ('-Session', '-Term')  # Adjust ordering as needed




class GradeAdmin(admin.ModelAdmin):#shows the grades in the admin panel, registered below,  from results/models
    form = GradeAdminForm   #from results/forms
    list_display = ('Gradelevel' ,'Term', 'Arm', 'students_link', 'subjects_link' )  
    ordering = ('-Term', '-Gradelevel')  # Adjust ordering as needed

    def students_link(self, obj):
        url = reverse('admin:student_students_file_changelist')  # Replace app_name with your app's name
        #return format_html('<a href="{}?Grade__id__exact={}">View Students</a>', url, obj.id)  this was used when foreignkey b/w grade and students
        return format_html('<a href="{}?Grade__id__contains={}">View Students</a>', url, obj.id) # used for manytomany relationship
    
    students_link.short_description = 'Students'


    def subjects_link(self, obj):
        url = reverse('admin:subjects_subject_changelist')  # Replace app_name with your app's name
        return format_html('<a href="{}?Grade__id__exact={}">View Subjects</a>', url, obj.id)
    
    subjects_link.short_description = 'Subjects'


admin.site.register(Session, SessionAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Term, TermAdmin)


