from django.shortcuts import render, redirect
from .models import Parts, CompatibleMachines ,CompatibleMolds,PartsPurchase,PartsRelease, PartsLocation, PartsFiles
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse , HttpResponseRedirect


from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_datepicker_plus import DateTimePickerInput
import datetime
from django.utils import timezone

from django.db.models import Sum , Count
from django.shortcuts import get_object_or_404
from django.db import IntegrityError


from django.db import transaction
from .forms import CompatibleMachinesFormSet,CompatibleMoldsFormSet

from django.urls import reverse_lazy


#==================================================================================================================================
#
# ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
#▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
#▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
#▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     ▐░▌          
#▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄ 
#▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌
#▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀█░█▀▀      ▐░▌      ▀▀▀▀▀▀▀▀▀█░▌
#▐░▌          ▐░▌       ▐░▌▐░▌     ▐░▌       ▐░▌               ▐░▌
#▐░▌          ▐░▌       ▐░▌▐░▌      ▐░▌      ▐░▌      ▄▄▄▄▄▄▄▄▄█░▌
#▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     ▐░░░░░░░░░░░▌
# ▀            ▀         ▀  ▀         ▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀ 
#
#==================================================================================================================================
def PartsSearch(request):
    mypart= request.POST.get('mypart')
    
    parts_ids=""
    q_objects = Q()            
    if mypart != "0" and mypart != "" and mypart != None :
        q_objects &= Q(part_barcode__contains=mypart)
        q_objects |= Q(part_name__contains=mypart)
        q_objects |= Q(part_model__contains=mypart)
        q_objects |= Q(part_note__contains=mypart)
        q_objects |= Q(part_manufacturer_barcode__contains=mypart)
        q_objects |= Q(part_manufacturer_part_number__contains=mypart)
        q_objects |= Q(part_compatible__contains=mypart)
        
        parts_ids = Parts.objects.filter(q_objects)[:30]

    else:
        parts_ids =""
        
    return render(request, 'parts_search.html', {'partsids': parts_ids})    
    
    
class PartsListView(ListView):
    model = Parts    
    context_object_name = 'parts'
    ordering = ['part_name']
    paginate_by = 50


class PartsListAddView(ListView):
    model = Parts    
    context_object_name = 'parts'
    template_name='parts/parts_add.html'
    ordering = ['part_name']
    paginate_by = 50
    
    
class PartsDetailView(DetailView):
    model = Parts
    
    
    def get_queryset(self):
        queryset = Parts.objects.filter(id=self.kwargs['pk']) 
        #queryset['parts_location'] = PartsLocation.objects.filter(purchase_id__part_id__id=  self.kwargs['pk']).values('warehouse','warehouse__warehouse_name','rack','bay','level','position').annotate(total_location_inventory=Sum('quantity'))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(PartsDetailView, self).get_context_data(**kwargs)
        #context['parts_location'] = PartsLocation.objects.filter(part_id__id=  self.kwargs['pk']).values('warehouse','warehouse__warehouse_name','rack','bay','level','position').annotate(total_location_inventory=Sum('quantity'))
        context['parts_location'] = PartsLocation.objects.filter(part_id__id=  self.kwargs['pk'])
        context['parts_files'] = PartsFiles.objects.filter(part_id__id=  self.kwargs['pk'])
        return context
    
    

class PartsCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = "parts.add_parts"

    model = Parts    
    fields= ['part_barcode','part_name','part_model','part_note','part_manufacturer_barcode','part_manufacturer_part_number','part_oem_number','part_compatible','part_min_qty']

    def get_form(self):
        form = super().get_form()

        #form.initial['machine_id'] = self.machineid

        return form

    def get_context_data(self, **kwargs):
        data = super(PartsCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['machine'] = CompatibleMachinesFormSet(self.request.POST)
            data['mold'] = CompatibleMoldsFormSet(self.request.POST)
  
        else:
            data['machine'] = CompatibleMachinesFormSet()
            data['mold'] = CompatibleMoldsFormSet()

        return data

    def form_valid(self, form):
        
        context = self.get_context_data()
        machine = context['machine']
        mold = context['mold']

        with transaction.atomic():
        
            form.instance.creator = self.request.user
            self.object = form.save()

            if machine.is_valid():
                machine.instance = self.object
                machine.save()    

            if mold.is_valid():
                mold.instance = self.object
                mold.save()


        return super(PartsCreateView, self).form_valid(form)


class PartsUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = "parts.change_parts"

    model = Parts    
    fields= ['part_barcode','part_name','part_model','part_note','part_manufacturer_barcode','part_manufacturer_part_number','part_oem_number','part_compatible','part_qty_in_stock','part_min_qty']

    def get_form(self):
        form = super().get_form()

        #form.initial['machine_id'] = self.machineid

        return form

    def get_context_data(self, **kwargs):
        data = super(PartsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['machine'] = CompatibleMachinesFormSet(self.request.POST, instance=self.object)
            data['machine'].full_clean()
            data['mold'] = CompatibleMoldsFormSet(self.request.POST, instance=self.object)
            data['mold'].full_clean()
  
        else:
            data['machine'] = CompatibleMachinesFormSet( instance=self.object)
            data['mold'] = CompatibleMoldsFormSet( instance=self.object)

        return data

    def form_valid(self, form):
        
        context = self.get_context_data()
        machine = context['machine']
        mold = context['mold']

        with transaction.atomic():
        
            form.instance.creator = self.request.user
            self.object = form.save()

            if machine.is_valid():
                machine.instance = self.object
                machine.save()    

            if mold.is_valid():
                mold.instance = self.object
                mold.save()


        return super(PartsUpdateView, self).form_valid(form)
        
        
class PartAddFileCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = "parts.add_parts"
    model = PartsFiles
    fields= ['description','partfile'] 
       
    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.part_id = get_object_or_404(Parts, pk = self.partid)        
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        self.partid = kwargs.get('partid', "")
        return super().dispatch(request,*args, **kwargs)      


class PartAddFileDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required = "parts.add_parts"
    model = PartsFiles
    
    def get_success_url(self):
        return reverse_lazy('parts-detail-page', kwargs={'pk': self.object.part_id.pk}) 

        
        
#==================================================================================================================================
#
# ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
#▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
#▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
#▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌          
#▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ 
#▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
#▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀█░█▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ 
#▐░▌          ▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌          ▐░▌▐░▌          
#▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌       ▐░▌ ▄▄▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ 
#▐░▌          ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
# ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
#                                                                                                        
#==================================================================================================================================

class PartsPurchaseDetailView(DetailView):
    model = PartsPurchase



class PartsPurchaseCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):             

    permission_required = "parts.add_parts"

    model = PartsPurchase    
    fields= ['purchase_date','po_number','invoice_number','vendor','vendor_phone','purchase_note']

    def get_form(self):
        form = super().get_form()        
        form.fields['purchase_date'].widget = DateTimePickerInput() 

        return form            
        
    def form_valid(self, form):
        part_id = get_object_or_404(Parts, pk = self.partid)
        form.instance.creator = self.request.user

        form.instance.part_id=part_id

        return super().form_valid(form)        


    def dispatch(self, request, *args, **kwargs):
        self.partid = kwargs.get('partid', "")
        return super().dispatch(request,*args, **kwargs)                 
             
             
#==================================================================================================================================             
#
# ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄ 
#▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌
#▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌ ▀▀▀▀█░█▀▀▀▀ 
#▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     
#▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     
#▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     
#▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     
#▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     
#▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     
#▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     
# ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀      
# 
#==================================================================================================================================            

class PartsReleaseDetailView(DetailView):
    model = PartsRelease

class PartsReleaseCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):             

    permission_required = "parts.add_parts"

    model = PartsRelease    
    fields= ['release_date','qty_released','employee','release_note']

    def get_form(self):
        form = super().get_form()
        form.fields['qty_released'].widget.attrs['readonly'] = "readonly"
        form.fields['release_date'].widget = DateTimePickerInput() 
        return form    

        
    def get_context_data(self, **kwargs):  
        
        kwargs['parts_location'] = PartsLocation.objects.filter(part_id__id=  self.partid)
        
        # combine similar locations
        #kwargs['parts_location'] = PartsLocation.objects.filter(part_id__id=  self.partid).values('warehouse','warehouse__warehouse_name','rack','bay','level','position').annotate(total_location_inventory=Sum('quantity'))
        data = super(PartsReleaseCreateView, self).get_context_data(**kwargs)

        return data

    def form_valid(self, form):
    
        form.instance.creator = self.request.user            
        
        part_id = get_object_or_404(Parts, pk = self.partid)
        form.instance.part_id = part_id        
        current_qtty = part_id.part_qty_in_stock

        #qty_released= form.instance.qty_released

        # get hidden field of total qty 
        # compare with total inventory
        #totalqtyout = self.request.POST.get('totalqtyout',"")
        #totalqtyout_int=0
        #if totalqtyout!="" :
        #    try:
        #      totalqtyout_int = int(totalqtyout)
        #    except ValueError as verr:
        #      totalqtyout_int=0
        #    except Exception as ex:
        #     totalqtyout_int=0    
        #if totalqtyout_int > current_qtty:
        #    form.add_error('qty_released','Not enough inventory in stock!!!!!!')
        #    return super().form_invalid(form)
  
        # get qty out of each location
        # compare with each location inventory
        # if both ok then save
        #values = request.POST.getlist('key')

        for key, value in self.request.POST.items():
            locationid=0
            qtyout = 0
            if (key.find('qtyout') != -1):
                if value!="" :
                    try:
                      qtyout = int(value)
                    except ValueError as verr:
                      qtyout=0
                    except Exception as ex:
                      qtyout=0
                if qtyout>0:
                    nlocation=key.split("_")
                    locationid = self.request.POST.get('locationid_'+nlocation[1],"")
                    if int(locationid)>0:
                        current_location = PartsLocation.objects.get(id = locationid)
                        current_qttyqty=current_location.quantity
                        newqty=current_qttyqty-qtyout
                        updatelocation = PartsLocation.objects.filter(id = locationid).update(quantity=newqty)
                        queryset = PartsLocation.objects.filter(part_id =  current_location.part_id.id)
                        totals = queryset.aggregate(sum=Sum('quantity')).get('sum')
                        partupdate = Parts.objects.filter(id = current_location.part_id.id).update(part_qty_in_stock=totals)

        #form.add_error('qty_released','---')
        #return super().form_invalid(form)    
        #if "locationid_" in key:
        #locationid = value
        #new_qtty = current_qtty - totalqtyout_int
        #mupdate=Parts.objects.filter(pk=part_id.pk).update(part_qty_in_stock=new_qtty)
        
        return super().form_valid(form)             


    def dispatch(self, request, *args, **kwargs):
        self.partid = kwargs.get('partid', "")
        return super().dispatch(request,*args, **kwargs)         



