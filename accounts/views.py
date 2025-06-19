from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # ログイン成功でホームへ
        else:
            error = "ユーザー名かパスワードが違います。"
            return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')


def signup_view(request): #ユーザーがフォームを送信（submit）したときは、リクエストが POST になる。form.is_valid() → バリデーション（未入力・形式エラーなど）をチェック。OKなら form.save() → データベースに新しいユーザーが保存される！
    if request.method == 'POST':
        form = SignUpForm(request.POST) #入力された内容を SignUpForm に渡す。
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  #登録完了後、ログイン画面（accounts:login）に移動。
    else:
        form = SignUpForm() #最初に画面を開いたとき（GET）は、空のフォームを表示するためにこの処理。

    return render(request, 'accounts/signup.html', {'form': form}) #signup.html テンプレートにフォームを送って、表示する。
# Create your views here.

def home_view(request):
    return HttpResponse("こんにちは！あなたの推し活をサポートします。")