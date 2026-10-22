from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book_list/', views.book_list, name='book_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('<int:book_id>/return/', views.return_book, name='return_book'),
]
