from django.shortcuts import render

# Create your views here.



def portfolio_top(request):
    print("ログイン状態:", request.user.is_authenticated)  # ←これを追加
    return render(request, 'portfolio/top.html')
