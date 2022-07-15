from django.urls import path
from . import views


urlpatterns = [
    path('', views.CardList.as_view(), name='card_list'),
    path('search/', views.CardSearch.as_view(), name='card_search'),
    path('card_generator/', views.CardGenerator.as_view(), name='card_generator'),
    path('card/<int:pk>/', views.CardDetail.as_view(), name='card_detail'),
    path('delete_card/<int:pk>/', views.DeleteCard.as_view(), name='card_delete'),
    path('deactivate_card/<int:pk>/', views.DeactivateCard.as_view(), name='deactivate_card'),
    path('activate_card/<int:pk>/', views.ActivateCard.as_view(), name='activate_card'),
]

