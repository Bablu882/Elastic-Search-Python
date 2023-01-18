from django.contrib import admin

# Register your models here.
from .models import Account,Opportunity,Interest,Product,Interest_Junction_c

admin.site.register(Account)
admin.site.register(Opportunity)
admin.site.register(Interest)
admin.site.register(Product)
admin.site.register(Interest_Junction_c)