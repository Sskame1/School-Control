from django.shortcuts import render

# Create your views here.

def facepass_view(req):
    return render(req, 'facepass/index.html')