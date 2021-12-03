from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



from django.db.models.signals import post_delete
from django.dispatch import receiver
from .validators import validate_file_extension


letter= [
('A', 'A'),
('B', 'B'),
('C', 'C'),
('D', 'D'),
('E', 'E'),
('F', 'F'),
('G', 'G'),
('H', 'H'),
('I', 'I'),
('J', 'J'),
('K', 'K'),
('L', 'L'),
('M', 'M'),
('N', 'N'),
('O', 'O'),
('P', 'P'),
('Q', 'Q'),
('R', 'R'),
('S', 'S'),
('T', 'T'),
('U', 'U'),
('V', 'V'),
('W', 'W'),
('X', 'X'),
('Y', 'Y'),
('Z', 'Z'),
]

number=[
('01', '01'),
('02', '02'),
('03', '03'),
('04', '04'),
('05', '05'),
('06', '06'),
('07', '07'),
('08', '08'),
('09', '09'),
('10', '10'),
('11', '11'),
('12', '12'),
('13', '13'),
('14', '14'),
('15', '15'),
('16', '16'),
('17', '17'),
('18', '18'),
('19', '19'),
('20', '20'),
('21', '21'),
('22', '22'),
('23', '23'),
('24', '24'),
('25', '25'),
('26', '26'),
('27', '27'),
('28', '28'),
('29', '29'),
('30', '30'),
('31', '31'),
('32', '32'),
('33', '33'),
('34', '34'),
('35', '35'),
('36', '36'),
('37', '37'),
('38', '38'),
('39', '39'),
('40', '40'),


]

class Parts(models.Model):
    part_barcode = models.CharField(max_length=100, null=True, blank=True , verbose_name='Barcode')
    part_name = models.CharField(max_length=200, null=True, blank=True , verbose_name='Name')
    part_model = models.CharField(max_length=100, null=True, blank=True , verbose_name='Model')
    part_note = models.TextField(null=True, blank=True, verbose_name='Note') 
    part_manufacturer_barcode = models.CharField(max_length=100, null=True, blank=True , verbose_name='Manufacturer Barcode')
    part_manufacturer_part_number= models.CharField(max_length=100, null=True, blank=True , verbose_name='Manufacturer Part Number')
    part_oem_number= models.CharField(max_length=100, null=True, blank=True , verbose_name='OEM Number')
    part_qty_in_stock = models.PositiveIntegerField( null=True, blank=True , verbose_name= 'Quantity In Stock')
    part_min_qty = models.PositiveIntegerField( null=True, blank=True , verbose_name= 'Minimum Quantity')
    part_compatible= models.CharField(max_length=100, null=True, blank=True , verbose_name='Where to Use')
    
    date_posted = models.DateTimeField(default=timezone.now)    
    creator = models.ForeignKey(User , on_delete=models.SET_NULL, blank=True, null=True,)

    class Meta:
        ordering = ['part_name']
    def __str__(self):
        return str(self.part_name) + str(self.part_manufacturer_barcode)

    def get_absolute_url(self):
        return reverse('parts-detail-page',kwargs={'pk':self.pk})


    
    
class CompatibleMachines (models.Model):
    part_id = models.ForeignKey(Parts, on_delete=models.CASCADE, null=True,related_name='machinparts')
    machine_id = models.CharField(max_length=2, choices=letter,null=True, blank=True ,  verbose_name='Machine' )
      


class CompatibleMolds(models.Model):
    part_id = models.ForeignKey(Parts, on_delete=models.CASCADE, null=True,related_name='moldparts') 
    mold_id  = models.CharField(max_length=2, choices=letter,null=True, blank=True ,  verbose_name='Mold' )
     


