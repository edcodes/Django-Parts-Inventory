from django.shortcuts import render


def home(request):
    
    return render(request, 'design/home.html', {'title': 'home'})
    
    











