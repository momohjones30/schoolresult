from django.contrib import admin
from results.models import Session, Term, Grade
from subjects.models import Subject
from django.template.response import TemplateResponse
from student.models import Students_file
from django.contrib.auth.models import Group
from django.urls import path




'''class staffadmin(admin.AdminSite):
    site_header = 'Academic Staff Administration'
    site_title  = "Staff Admin Portal"
    index_title = "Welcome to Staff Admin Dashboard"
 
    def has_permission(self, request):
        # Allow only users in the "Staff" group
        #return request.user.is_active and request.user.is_staff and request.user.groups.filter(name='Staff').exists()
        return request.user.is_authenticated and Group.objects.get(name='Teacher') in request.user.groups.all()
        #return request.user.is_authenticated and getattr(request.user, 'role', None) == 'TEACHER'
        
    
    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        # Initialize variables with default values
        # extra_context = extra_context or {}

        sessions = Session.objects.all()
        terms = Term.objects.none()  # Initialize as an empty queryset
        grades = Grade.objects.none()  # Initialize as an empty queryset
        subjects = Subject.objects.none() # Initialize as an empty queryset

        session_id = request.GET.get('session_id', None)    # gets the session id of the clicked session
        term_id = request.GET.get('term_id', None)
        grade_id = request.GET.get('grade_id', None)
        subjects_id= request.GET.get('subjects_id', None)
        #print(session_id, term_id, grade_id, subjects_id )

        extra_context =  {
            'sessions': sessions,
            'terms': terms,
            'grades': grades,
            'subjects': subjects,
             }

        if session_id:
            terms = Term.objects.filter(Session_id=session_id)      # Access related terms
            sessions = Session.objects.get(id=session_id) # Retrieve the specific session
            extra_context =  {
            'sessionss': sessions, #  extra s for the sake of passing the sessions.AcademicSession into the template preventing 'Session' object is not iterable
            'terms': terms,
             }
            #print(f"Session ID for index: {session_id}, Term ID: {term_id}, Grade ID: {grade_id}")

        if term_id:
            term = Term.objects.get(id=term_id)
            session = term.Session 
            grades = Grade.objects.filter(Term=term)
            extra_context =  {
            'sessionss': session,
            'termss': term,    #extra s for the sake of passing the termss.term into the template
            'grades': grades,
             } 
            #print(f"Session ID (none or value): {session_id}, Term ID for index: {term_id}, Grade ID: {grade_id}")

        if grade_id:
            grade = Grade.objects.get(id=grade_id)
            term = grade.Term
            session = term.Session 
            subjects = Subject.objects.filter(Grade=grade)
            #subjects = grades.subject_set.all()  # Access related subjects for manytomany relationships
            extra_context =  {
                'sessionss': session,
                'termss': term, 
                'grade': grade,
                'subjects': subjects,
            }
            #print(f"Session ID (none or value): {session_id}, Term ID: {term_id}, Grade ID for index: {grade_id}")


        if subjects_id:
            grades = Grade.objects.get(id=grade_id)
            subjects = grades.subject_set.all()  # Access related subjects for manytomany relationships
            extra_context =  {
                'grades': grades,
                'subjects': subjects,
            }
            #print(f"Session ID (none or value): {session_id}, Term ID: {term_id}, Grade ID: {grade_id}, Subject ID for index: {grade_id}")


        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            #"title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or "admin/index.html", context)
    
# Instantiate the custom admin site
staffadminsite = staffadmin(name="Academic Staff Admin")
'''

class StudentAdmin(admin.AdminSite):

    site_header = 'Student Administration'
    site_title  = "Student Portal"
    index_title = "Student Dashboard"

    def has_permission(self, request):
        # Allow only users in the "Student" group
        return request.user.is_authenticated and Group.objects.get(name='Student') in request.user.groups.all()
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.index), name='student_dashboard'),
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
       
        try:
            student_profile = request.user.profile  # Access the OneToOne relationship in Students_file
        except Students_file.DoesNotExist:
            extra_context = {'error': 'No profile found for this student.'}
            return TemplateResponse(request, self.index_template or "admin/studentindex.html", extra_context)

        session_id = request.GET.get('session_id', None)    # gets the session id of the clicked session
        term_id = request.GET.get('term_id', None)
        grade_id = request.GET.get('grade_id', None)

        
        if hasattr(request.user, 'profile'):  # Assuming student have a related profile
            student_profile = request.user.profile  #This means each User has one Students_file, which can be accessed via user.profile.
            #sessions = Session.objects.filter(profile=student_profile)
            sessions = student_profile.sessions.all()
            terms = Term.objects.none()
            grades = Grade.objects.none()
            subjects = Subject.objects.none()
            performance_data = []
                        
            if session_id:
                terms = Term.objects.filter(Session_id=session_id, profile=student_profile)      # Access related terms
                sessions = Session.objects.get(id=session_id) # Retrieve the specific session
                extra_context =  {
                'sessionss': sessions, #  extra s for the sake of passing the sessions.AcademicSession into the template preventing 'Session' object is not iterable
                'terms': terms,
                }

            if term_id:

                term = Term.objects.get(id=term_id, profile=student_profile)
                session = term.Session 
                extra_context =  {
                'sessionss': session,
                'termss': term,    #extra s for the sake of passing the termss.term into the template
                } 

        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            #"title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or "admin/studentindex.html", context)
    
studentsite = StudentAdmin(name="StudentAdmin")
studentsite.register(Students_file)


