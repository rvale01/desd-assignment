from django.http import JsonResponse
from django.shortcuts import render

def homepage(request):
    return render(
        request,
        'general/homepage.html'
    )