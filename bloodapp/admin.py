from django.contrib import admin
from bloodapp.models import Blooddonate,Bloodorder,Bloodsell,SliderImage,Confirmbuydetails
# Register your models here.
class Bloodadmin(admin.ModelAdmin):
    list_display=['id','type','quantity','price']
    list_filter=['type','price']

class Donateadmin(admin.ModelAdmin):
    list_display=['id','name','email','type','mobile','address']
    list_filter=['name','type','email','mobile','address']

class Orderadmin(admin.ModelAdmin):
    list_display=['id','orderid','userid','type','quantity']
    list_filter=['userid','type']

class Confirmbuyadmin(admin.ModelAdmin):
    list_display=['id','userid','type','quantity','price','total_price','mobile','email']
    list_filter=['userid','type','mobile','email']

class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption')

admin.site.register(Bloodsell,Bloodadmin)
admin.site.register(Bloodorder,Orderadmin)
admin.site.register(Confirmbuydetails,Confirmbuyadmin)
admin.site.register(Blooddonate,Donateadmin)
admin.site.register(SliderImage,SliderImageAdmin)