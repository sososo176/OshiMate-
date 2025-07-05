from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from items.models import Item  # ← items アプリにある Item モデルを使うため追加
from .forms import SignUpForm, ProfileForm  
from .models import Profile  
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import ProfileForm
from .forms import EmailChangeForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



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

#def home_view(request):
    #return HttpResponse("こんにちは！あなたの推し活をサポートします。")

def home_view(request):
    query = request.GET.get('q')  # URLパラメータから「q=検索キーワード」を取得
    category = request.GET.get('category')# URLパラメータからカテゴリを取得
    items = Item.objects.all()
    categories = Item.objects.values_list('category', flat=True).distinct()
    
    if query:
        items = Item.objects.filter(title__icontains=query)  # タイトルに部分一致するものを取得
    if category:
        items = items.filter(category=category)

   
    message = "こんにちは！あなたの推し活をサポートします。"

    return render(request, 'accounts/home.html',
                  {'items': items, 
                   'query': query, 
                    'category': category,#ユーザーが現在選択しているカテゴリ
                    'categories': categories,#全カテゴリ一覧（重複なし）
                   'message': message}) # ← メッセージをテンプレートに送る

# accounts/views.py


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            # 認証失敗
            return render(request, 'accounts/login.html', {'error': 'ログインできませんでした'})
    return render(request, 'accounts/login.html')


def mypage_view(request):
    return render(request, 'accounts/mypage.html')


@login_required
def profile_edit_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '保存されました')  # ← メッセージ追加
            return redirect('accounts:mypage')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def email_change_view(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['new_email']
            request.user.save()
            messages.success(request, 'メールアドレスを変更しました') 
            return redirect('accounts:mypage')
    else:
        form = EmailChangeForm()

    return render(request, 'accounts/email_change.html', {'form': form})


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'パスワードを変更しました。')
            return redirect('accounts:password_change_done')# 完了ページへ
    else:
        form = PasswordChangeForm(request.user)# 初回アクセス時：空のフォームを表示
    return render(request, 'accounts/password_change.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # ログアウト後にログイン画面に戻る



@login_required
def profile_edit_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:mypage')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})
