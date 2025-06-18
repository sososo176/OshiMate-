from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/login.html')

def signup_view(request):  # ←追加(6/18)
    return render(request, 'accounts/signup.html')

# Create your views here.
