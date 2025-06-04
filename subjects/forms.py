from django import forms
from student.models import Students_file
from subjects.models import Subject

#Code for what and how what is displayed for subject model in subject app 
class SubjectAdminForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['sesssion', 'Term','Grade', 'NameOfSubject', 'teacher']

   

'''LEARN AND KEEP THIS HERE
from django import forms
from django.contrib import admin
from .models import Subject

class SubjectAdminForm(forms.ModelForm):
    extra_field = forms.CharField(required=False)  # Custom field not in the model

    class Meta:
        model = Subject
        fields = ['sesssion', 'Grade', 'Term', 'NameOfSubject', 'teacher', 'students']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Do something with the extra_field
        extra_field_value = self.cleaned_data.get('extra_field')
        if commit:
            instance.save()
        return instance

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    form = SubjectAdminForm  # Use the custom form
    list_display = ('NameOfSubject', 'teacher')
    list_filter = ('teacher', 'Grade', 'Term')
    search_fields = ('NameOfSubject',)
'''


