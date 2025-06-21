# items/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ItemForm
from .models import Item

def item_create_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        # アップロードされた画像をリストに格納
        uploaded_images = [
            request.FILES.get('image1'),
            request.FILES.get('image2'),
            request.FILES.get('image3'),
            request.FILES.get('image4'),
            request.FILES.get('image5'),
        ]
        # 空でない画像だけカウント（空白がある可能性を考慮）
        non_empty_images = [img for img in uploaded_images if img]
        if len(non_empty_images) > 5:
            messages.error(request, '画像は最大5枚までです。')
            return render(request, 'items/item_form.html', {'form': form})

        if form.is_valid():
            item = form.save(commit=False)  # 一度保存を保留
            item.image1 = uploaded_images[0]
            item.image2 = uploaded_images[1]
            item.image3 = uploaded_images[2]
            item.image4 = uploaded_images[3]
            item.image5 = uploaded_images[4]
            item.save()
            messages.success(request, '投稿が完了しました！')
            return redirect('accounts:home')
    else:
        form = ItemForm()

    return render(request, 'items/item_form.html', {'form': form})
