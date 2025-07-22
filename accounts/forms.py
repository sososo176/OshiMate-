from django import forms
from django.contrib.auth.forms import UserCreationForm #Djangoが用意したユーザー登録フォーム（UserCreationForm）を元に自分用フォームを作るための準備。
from django.contrib.auth.models import User #Userは、Djangoの**「ユーザー情報を保存するモデル（テーブル）」
import re
from .models import Profile
from django.contrib.auth import authenticate




GENDER_CHOICES = [
    ('男性', '男性'),
    ('女性', '女性'),
    ('その他', 'その他'),
]
#SignUpForm は、Djangoの UserCreationForm をカスタマイズした「自分用の登録フォーム」。email = ... の部分で、「メールアドレスも入力必須にする」という追加設定をしている。

class SignUpForm(UserCreationForm):
    username = forms.CharField(
    label="ユーザー名",
    max_length=150,
    help_text=""
)

    email = forms.EmailField(label="メールアドレス", required=True)
    gender = forms.ChoiceField(label="性別", choices=GENDER_CHOICES)
    birthdate = forms.DateField(label="生年月日", widget=forms.DateInput(attrs={'type': 'date'}))
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        help_text="英数字を含む8〜24文字"
    )
    password2 = forms.CharField(
        label="パスワード（確認）",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'birthdate', 'password1', 'password2')
        # labels = {
        #     'username': 'ユーザー名',
        # }


    def clean_email(self):  
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています。")
        return email
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d]{8,24}$', password):
            raise forms.ValidationError("パスワードは英数字を含む8〜24文字で入力してください。")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "パスワードが一致しません。")
            
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Profile を作成して保存
            Profile.objects.create(
                user=user,
                gender=self.cleaned_data['gender'],
                birthdate=self.cleaned_data['birthdate'],
                name=self.cleaned_data['username'],  # ユーザー名をプロフィール名にも保存
            )
        return user       


class ProfileForm(forms.ModelForm):
    username = forms.CharField(label='ユーザー名', max_length=150)
    image = forms.ImageField(label='プロフィール画像', required=False)

    class Meta:
        model = Profile
        fields = ['image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            
    def clean_username(self):  # ユーザー名重複チェック
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('このユーザー名はすでに使用されています。')
        return username

    def save(self, commit=True):
        # Save profile image
        profile = super().save(commit=False)
        if commit:
            profile.save()

        # Save username
        if self.user:
            self.user.username = self.cleaned_data['username']
            if commit:
                self.user.save()

        return profile

class EmailChangeForm(forms.Form):
    new_email = forms.EmailField(label='新しいメールアドレス', required=True)
    
    

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません。")

        from django.contrib.auth import authenticate
        user = authenticate(username=user.username, password=password)
        if user is None:
            raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません。")

        self.user = user
        return self.cleaned_data
