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
   
    path('item-list/<int:list_id>/copy/', views.copy_list_view, name='copy_list'),  
    path('item-list/<int:list_id>/delete/', views.delete_item_list, name='delete_item_list'),
    path('item-list/<int:list_id>/uncheck_all/', views.uncheck_all_view, name='uncheck_all'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('user-posts/', views.user_posts_view, name='user_posts'), 
    path('checklist-item/<int:item_id>/delete/', views.remove_checklist_item, name='remove_checklist_item'),
    
    path('list/<int:list_id>/update-name/', views.update_list_name_view, name='update_list_name'),


]
