"""
URL configuration for ch3_12 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views



urlpatterns = [
    path('admin/', admin.site.urls),  # Django 內建後台管理介面
    path('search_list/', views.search_list, name='search_list'),  # 依姓名搜尋學生資料結果列表
    path('search_name/', views.search_name, name='search_name'),  # 姓名搜尋表單頁面
    path('', views.index, name='index'),  # 首頁(根目錄)
    path('index/', views.index, name='index'),  # 首頁(另一組網址,與上面同名)
    path('post/', views.post, name='post'),  # 新增學生資料
    path('edit/<int:id>/', views.edit, name='edit'),  # 編輯指定id的學生資料
    path('delete/<int:id>/', views.delete, name='delete'),  # 刪除指定id的學生資料

#####################################################
    # web api
    path('getAllItems/', views.getAllItems, name='getAllItems'),  # 取得所有項目
    path('getItem/<int:id>/', views.getItem, name='getItem'),  # 取得指定id的項目
    path('createItem/', views.createItem, name='createItem'),  # 新增項目
    path('updateItem/<int:id>/', views.updateItem, name='updateItem'),  # 更新指定id的項目
    path('deleteItem/<int:id>/', views.deleteItem, name='deleteItem'),  # 刪除指定id的項目
]