#==================================================================================================================================             
#
# ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄ 
#▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌
#▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌
#▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌     ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌▐░▌    ▐░▌
#▐░▌          ▐░▌       ▐░▌▐░▌          ▐░█▄▄▄▄▄▄▄█░▌     ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌ ▐░▌   ▐░▌
#▐░▌          ▐░▌       ▐░▌▐░▌          ▐░░░░░░░░░░░▌     ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌  ▐░▌  ▐░▌
#▐░▌          ▐░▌       ▐░▌▐░▌          ▐░█▀▀▀▀▀▀▀█░▌     ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌   ▐░▌ ▐░▌
#▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌     ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌    ▐░▌▐░▌
#▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌     ▐░▌      ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌     ▐░▐░▌
#▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌
# ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀ 
#                                                                            
#==================================================================================================================================             
def LoadDropdown(request):
    style= request.POST.get('style')
    mylists = []
    if style=='number':
        numbers = 0
        while(numbers < 40 ):
            numbers+=1
            if numbers<10:
                mylists.append("0"+str(numbers))
            else:
                mylists.append(str(numbers))
    elif style=='letter':
        numbers = 64
        while(numbers < 90 ):
            numbers+=1
            mylists.append(chr(numbers))        

    #return HttpResponse(mylist)
    return render(request, 'loaddropdown.html', {'mylists': mylists})    



def MoveLocationTo (request):
    existingid = request.POST.get('existingid')
    partid = request.POST.get('partid')
    warehouse = request.POST.get('warehouse')
    rack = request.POST.get('rack')
    bay = request.POST.get('bay')
    level = request.POST.get('level')
    position = request.POST.get('position')
    quantity = request.POST.get('quantity')
    
    q_objects = Q()
    q_objects &= Q(part_id=partid)
    q_objects &= Q(warehouse=warehouse)
    q_objects &= Q(rack=rack)
    q_objects &= Q(bay=bay)
    q_objects &= Q(level=level)
    q_objects &= Q(position=position)
    
    #new_location=PartsLocation.objects.filter(q_objects)
    old_location = PartsLocation.objects.get(id = existingid)
    old_qty = old_location.quantity
    old_locationid= old_location.id
    
    output="0"
    
    
    if int(quantity) <= old_qty:
        old_newqty= old_qty - int(quantity)
        
        
        try:
            new_location = PartsLocation.objects.get(q_objects)
            qty = new_location.quantity
            new_locationid= new_location.id
            newqty= qty + int(quantity)
            updatelocation = PartsLocation.objects.filter(id = new_locationid).update(quantity=newqty)
            output="1"
        except PartsLocation.DoesNotExist:  
            part_id = get_object_or_404(Parts, pk = int(partid))
                
            obj = PartsLocation.objects.create(part_id=part_id, warehouse=warehouse, rack=rack,bay=bay,level=level,position=position,quantity=int(quantity))
            output="2"
            
        if old_newqty <= 0 :
            updatelocation2 = PartsLocation.objects.filter(id = old_locationid).delete()
        else:
            updatelocation2 = PartsLocation.objects.filter(id = old_locationid).update(quantity=old_newqty)       

    #get total qty update on part
    
    
    queryset = PartsLocation.objects.filter(part_id =  int(partid))
    totals = queryset.aggregate(sum=Sum('quantity')).get('sum')



    #total = PartsLocation.objects.filter(part_id =  int(partid)).values('quantity').annotate(total_qty=Sum('quantity')).get('total_qty')
    partupdate = Parts.objects.filter(id = int(partid)).update(part_qty_in_stock=totals)   
    output = totals
    
    
    
    
    #return HttpResponseRedirect(reverse_lazy('parts-detail-page', kwargs={'pk': int(partid)}))
    return HttpResponse(output)
    #return render(request, 'loaddropdown.html', {'mylists': mylists}) 



