from django.contrib import admin
from . models import Question, Assignment, Classroom, Student, Professor

admin.site.register(Classroom)
admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(Professor)