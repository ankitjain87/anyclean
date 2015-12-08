from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from anyclean import controllers, models, decorators


@login_required
@decorators.has_cc_permission
def dashboard(request):
    return render(request, 'cc/dashboard.html')


@login_required
@decorators.has_cc_permission
def search_page(request):
    return render(request, 'cc/search.html')


@login_required
@decorators.has_cc_permission
def search(request):
    return render(request, 'cc/search.html')


@login_required
@decorators.has_cc_permission
def assign_pickup(request):
    pickups = controllers.get_all_pickups()





def zohoverify(request):
    return render(request, 'verifyforzoho.html')



# Customer Care services
def search_customer(request):
    '''Search customer by cid, name, mobile, email.'''
    input = request.REQUEST.get('input')
    search_by = request.REQUEST.get('search_by')

    cust_detail = controllers.search_customer(input, search_by)


# Place order service
def place_order(request):
    order_type = request.REQUEST.get('order_type')
    order_date = request.REQUEST.get('order_date')
    quantity = request.REQUEST.get('quantity')
    weight = request.REQUEST.get('weight')
    order_date = request.REQUEST.get('order_date')

