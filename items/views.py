# items/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ItemForm, ProfileForm
from .models import Item
from django.contrib.auth.decorators import login_required
from .models import ItemList, ItemList, ChecklistItem
from django.views.decorators.http import require_POST
#from django.http import HttpResponseRedirect

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
    item_lists = ItemList.objects.filter(user=request.user) 
    
    return render(request, 'items/item_detail.html', {
        'item': item,
        'user': request.user,
        'item_lists': item_lists,
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
            
            item.save()
            messages.success(request, '投稿が完了しました！')
            return redirect('accounts:home')
    else:
        form = ItemForm()

    return render(request, 'items/item_form.html', {'form': form})



#@login_required
#def item_list_view(request):
 #   item_lists = ItemList.objects.filter(user=request.user).order_by('-created_at')
 #  return render(request, 'items/item_list.html', {'item_lists': item_lists})

# items/views.py
def item_list_view(request):
    tutorial_lists = ItemList.objects.filter(is_tutorial=True)  # 初心者用
    user_lists = ItemList.objects.filter(user=request.user, is_tutorial=False)  # 通常用
    return render(request, 'items/item_list.html', {
        'tutorial_lists': tutorial_lists,
        'user_lists': user_lists,
    })


@login_required
def add_to_list_view(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        list_id = request.POST.get('item_list_id')
        item_list = get_object_or_404(ItemList, id=list_id, user=request.user)

        # 重複登録を防ぐ
        if not ChecklistItem.objects.filter(item_list=item_list, item=item).exists():
            ChecklistItem.objects.create(item_list=item_list, item=item)
            messages.success(request, '持ち物リストに追加しました！')
        else:
            messages.info(request, 'すでにこのリストに含まれています。')

    return redirect('items:item_detail', pk=pk)

@require_POST
@login_required
def create_item_list_view(request):
    name = request.POST.get('name')
    if name:
        ItemList.objects.create(user=request.user, name=name)
    return redirect(request.META.get('HTTP_REFERER', 'accounts:home'))



@login_required
def item_list_detail_view(request, list_id):
    item_list = get_object_or_404(ItemList, id=list_id)
    checklist_items = ChecklistItem.objects.filter(item_list=item_list)
    is_tutorial = item_list.is_tutorial
    return render(request, 'items/item_list_detail.html', {
        'item_list': item_list,
        'checklist_items': checklist_items,
        'is_tutorial': is_tutorial,
    })

@login_required
def update_checklist_view(request, list_id):
    item_list = get_object_or_404(ItemList, id=list_id, user=request.user)
    checklist_items = ChecklistItem.objects.filter(item_list=item_list)

    # すべて一旦未チェックに
    checklist_items.update(is_checked=False)

    # チェックされたIDを反映
    checked_ids = request.POST.getlist('checked_items')
    ChecklistItem.objects.filter(id__in=checked_ids).update(is_checked=True)

    return redirect('items:item_list_detail', list_id=list_id)

@require_POST
@login_required
def update_check_status_view(request, list_id):
    item_list = get_object_or_404(ItemList, id=list_id, user=request.user)
    checklist_items = ChecklistItem.objects.filter(item_list=item_list)

    # POSTデータを確認
    print("POST data:", request.POST)  # 送信されたデータを確認

    # チェックボックスの状態を更新
    for item in checklist_items:
        checkbox_value = request.POST.get(f'check_{item.id}')
        if checkbox_value:
            item.is_checked = True  # チェックされていればTrueに設定
        else:
            item.is_checked = False  # チェックされていなければFalseに設定
        item.save()  # 更新された状態を保存

    # 成功メッセージと共にリダイレクト
    messages.success(request, "チェック状態を保存しました。")
    return redirect('items:item_list_detail', list_id=list_id)


@require_POST
@login_required
def remove_checklist_item(request, item_id):
    checklist_item = get_object_or_404(ChecklistItem, id=item_id, item_list__user=request.user)

    item_list_id = checklist_item.item_list.id
    checklist_item.delete()
    messages.success(request, "アイテムを削除しました。")

    return redirect('items:item_list_detail', list_id=item_list_id)

def copy_list_view(request, list_id):
    original_list = get_object_or_404(ItemList, id=list_id, is_tutorial=True)
    if request.method == 'POST':
        copied_list = ItemList.objects.create(
            name=f"{original_list.name}（コピー）",
            user=request.user,
            is_tutorial=False
        )
        # 元のリストのアイテムを複製
        for checklist_item in ChecklistItem.objects.filter(item_list=original_list):
            ChecklistItem.objects.create(
                item_list=copied_list,
                item=checklist_item.item,
                is_checked=False  # コピー時は未チェックにする
            )
        return redirect('items:item_list')
    
@login_required
def delete_item_list(request, list_id):
    item_list = get_object_or_404(ItemList, id=list_id, user=request.user)
    item_list.delete()
    return redirect('items:item_list')


@require_POST
@login_required
def uncheck_all_view(request, list_id):
    item_list = get_object_or_404(ItemList, id=list_id, user=request.user)

    # 全てのチェックをFalseにする
    ChecklistItem.objects.filter(item_list=item_list).update(is_checked=False)

    messages.success(request, "すべてのチェックを解除しました。")
    return redirect('items:item_list_detail', list_id=list_id)



@login_required
def mypage_view(request):
    return render(request, 'items/mypage.html')#'accounts/mypage.html','items/mypage.html'



@login_required
def profile_edit_view(request):
    # ユーザーのプロフィールを取得
    profile = request.user.profile

    if request.method == 'POST':
        # フォームが送信された場合
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # フォームのデータを保存
            return redirect('mypage')  # マイページにリダイレクト
    else:
        # フォームを表示
        form = ProfileForm(instance=profile)

    return render(request, 'items/profile_edit.html', {'form': form})


@login_required
def user_posts_view(request):
    user_posts = Item.objects.filter(user=request.user)  # ユーザーの投稿を取得
    return render(request, 'items/user_posts.html', {'user_posts': user_posts})
