from django.urls import path, include
from django.shortcuts import render, get_object_or_404
from simpellab.modules.sales.models import SalesOrder


def sales_order_public_view(request, instance_id):
    obj = get_object_or_404(SalesOrder, pk=instance_id)
    return render(request, 'invoice_public.html', context={'obj': obj})


urlpatterns = [
    path(
        'invoice/<str:instance_id>/',
        sales_order_public_view,
        name='sales_salesorder_inspect_public'),
    path(
        'sales/<str:instance_id>/',
        sales_order_public_view,
        name='sales_invoice_inspect_public')
]