from django.contrib import admin

# Register your models here.
from .models import Account,Contact,Interest,Product,Interest_Junction_c

admin.site.register(Account)
admin.site.register(Contact)
admin.site.register(Interest)
admin.site.register(Product)
admin.site.register(Interest_Junction_c)