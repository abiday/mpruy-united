from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ShopForm  
from main.models import Shop  
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    shop_items = Shop.objects.all()  

    context = {
        'npm': '2406356580',
        'name': 'Abid Dayyan',
        'class': 'PBP F',
        'shop_items': shop_items 
    }

    return render(request, "main.html", context)

def create_item(request): 
    form = ShopForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_item.html", context) 

def show_item(request, id): 
    item = get_object_or_404(Shop, pk=id)  
    
    context = {
        'item': item 
    }

    return render(request, "item_detail.html", context) 

def show_xml(request):
     shop_list = Shop.objects.all()
     xml_data = serializers.serialize("xml", shop_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    shop_list = Shop.objects.all()
    json_data = serializers.serialize("json", shop_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, item_id):
   try:
       shop_item = Shop.objects.filter(pk=item_id)
       xml_data = serializers.serialize("xml", shop_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Shop.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, item_id):
   try:
       shop_item = Shop.objects.get(pk=item_id)
       json_data = serializers.serialize("json", [shop_item])
       return HttpResponse(json_data, content_type="application/json")
   except Shop.DoesNotExist:
       return HttpResponse(status=404)