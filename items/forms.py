# items/forms.py
from django import forms
from .models import Item
from accounts.models import Profile  # ← Profileはaccountsからインポート


#from .models import Item, Profile 




class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'category', 'description', 
                  'image1', 'image2', 'image3', 'image4', 'image5']
        labels = {
            'title': 'アイテム名',
            'category': 'カテゴリ',
            'description': 'オススメポイント',
            'image1': '画像1',
            'image2': '画像2',
            'image3': '画像3',
            'image4': '画像4',
            'image5': '画像5',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio']