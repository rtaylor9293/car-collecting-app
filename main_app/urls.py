from django.contrib import admin  # ✅ Correct import
from django.urls import include, path
from . import views  # Import views to connect routes to view functions
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('cars/', views.car_index, name='car-index'),
    path('cars/<int:car_id>/', views.car_detail, name='cars_detail'),
    path('cars/create/', views.CarCreate.as_view(), name='car-create'),
    path('cars/<int:pk>/update/', views.CarUpdate.as_view(), name='car-update'),
    path('cars/<int:pk>/delete/', views.CarDelete.as_view(), name='car-delete'),
    path('cartrips/create/', views.CarTripsCreate.as_view(), name='cartrip-create'),
    path('cartrips/<int:pk>/', views.CarTripDetail.as_view(), name='cartrip-detail'),
    path('cartrips/', views.CarTripsList.as_view(), name='cartrip-index'),
    path('cartrips/<int:pk>/update/', views.CarTripUpdate.as_view(), name='cartrip-update'),
    path('cartrips/<int:pk>/delete/', views.CarTripDelete.as_view(), name='cartrip-delete'),
    # Include built-in auth urls
    path('accounts/signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

]
