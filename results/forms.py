from django import forms
from .models import Grade, Session, Term
from student.models import Students_file
from django.core.exceptions import ValidationError

class GradeAdminForm(forms.ModelForm): #used in result/admin
    class Meta:
        model = Grade
        fields = '__all__'
    
    # Customize the widget for the TextField
    Arm = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 1, 'cols': 10})  # Adjust rows and cols as needed
    )

    #Displaying all sessions in a non-editable way
    # Available_grades = forms.ModelMultipleChoiceField(
    #     queryset=Grade.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,   #Or another widget that suits your design
    #     required=False,
    #     #disabled=True  # This makes the field non-editable
    # )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Check if the instance is already saved
            self.fields['Gradelevel'].queryset = Grade.objects.filter(Gradelevel=self.instance)




class SessionAdminForm(forms.ModelForm): #used in result/admin
    class Meta:
        model = Session
        fields = '__all__'

    #Displaying all sessions in a non-editable way
    sessions = forms.ModelMultipleChoiceField(
        queryset=Session.objects.all(),
        widget=forms.CheckboxSelectMultiple,   #Or another widget that suits your design
        required=False,
        #disabled=True  # This makes the field non-editable
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Check if the instance is already saved
            self.fields['AcademicSession'].queryset = Term.objects.filter(Session=self.instance)



class StudentAdminForm(forms.ModelForm): #used in subject/admin
    class Meta:
        model = Students_file
        fields = ['user','FirstName', 'LastName', 'DateofBirth', 'Passportphoto', 
                  'Grade', 'DateofEntry', 'parents', 'DateofGraduation', 'DateofExit']

    # def clean_user(self):
    #     user = self.cleaned_data.get('user')
    #     if Students_file.objects.filter(user=user).exists():
    #         raise ValidationError("A StudentsFile for this user already exists.")
    #     return user
    


#This shows the clickable subjects available for the grade when registering a student
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # When editing an instance, pre-fill the subjects field with the current grade's subjects
    #     if 'Grade' in self.data:
    #         try:
    #             grade_id = int(self.data.get('Grade'))
    #             self.fields['subjects'].queryset = Subject.objects.filter(id=grade_id)
    #         except (ValueError, TypeError):
    #             self.fields['subjects'].queryset = Subject.objects.none()
    #     elif self.instance.pk:
    #         self.fields['subjects'].help_text = 'No subject assigned because no grade assigned'
