 
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, TemplateView, CreateView, DeleteView
from django.views.generic import YearArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import count_profit_revenue
from .models import Ingridient, MenuItem, Purchase, RecipeRequirement
from .filters import PurchaseFilter, IngridientFilter
from .forms import IngridientForm, RecipeRequirementForm, MenuItemCreateForm, RecipeRequirementFormSet
from django.urls import reverse_lazy, reverse
from django.forms import formset_factory, inlineformset_factory
from accounts.decorators import not_unautheticated_user
from django.contrib import messages
# Create your views here.
class CustomLoginRequiredMixin(LoginRequiredMixin):

    permission_denied_message = 'You have to be logged in to access that page'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING,
                             self.permission_denied_message)
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )




class IngridientView(View):

    def get(self, request):
        all_ingridients = Ingridient.objects.all()
        f = IngridientFilter(request.GET, queryset=all_ingridients)
        all_ingridients = f.qs
        context = {
            'all_ingridients': all_ingridients,
            'myFilter': f,
        }
        return render(request, 'inventory/ingridients-list.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            ingridients_ids = request.POST.getlist('id[]')
            for id in ingridients_ids:
                ingridient = Ingridient.objects.get(pk=id)
                ingridient.delete()
            return redirect('ingridients-list')



class MenuItemListView(ListView):
    model = MenuItem
    context_object_name = 'menu_items_list'
    template_name = 'inventory/menu-items-list.html'





class PurchaseListView(CustomLoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login-page')
    permission_denied_message = 'In order to view this page, please log in...'
    def get(self, request):
        purchases_list = Purchase.objects.all()
        f = PurchaseFilter(request.GET, queryset=purchases_list)
        purchases_list = f.qs.order_by('-timestamp')
        purchases = {}
    
        for purchase in purchases_list:
            purchase_rr = purchase.menu_item.reciperequirement_set.all()
            purchase_revenue = 0
            for rr in purchase_rr:
                quantity_to_cook = rr.quantity
                quantity_of_ingridient = rr.ingridient.quantity
                price_of_unit = rr.ingridient.unit_price
                price_of_unit_to_cook = quantity_to_cook * (price_of_unit / quantity_of_ingridient)
                purchase_revenue += price_of_unit_to_cook
                
            purchases[purchase] = {
                'menu_item': None,
                'timestamp': None,
                'profit': None,
            }

            purchases[purchase]['menu_item'] = purchase.menu_item.title
            purchases[purchase]['timestamp'] = purchase.timestamp
            purchases[purchase]['profit'] = purchase.menu_item.price - purchase_revenue

#         revenue, profit = count_profit_revenue(purchases.keys())
        

        context = {
            'purchases_dict': purchases,
            'myFilter': f,
#             'revenue': revenue,
#             'profit': profit,
        }

        return render(request, 'inventory/purchase-list.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            purchases_ids = request.POST.getlist('id[]')
            for id in purchases_ids:
                ingridient = Purchase.objects.get(pk=id)
                ingridient.delete()
            return redirect('purchase-list')


        


# class ProfitRevenueView(TemplateView):
#     template_name = 'inventory/profit-revenue.html'
#     purchases = Purchase.objects.all()
#     revenue, profit = count_profit_revenue(purchases)
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs) 
#         context['revenue'] = self.revenue
#         context['profit'] = self.profit
#         return context


class Home(TemplateView):
    template_name = 'inventory/home.html'
    

class PurchaseYearArchiveView(YearArchiveView):
    queryset = Purchase.objects.all()
    date_field = 'timestamp'
    make_object_list = True
    allow_future = False
    template_name = 'inventory/purchase-year-archive.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['revenue'] = count_profit_revenue(context['object_list'])[0]
        context['profit'] = count_profit_revenue(context['object_list'])[1]
        return context



class IngridientCreateView(CustomLoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login-page')

    model = Ingridient
    form_class = IngridientForm
    success_url = reverse_lazy('ingridients-list')
    template_name = 'inventory/ingridient-create.html'





class MenuItemCreateView(CustomLoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login-page')

    model = MenuItem
    form_class = MenuItemCreateForm
    success_url = reverse_lazy('menu-items-list')
    template_name = 'inventory/menu-item-create.html'
    

@not_unautheticated_user
def manage_requirements(request, menu_item_pk):
    menu_item = MenuItem.objects.get(pk=menu_item_pk)
    formset_class = RecipeRequirementFormSet
    if request.method == 'POST':
        formset = formset_class(request.POST, request.FILES, instance=menu_item)
        if formset.is_valid():
            formset.save()
            return redirect('menu-items-list')
    else:
        formset = formset_class(instance=menu_item)
        context = {
            'formset': formset,
            'menu_item_pk': menu_item_pk,
        }
        return render(request, 'inventory/menu-item-requirements.html', context)



class PurchaseCreateView(CustomLoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login-page')

    template_name = 'inventory/purchase-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = [X for X in MenuItem.objects.all()]
        return context

    def post(self, request):
        menu_item_id = request.POST['menu_item']
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)

        for requirement in requirements.all():
            required_ingridient = requirement.ingridient
            required_ingridient.quantity -= requirement.quantity
            required_ingridient.save()

        purchase.save()
        return redirect('purchase-list')


@not_unautheticated_user
def ingridient_update_view(request, ingridient_pk):
    ingridient = Ingridient.objects.get(pk=ingridient_pk)
    form = IngridientForm(instance=ingridient)

    if request.method == 'POST':
        form = IngridientForm(request.POST, instance=ingridient)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingridients-list')

    context = {'form': form}
    return render(request, 'inventory/ingridient-update.html', context)


class MenuItemDeleteView(DeleteView):
    model = MenuItem
    success_url = reverse_lazy('menu-items-list')


