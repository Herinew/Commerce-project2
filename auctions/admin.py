from django.contrib import admin
from .models import Listings, Bids, Category, Comments

# Register your models here.
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Category)
admin.site.register(Comments)
