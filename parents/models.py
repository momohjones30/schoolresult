from django.db import models


class Parent(models.Model):                     #model for the file of a parent, registered in student/admin
    Name = models.CharField(max_length=200, null = False, blank= False)
    Phonenumber = models.CharField(max_length=11, help_text='Local phone number', verbose_name='Phone number 1', blank=False)
    Phonenumber2 = models.CharField(blank=True, max_length=20, help_text='Other phone number, if any', verbose_name='Phone number 2')
    Address = models.TextField(max_length=200, verbose_name='Home Address', blank=True)

    def __str__(self):
        return self.Name
