
from . import views
from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'map'
urlpatterns = [
    path('', views.index, name='index'),
    path('show-summary/<int:id>/', views.show_op, name='show_op'),
    # path('show-image/<int:id>/', views.show_image, name='show_img'),
    


]
