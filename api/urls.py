from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    path('tier/', views.TierList.as_view()),
    path('tier/<int:pk>/', views.TierDetail.as_view()),
    path('image-list/', views.image_list, name="image-list"),
    path('upload/', views.ImageViewSet.as_view(), name='upload'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('generate_link/', views.generate_link, name='generate_link'),
]