class MoveLocation(DetailView):
    model = PartsLocation
    
    
    def get_queryset(self):
        queryset = PartsLocation.objects.filter(id=self.kwargs['pk']) 
         

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(MoveLocation, self).get_context_data(**kwargs)
        partid= PartsLocation.objects.get(id=self.kwargs['pk'])
        context['parts_location'] = PartsLocation.objects.filter(part_id__id=  partid.part_id.id)

        return context






class LocationCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):             

    permission_required = "parts.add_parts"

    model = PartsLocation    
    fields= ['warehouse','rack','bay','level','position','quantity']

    def get_form(self):
        form = super().get_form()
         
        return form    

        
    def get_context_data(self, **kwargs):  

        # combine similar locations
        purchaseid = get_object_or_404(PartsPurchase, pk = self.purchaseid)
        partid= get_object_or_404(Parts, pk = purchaseid.part_id.pk)
        
        kwargs['purchase'] = PartsPurchase.objects.get(pk =  self.purchaseid)
        kwargs['parts_location'] = PartsLocation.objects.filter(part_id =  partid.id)

        data = super(LocationCreateView, self).get_context_data(**kwargs)

        return data        

    def form_valid(self, form):
        
        self.object = form.save(commit=False)

        purchaseid = get_object_or_404(PartsPurchase, pk = self.purchaseid)
        form.instance.purchase_id=purchaseid
        partid= get_object_or_404(Parts, pk = purchaseid.part_id.pk)
        total_in_stock=partid.part_qty_in_stock
        
        form.instance.part_id = partid
        total_ordered = purchaseid.qty_ordered
        if total_ordered is None:
            total_ordered=0
        if total_in_stock is None:
            total_in_stock=0
        
        warehouse=form.instance.warehouse
        rack=form.instance.rack
        bay=form.instance.bay
        level=form.instance.level       
        position=form.instance.position
        qty=form.instance.quantity 
        
        q_objects = Q()
        q_objects &= Q(part_id=partid)
        q_objects &= Q(warehouse=warehouse)
        q_objects &= Q(rack=rack)
        q_objects &= Q(bay=bay)
        q_objects &= Q(level=level)
        q_objects &= Q(position=position)

        #exist, created = PartsLocation.objects.get_or_create(q_objects)
        #obj, created = PartsLocation.objects.filter(q_objects).get_or_create(purchase_id=purchaseid, warehouse=warehouse,rack=rack,bay=bay,level=level,position=position)
        #if created:
        #    obj.quantity = qty   
        #else:
        #   currentqty = obj.quantity
        #   obj.quantity = currentqty+qty
              
        
        try:
            if form.is_valid():
                purchaseid.qty_ordered =  total_ordered+qty
                purchaseid.save()
                
                partid.part_qty_in_stock=total_in_stock+qty
                partid.save()
                
                form.save()

        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                #form.add_error('training_employee','Employee is already in this training !!!!')
                obj = PartsLocation.objects.get(q_objects)
                currentqty = obj.quantity                
                mupdate=PartsLocation.objects.filter(q_objects).update(quantity=currentqty+qty)
                
                purchaseid.qty_ordered=  total_ordered+qty
                purchaseid.save()
                
                partid.part_qty_in_stock=total_in_stock+qty
                partid.save()
                
                return super().form_invalid(form)

        #form.add_error('warehouse','test')
        #return super().form_invalid(form)
        #self.object.save()
        #return reverse_lazy('parts-location-page', kwargs={'purchaseid': self.purchaseid}) 
        #return super().form_valid(form) 
        return super(LocationCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.purchaseid = kwargs.get('purchaseid', "")
        return super().dispatch(request,*args, **kwargs) 











