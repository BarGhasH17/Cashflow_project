from django.contrib import admin
from .models import Status, Type, Category, Subcategory, CashFlowRecord

admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(CashFlowRecord)