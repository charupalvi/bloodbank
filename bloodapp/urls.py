"""
URL for bloodapp :-

"""
from django.urls import path
from bloodapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    path('register',views.register),
    path('login',views.userLogin),
    path('logout',views.userLogout),
    path('donate',views.bloodDonate, name='donate'),
    path('donations', views.donationList, name='donations'),
    path('bloodbuy/', views.blood_buy_view, name='bloodbuy'),
    path('contactus/', views.contact_us, name='contact_us'),
    # path('contactus',views.contact),
    path('confirmbuydetails',views.confirmBuyDetails,name='confirmbuydetails'),
    path('confirmorder',views.confirmOrder,name='confirmorder'),
    path('makepayment',views.makePayment),
    path('placeorder/<str:oid>',views.placeOrder),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
