from django.urls import path
from .views import IndexPage, ShopPage, ServicePage, ThanksPage, CartPage, ContactPage, CheckoutPage, AboutPage, \
    BlogPage, UpdateProductView, DeleteProductView

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('shop/', ShopPage.as_view(), name='shop'),
    path('service/', ServicePage.as_view(), name='service'),
    path('checkout/', CheckoutPage.as_view(), name='checkout'),
    path('about/', AboutPage.as_view(), name='about'),
    path('blog/', BlogPage.as_view(), name='blog'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('cart/', CartPage.as_view(), name='cart'),
    path('thanks/', ThanksPage.as_view(), name='thanks'),
    path('update/<int:id>/', UpdateProductView.as_view(), name='update'),
    path('delete/<int:id>/', DeleteProductView.as_view(), name='delete'),

]
