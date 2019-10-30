'''API views using mostly ModelViewSet.'''
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from app.models import Professor
from app.serializers import ProfessorSerializer

@api_view(['GET',])
def index(request):
    '''API root for CodeClassroom.'''
    return Response({
        'professors': reverse('professor-list', request=request),
    })

class ProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorSerializer
    queryset = Professor.objects.all()
