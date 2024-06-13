from django.contrib import admin
from .models import VehicleCategories,brands,partscategory,Top_categories


# Register your models here.


admin.site.register(VehicleCategories)
admin.site.register(brands)
admin.site.register(partscategory)
admin.site.register(Top_categories)
