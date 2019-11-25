from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    html = 'CodeClassroom API.<br/>Go to <a href="api"><code>api/</code></a> for the full list of end-points.'
    return HttpResponse(html)


def docs(request):
	return render(request, 'docs.html')