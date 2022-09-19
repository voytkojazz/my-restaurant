from django.urls import path

from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('ingridients/', views.IngridientView.as_view(), name='ingridients-list'),
    path('menu/', views.MenuItemListView.as_view(), name='menu-items-list'),
    path('purchases/',  views.PurchaseListView.as_view(), name='purchase-list'),
    path('profit-revenue/', views.ProfitRevenueView.as_view(), name='profit-revenue'),
    path('purchases/<int:year>/', views.PurchaseYearArchiveView.as_view(), name='purhase_year_archive'),
    path('ingridients/create/', views.IngridientCreateView.as_view(), name='ingridient-create'),
    path('menu/create/', views.MenuItemCreateView.as_view(), name='menu-item-create'),
    path('menu/<int:menu_item_pk>/requirements/', views.manage_requirements, name='menu-item-requirements'),
    path('purchases/create/', views.PurchaseCreateView.as_view(), name='purchase-create'),
    path('ingridients/<int:ingridient_pk>/update', views.ingridient_update_view, name='ingridient-update'),
    path('menu/<int:pk>/delete', views.MenuItemDeleteView.as_view(), name='menu-item-delete'),
]
