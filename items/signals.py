

# 「ユーザー（User）が新しく作成された」タイミング（＝post_save）で「そのユーザーに対応する Profile オブジェクトも自動で作る」という処理
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
#from .models import Profile

