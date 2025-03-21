from django.urls import path
from .views import homeView, LoginView, SignUpView, CityListCreateView, CityDeleteView, CustomLogoutView

urlpatterns = [
    path('', homeView.as_view(), name='homeView'),
    path('login/', LoginView.as_view(), name='loginView'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='registerView'),
    
    path('city/', CityListCreateView.as_view(), name='city-list-create'),
    path('city/<int:pk>/', CityDeleteView.as_view(), name='city-delete'),
]