# from django.contrib import admin
# from .models import ColdroomEntry, Offal, Notification, Grv, ProductionSheet, ExcelExport, ProductionsExport, StockSheet
# from .models import SlaughterSheet, Cattle, GradePrices, CattlePayments, DailyCashier, Payment, Income

# admin.site.register(ColdroomEntry)
# admin.site.register(Income)

# @admin.register(SlaughterSheet)
# class SlaughterSheetAdmin(admin.ModelAdmin):
#     list_display = ("sheet_no", "purchase_date", "supplier_name", "number_of_cattle", "total_amount", "is_paid")
#     search_fields = ("sheet_no", "supplier_name")
#     list_filter = ("is_paid", "purchase_date")
#     ordering = ("-created_at",)


from django.contrib import admin