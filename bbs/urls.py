from django.urls import path
from . import views

app_name = 'bbs'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('board/list/', views.BoardListView.as_view(), name='board_list'),
    path('thread/menu/<int:pk>/', views.ThreadMenuView.as_view(), name='thread_menu'),
    path('thread/detail/<int:pk>/', views.ThreadDetailView.as_view(), name='detail'),
    path('thread/search/', views.ThreadSearchView.as_view(), name='thread_search'),
]
