# items/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ItemForm
from .models import Item
from django.contrib.auth.decorators import login_required

@login_required
def item_edit_view(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # 投稿者以外は編集できない
    if request.user != item.user:
        messages.error(request, "編集権限がありません")
        return redirect('accounts:home')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, "アイテムを更新しました！")
            return redirect('items:item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)

    return render(request, 'items/item_form.html', {'form': form, 'item': item})

@login_required
def item_detail_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'items/item_detail.html', {
        'item': item,
        'user': request.user
    })

@login_required
def item_delete_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user == item.user:
        item.delete()
        messages.success(request, "アイテムを削除しました")
    else:
        messages.error(request, "削除権限がありません")
    return redirect('accounts:home')


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
            item.user = request.user
            
            item.image1 = uploaded_images[0]
            item.image2 = uploaded_images[1]
            item.image3 = uploaded_images[2]
            item.image4 = uploaded_images[3]
            item.image5 = uploaded_images[4]
            item.user = request.user
            item.save()
            messages.success(request, '投稿が完了しました！')
            return redirect('accounts:home')
    else:
        form = ItemForm()

    return render(request, 'items/item_form.html', {'form': form})

