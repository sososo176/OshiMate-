from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
#from .models import Profile
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) 
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  
    gender = models.CharField(max_length=10, choices=[('男性', '男性'), ('女性', '女性'), ('その他', 'その他')], blank=True)
    birthdate = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.user.username

    



# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()


# #新しいユーザーが登録されたときに、そのユーザーに対応する Profile を自動作成
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)