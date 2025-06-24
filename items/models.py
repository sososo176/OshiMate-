

# Create your models here.
from django.db import models  # Djangoのモデル機能を使うためにインポート
from django.contrib.auth.models import User

class Item(models.Model):  # Itemというデータの「型（モデル）」を定義
    title = models.CharField(max_length=100)  
    # アイテムのタイトル（例：「ペンライト」）。最大100文字までの文字列。

    image = models.ImageField(upload_to='item_images/')  
    # 画像を保存するフィールド。「media/item_images/」というフォルダに保存される。

    created_at = models.DateTimeField(auto_now_add=True)
    # 登録された日時を自動で記録（作成時のみ）
 # ↓カテゴリを追加
    category = models.CharField(max_length=50, choices=[
    ('現場グッズ', '現場グッズ'),
    ('参戦服', '参戦服'),
    ('宿泊用品', '宿泊用品'),
], default='現場グッズ')
    
    description = models.TextField(blank=True)
    # オススメポイント（アイテムの説明文）

    image1 = models.ImageField(upload_to='item_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='item_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='item_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='item_images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='item_images/', blank=True, null=True)
    # 画像（最大5枚まで）

    created_at = models.DateTimeField(auto_now_add=True)
    # 作成日時（自動で記録）
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title  
        # 管理画面などで「Item(1)」ではなく「ペンライト」と表示されるように


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/')


class ItemList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}（{self.user.username}）'


class ChecklistItem(models.Model):
    item_list = models.ForeignKey(ItemList, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item.title} in {self.item_list.name}'
