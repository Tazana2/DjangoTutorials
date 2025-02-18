from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path('products/', views.ProductIndexView.as_view(), name='index'),
    path('products/create', views.ProductCreateView.as_view(), name='form'),
    path('products/<str:id>', views.ProductShowView.as_view(), name='show'),
    path('contact/', views.ContactPageView.as_view(),name='contact'),
    path('cart', views.CartView.as_view(), name='cart_index'),
    path('cart/add/<str:product_id>', views.CartView.as_view(), name='cart_add'),
    path('cart/removeAll', views.CartRemoveAllView.as_view(), name='cart_removeAll'),
]
