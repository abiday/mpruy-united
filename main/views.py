import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ShopForm  
from main.models import Shop
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_main(request):
    shop_products = Shop.objects.all()  

    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        shop_products = Shop.objects.all()
    else:
        shop_products = Shop.objects.filter(user=request.user)

    context = {
        'npm': '2406356580',
        'name': 'Abid Dayyan',
        'class': 'PBP F',
        'shop_products': shop_products,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)


@login_required(login_url='/login')
def create_product(request): 
    form = ShopForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id): 
    product = get_object_or_404(Shop, pk=id)  
    
    context = {
        'product': product 
    }

    return render(request, "product_detail.html", context) 

def show_xml(request):
     shop_list = Shop.objects.all()
     xml_data = serializers.serialize("xml", shop_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    shop_list = Shop.objects.all()
    json_data = serializers.serialize("json", shop_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
   try:
       shop_product = Shop.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", shop_product)
       return HttpResponse(xml_data, content_type="application/xml")
   except Shop.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, product_id):
   try:
       shop_product = Shop.objects.get(pk=product_id)
       json_data = serializers.serialize("json", [shop_product])
       return HttpResponse(json_data, content_type="application/json")
   except Shop.DoesNotExist:
       return HttpResponse(status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Shop, pk=id)
    if product.user != request.user:
        return HttpResponseRedirect(reverse('main:show_main'))
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Shop, pk=id)
    if product.user != request.user:
        return HttpResponseRedirect(reverse('main:show_main'))
    
    form = ShopForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)