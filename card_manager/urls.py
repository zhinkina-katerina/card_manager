from django.urls import path
from . import views


urlpatterns = [
    path('', views.CardList.as_view(), name='card_list'),
    path('search/', views.CardSearch.as_view(), name='card_search'),
    path('card/<int:pk>/', views.CardDetail.as_view(), name='card_detail'),
]

