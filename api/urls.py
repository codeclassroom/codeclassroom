from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('user', views.UserViewSet)
router.register('student', views.StudentViewSet)
router.register('professor', views.ProfessorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
