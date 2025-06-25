from django.urls import path
from .views import item_create_view
from . import views

app_name = 'items'

urlpatterns = [
    path('create/', item_create_view, name='item_create'),  # ← 重複修正
    path('<int:pk>/', views.item_detail_view, name='item_detail'),
    path('<int:pk>/delete/', views.item_delete_view, name='item_delete'),
    path('<int:pk>/edit/', views.item_edit_view, name='item_edit'),
    path('item-lists/', views.item_list_view, name='item_list'),
    path('<int:pk>/add-to-list/', views.add_to_list_view, name='add_to_list'),
    path('create-item-list/', views.create_item_list_view, name='create_item_list'),
    path('item-lists/<int:list_id>/', views.item_list_detail_view, name='item_list_detail'),
    path('item-lists/<int:list_id>/update-checks/', views.update_check_status_view, name='update_check_status'),
    path('checklist-item/<int:checklist_item_id>/delete/', views.remove_checklist_item, name='remove_checklist_item'),  # 正しい関数名で1つだけにする
    path('item-list/<int:list_id>/copy/', views.copy_list_view, name='copy_list'),  
    path('item-list/<int:list_id>/delete/', views.delete_item_list, name='delete_item_list'),
    path('item-list/<int:list_id>/uncheck_all/', views.uncheck_all_view, name='uncheck_all'),

]
