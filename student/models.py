from django.db import models
from results.models import Grade, Term, Session
from parents.models import Parent
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


class Students_file(models.Model):
    # from django.conf import settings

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=False, null=True, related_name='profile', verbose_name="Username")
    FirstName = models.CharField(max_length=200, null = True, blank= False, help_text='First name')
    LastName = models.CharField(max_length=200, null = True, blank= False, help_text='Last name')
    DateofBirth = models.DateField(editable= True, null= True, blank=True, verbose_name= 'Date of Birth')
    term = models.ManyToManyField(Term, verbose_name="Term", related_name='profile')
    Grade = models.ManyToManyField(Grade, verbose_name="Grade at entry", related_name='profile') # null=True allows the foreign key to be NULL,
    Passportphoto = models.ImageField(upload_to='passport_photos/', blank=True, null=True)
    parents = models.ForeignKey(Parent, on_delete=models.DO_NOTHING, null=True, related_name='children')
    DateofEntry = models.DateField(editable= True, verbose_name= 'Date of Entry', null= True)
    DateofExit = models.DateField(editable= True, verbose_name= 'Date of Exit', null= True, blank=True)
    DateofGraduation = models.DateField(editable= True, verbose_name= 'Date of Graduation', null= True, blank=True)
    sessions = models.ManyToManyField(Session, verbose_name="Present Session", related_name='profile')

    def __str__(self):
            return self.FirstName + self.LastName
    


class Teacher(models.Model):    # had to put this model here to avoid circular error, registered in student/admin
    # from django.conf import settings
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Username")
    Name = models.CharField(max_length=100)
    phonenumber = models.CharField (max_length=20, help_text='Phone number')

    def __str__(self):
        return self.Name


@receiver(m2m_changed, sender=User.groups.through)
def update_teacher_profile_on_group_change(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        teacher_group = Group.objects.get(name='Teacher')
        if teacher_group in instance.groups.all():
            # Create or update a Teacher profile for the user
            Teacher.objects.update_or_create(
                user=instance,
                defaults={
                    'Name': f"{instance.first_name} {instance.last_name}",  # Combine first and last name
                    'phonenumber': instance.Teacher.phonenumber if hasattr(instance, 'Teacher') else "",  # Keep existing phone number if available
                }
            )
            # Set the user as staff
            instance.is_staff = True
            instance.save()
        else:
            # If the user is not in the Teacher group, delete the Teacher profile if it exists
            if hasattr(instance, 'Teacher'):
                instance.Teacher.delete()
            # Remove staff status
            instance.is_staff = False
            instance.save()