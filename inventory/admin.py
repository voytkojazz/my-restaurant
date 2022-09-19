
from django.contrib import admin
from .models import Ingridient, MenuItem, RecipeRequirement, Purchase
# Register your models here.

###### INLINES ##########
class RecipeRequirementInline(admin.TabularInline):
    model = RecipeRequirement




######### ADMIN MODELS ############
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'timestamp',)

class MenuItemAdmin(admin.ModelAdmin):
    inlines = [
        RecipeRequirementInline,
    ]






admin.site.register(Ingridient)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(RecipeRequirement)
admin.site.register(Purchase, PurchaseAdmin)





