from django.contrib import admin
from .models import ItemList, Item, ChecklistItem  # ← ChecklistItem を追加

admin.site.register(ItemList)
admin.site.register(Item)
admin.site.register(ChecklistItem)  # ← これを追加！

