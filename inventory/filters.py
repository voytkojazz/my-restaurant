from typing import Text
import django_filters
from django_filters import DateFilter, ModelChoiceFilter, ChoiceFilter
from .models import Ingridient, Purchase, MenuItem
from django.forms.widgets import TextInput
from django.forms.widgets import Select

class PurchaseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='timestamp', lookup_expr='gte', label='Display from: ', widget=TextInput(attrs={'placeholder': '(mm/dd/yyyy)'}))
    end_date = DateFilter(field_name='timestamp', lookup_expr='lte', label='Display until:', widget=TextInput(attrs={'placeholder': '(mm/dd/yyyy)'}))
    menu_item = ModelChoiceFilter(label='Choose Menu Item:', queryset=MenuItem.objects.all(), widget=Select(attrs={'class': 'form-select'}), empty_label='..select..')
    class Meta:
        model = Purchase
        fields = ['start_date', 'end_date', 'menu_item']


class IngridientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Search by name'}))
    unit = django_filters.ChoiceFilter(choices=Ingridient.UNIT_CHOICES, widget=Select(attrs={'class': 'form-select'}), empty_label='search by unit')

    class Meta:
        model = Ingridient
        fields = ['name', 'unit']
        