class PartsPurchase(models.Model):
    part_id = models.ForeignKey(Parts, on_delete=models.CASCADE, null=True,related_name='partspurchase')
    date_posted = models.DateTimeField(default=timezone.now)
    purchase_date = models.DateTimeField(default=timezone.now)
    po_number= models.PositiveIntegerField(null=True, blank=True , verbose_name= 'PO Number')
    invoice_number= models.PositiveIntegerField(null=True, blank=True , verbose_name= 'Invoice Number')
    qty_ordered= models.PositiveIntegerField( null=True, blank=True , verbose_name= 'Quantity Ordered')    
    vendor = models.CharField(max_length=100, null=True, blank=True , verbose_name='Vendor Name')
    vendor_phone = models.CharField(max_length=100, null=True, blank=True , verbose_name='Vendor Phone')
    creator = models.ForeignKey(User , on_delete=models.SET_NULL, blank=True, null=True,)
    purchase_note = models.TextField(null=True, blank=True, verbose_name='Purchase Note')
    class Meta:
        ordering = ['-purchase_date']
    def __str__(self):
        return str(self.part_id)

    def get_absolute_url(self):
        return reverse('parts-location-page',kwargs={'purchaseid':self.pk})
        
class PartsRelease(models.Model):
    part_id = models.ForeignKey(Parts, on_delete=models.CASCADE, null=True,related_name='partsrelease')
    date_posted = models.DateTimeField(default=timezone.now)
    release_date = models.DateTimeField(default=timezone.now)
    qty_released= models.PositiveIntegerField( null=True, blank=True , verbose_name= 'Quantity Released')    
    creator = models.ForeignKey(User , on_delete=models.SET_NULL, blank=True, null=True,)
    
    release_note = models.TextField(null=True, blank=True, verbose_name='Release Note')
    class Meta:
        ordering = ['-release_date']
        
    def __str__(self):
        return str(self.part_id)

    def get_absolute_url(self):
        return reverse('parts-detail-page',kwargs={'pk':self.part_id.pk})

class PartsLocation (models.Model):
    part_id = models.ForeignKey(Parts, on_delete=models.CASCADE, blank=True,null=True,related_name='partslocation')
    purchase_id = models.ForeignKey(PartsPurchase, on_delete=models.CASCADE, blank=True,null=True,related_name='purchaselocation')
    warehouse = models.CharField(max_length=2, choices=letter,null=True, blank=True ,  verbose_name='Warehouse' )
    rack= models.CharField(max_length=2, choices=letter,null=True, blank=True ,  verbose_name='Rack' )
    bay= models.CharField(max_length=2, choices=number, null=True, blank=True , verbose_name='Bay' )
    level= models.CharField(max_length=2, choices=letter,null=True, blank=True ,  verbose_name='Level' )
    position= models.CharField(max_length=2, choices=number, null=True, blank=True , verbose_name='Position' )   
                                                                                                
    quantity= models.PositiveIntegerField( null=True, blank=True , verbose_name= 'Quantity In Stock')
    
    class Meta:
        unique_together = ('part_id','warehouse', 'rack', 'bay', 'level', 'position') 
    
    def get_absolute_url(self):
        return reverse('parts-location-page',kwargs={'purchaseid':self.purchase_id.pk}) 
    
    
    
class PartsFiles(models.Model):
    part_id= models.ForeignKey(Parts, on_delete=models.CASCADE, blank=True, null=True,related_name='partsfile')
    description = models.CharField(max_length=255, blank=True)
    creator = models.ForeignKey(User , on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Creator')
    partfile = models.FileField(upload_to='partsfiles/%Y/%m/%d/' , validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return (str(self.uploaded_at) +' - '+ str(self.partfile))
        
        
    def get_absolute_url(self):
        return reverse('parts-detail-page',kwargs={'pk':self.part_id.pk})
    
    class Meta:
        ordering = ['-uploaded_at'] 
        
@receiver(post_delete, sender=PartsFiles)
def submission_delete(sender, instance, **kwargs):
    instance.partfile.delete(False)       
    
    
    
    
    