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
    path('bloodbuy/', views.blood_buy_view, name='bloodbuy'),
    path('contactus',views.contact),
    path('confirmbuydetails',views.confirmBuyDetails,name='confirmbuydetails'),
    path('confirmorder',views.confirmOrder,name='confirmorder'),
    path('makepayment',views.makePayment),
    path('placeorder/<str:oid>',views.placeOrder),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
