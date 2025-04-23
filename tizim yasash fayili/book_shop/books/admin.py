from django.contrib import admin
from .models import Reference, Book_model, Cost_Model, Output, Staff, Staff_work, income, SomeModel,Purchase

# Admin panelda modellarni dekorator yordamida ro'yxatdan o'tkazish





@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("buyer_name", "book", "quantity", "total_price", "created_at")
    list_filter = ("created_at",)





@admin.register(Book_model)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'quantity']
    search_fields = ['name__name', 'category__name']
    list_filter = ('is_deleted',)  

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    search_fields = ['name', 'value']

# Qolgan modellarni oddiy usulda ro'yxatdan o'tkazish
admin.site.register(Cost_Model)
admin.site.register(Output)
admin.site.register(Staff)
admin.site.register(Staff_work)
admin.site.register(income)


