from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from EmailApp import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'EmailApp'
urlpatterns = [
    path('cart/',views.cart,name='cart'),
    path('create-checkout-session/', views.create_checkout_session),
    path('checkout/',views.checkout,name='checkout'),
    path('removecart/',views.removecart,name='removecart'),
    path('product_compare/', views.product_compare, name='product_compare'),
    path('wishlist/',views.wishlist, name="wishlist"),
    path('wishlistdetails/',views.wishlistdetails, name="wishlistdetails"),
    path('increase_cart_item/',views.increase_cart_item,name='increase_cart_item'),
    path('admin/', admin.site.urls),
    path('register/',views.register,name='register'),
    path('index/',views.index, name='index'),
    path('login/',views.loginn, name='login'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		views.activate_account, name='activate'),
	url('^', include('django.contrib.auth.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/<int:data_id>/', views.payment_canceled, name='payment_cancelled'),
    path('stripe/', views.StripeView.as_view(), name='stripe'),
    path('config/', views.stripe_config),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
