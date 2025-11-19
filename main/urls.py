from django.urls import path
from . import views
from main.views import create_product_flutter

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('create-product/', views.create_product, name='create_product'),
    path('product/<str:id>/', views.show_product, name='show_product'),
    path('product/<str:id>/edit/', views.edit_product, name='edit_product'),
    path('product/<str:id>/delete/', views.delete_product, name='delete_product'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:product_id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', views.show_json_by_id, name='show_json_by_id'),
    path('get-products/', views.get_products_json, name='get_products_json'),
    
    # ✅ TAMBAHKAN 3 BARIS INI (yang hilang!)
    path('ajax/create-product/', views.create_product_ajax, name='create_product_ajax'),
    path('ajax/update-product/<int:id>/', views.update_product_ajax, name='update_product_ajax'),
    path('ajax/delete-product/<int:id>/', views.delete_product_ajax, name='delete_product_ajax'),
    
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('ajax/login/', views.login_ajax, name='login_ajax'),
    path('ajax/register/', views.register_ajax, name='register_ajax'),
    path('ajax/logout/', views.logout_ajax, name='logout_ajax'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
]