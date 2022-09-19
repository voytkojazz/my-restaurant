from django import forms

from .models import Ingridient, MenuItem, RecipeRequirement

class IngridientForm(forms.ModelForm):
    class Meta:
        model = Ingridient
        fields = '__all__'
        exclude = ('slug',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of ingridient'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'How many units has an ingridient'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price of ingridient'}),
        }
        labels = {
            'name': 'Name of new ingridient',
            'quantity': 'How many units',
            'unit': '...select unit...',
            'unit_price': 'Price of ingridient',
        }


class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = '__all__'
        widgets = {
            'menu_item': forms.Select(attrs={'class': 'form-select'}),
            'ingridient': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'quantity'}),
        }
        labels = {
            'menu_item': 'Menu item',
            'ingridient': 'Ingridient',
            'quantity': 'Quantity',
        }


class MenuItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'



RecipeRequirementFormSet = forms.inlineformset_factory(MenuItem, RecipeRequirement, fields=('ingridient', 'quantity'), widgets={
            'menu_item': forms.Select(attrs={'class': 'form-select'}),
            'ingridient': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'quantity'}),
        })

