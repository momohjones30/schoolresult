from django import forms
from django.contrib.auth.models import User, Group
from student.models import Students_file
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
            user = super().save(commit=False)
            user.is_staff = True  # Make user staff
            if commit:
                user.save()

            # Add user to 'students' group (create the group if it doesn't exist)
            try:
                students_group = Group.objects.get(name='Student')
            except Group.DoesNotExist:
                students_group = Group.objects.create(name='Student') # Corrected: Use Group.create()
                students_group.save()
                
            user.groups.add(students_group)  # Add user to the group
            return user

class TeacherCustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
            user = super().save(commit=False)
            user.is_staff = True  # Make user staff
            if commit:
                user.save()

            # Add user to 'teachers' group (create the group if it doesn't exist)
            try:
                teachers_group = Group.objects.get(name='Teacher')
            except Group.DoesNotExist:
                teachers_group = Group.objects.create(name='Teacher') # Corrected: Use Group.create()
                teachers_group.save()
                
            user.groups.add(teachers_group)  # Add user to the teachers group
            return user





class StudentRegistrationForm(forms.ModelForm):

    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    DateofBirth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    DateofEntry = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Students_file
        fields = ['username', 'FirstName', 'LastName', 'DateofBirth', 'Passportphoto', 'DateofEntry']

    # def save(self, commit=True):
    #     student = super().save(commit=False)
    #     student.user = user  # Link the student to the user account
    #     if commit:
    #         student.save()
    #     return student


class TeacherLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

