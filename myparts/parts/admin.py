from django.contrib import admin
from .models import Parts, CompatibleMachines ,CompatibleMolds,PartsPurchase,PartsRelease, PartsLocation




class PartsAdmin(admin.ModelAdmin): 
    list_display = ('part_name', 'part_manufacturer_barcode', 'part_manufacturer_part_number','part_qty_in_stock')
    search_fields =['part_name', 'part_manufacturer_barcode', 'part_manufacturer_part_number'] 
    

class PartsPurchaseAdmin(admin.ModelAdmin): 
    list_display = ('part_id', 'purchase_date', 'po_number','invoice_number','qty_ordered') 
    search_fields =['part_id__part_name', 'po_number','invoice_number', 'part_id__part_manufacturer_barcode', 'part_id__part_manufacturer_part_number']
    
class PartsReleaseAdmin(admin.ModelAdmin): 
    list_display = ('part_id', 'release_date','qty_released') 
    search_fields =['part_id__part_name',  'part_id__part_manufacturer_barcode', 'part_id__part_manufacturer_part_number']
    
    
class PartsLocationAdmin(admin.ModelAdmin): 
    list_display = ('part_id', 'warehouse', 'rack','bay','level','position','quantity') 
    search_fields =['warehouse', 'rack','bay', 'level', 'position']    

admin.site.register(Parts , PartsAdmin)
admin.site.register(PartsPurchase , PartsPurchaseAdmin)
admin.site.register(PartsRelease , PartsReleaseAdmin)
admin.site.register(PartsLocation , PartsLocationAdmin)

