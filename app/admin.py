from django.contrib import admin
from . models import Question, Assignment, Classroom, Student, Professor, Institution, Solution

admin.site.register(Classroom)
admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Institution)
admin.site.register(Solution)