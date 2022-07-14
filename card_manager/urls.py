from django.urls import path
from . import views


urlpatterns = [
    path('', views.CardList.as_view(), name='card_list'),
    path('search/', views.CardSearch.as_view(), name='card_search'),
    path('card/<int:pk>/', views.CardDetail.as_view(), name='card_detail'),
    path('delete_card/<int:pk>/', views.DeleteCardView.as_view(), name='card_delete'),
    path('change_status/<int:pk>/', views.ChangeStatusCardView.as_view(), name='change_status'),
]

