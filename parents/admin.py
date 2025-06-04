from django.contrib import admin
from student.models import Teacher
from parents.models import Parent

# Register your models here.



class ParentAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Phonenumber', 'get_children')
    search_fields = ('Name', 'Phonenumber')
    def get_children(self, obj):
        # Return a comma-separated string of children associated with the parent
        return ", ".join(child.FirstName for child in obj.children.all())
    get_children.short_description = 'Children'


admin.site.register(Parent, ParentAdmin)
admin.site.register(Teacher)