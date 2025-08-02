from django.shortcuts import render

# Create your views here.

def bells_view(req):
    return render(req, 'bells/index.html')