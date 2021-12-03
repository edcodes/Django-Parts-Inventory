from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import Parts, CompatibleMachines ,CompatibleMolds


class CompatibleMachinesForm(ModelForm):

    class Meta:
        model = CompatibleMachines
        exclude = ()

CompatibleMachinesFormSet = inlineformset_factory(Parts, CompatibleMachines, form=CompatibleMachinesForm, extra=1)
                                            
#====================================================================                                          

class CompatibleMoldsForm(ModelForm):
    
    class Meta:
        model = CompatibleMolds
        exclude = ()

CompatibleMoldsFormSet = inlineformset_factory(Parts, CompatibleMolds, form=CompatibleMoldsForm, extra=1)
                                            
#====================================================================   
