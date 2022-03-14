from django.urls import path,include
from socialnetwork import views

urlpatterns = [
    path('', views.global_action),
    path('socialnetwork/', include('socialnetwork.urls')),
]
