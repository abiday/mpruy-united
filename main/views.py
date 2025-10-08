import datetime
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ShopForm  
from main.models import Shop
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.serializers import serialize

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

@csrf_exempt
def create_product_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required'
        }, status=401)

    if request.method == 'POST':
        try:
            # Create new product
            product = Shop.objects.create(
                user=request.user,
                name=request.POST.get('name'),
                price=request.POST.get('price'),
                description=request.POST.get('description'),
                category=request.POST.get('category'),
                thumbnail=request.POST.get('thumbnail', ''),
                second_image=request.POST.get('second_image', ''),
                is_featured=request.POST.get('is_featured') == 'on'
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Product created successfully',
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': str(product.price),
                    'description': product.description,
                    'category': product.category
                }
            })
        except Exception as e:
            import traceback
            print(f"Error creating product: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@require_http_methods(["GET"])
def get_products_json(request):
    try:
        products = Shop.objects.all()
        products_data = []
        
        for product in products:
            # Safely get image URLs
            image_url = ''
            second_image_url = ''
            
            try:
                if product.image:
                    image_url = product.image.url
            except (ValueError, AttributeError):
                image_url = ''
            
            try:
                if product.second_image:
                    second_image_url = product.second_image.url
            except (ValueError, AttributeError):
                second_image_url = ''
            
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'description': product.description,
                'category': product.category,
                'image_url': image_url,
                'second_image_url': second_image_url,
                'user_id': str(product.user.id) if product.user else None,
                'is_featured': product.is_featured
            })
        
        return JsonResponse(products_data, safe=False)
    except Exception as e:
        import traceback
        print(f"Error in get_products_json: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def update_product_ajax(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required'
        }, status=401)

    product = get_object_or_404(Shop, id=id)
    
    if product.user != request.user:
        return JsonResponse({
            'status': 'error',
            'message': 'Not authorized'
        }, status=403)

    if request.method == 'POST':
        try:
            product.name = request.POST.get('name', product.name)
            product.price = request.POST.get('price', product.price)
            product.description = request.POST.get('description', product.description)
            product.category = request.POST.get('category', product.category)
            product.thumbnail = request.POST.get('thumbnail', product.thumbnail)
            product.second_image = request.POST.get('second_image', product.second_image)
            product.is_featured = request.POST.get('is_featured') == 'on'
            
            product.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Product updated successfully'
            })
        except Exception as e:
            import traceback
            print(f"Error updating product: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@csrf_exempt
def delete_product_ajax(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required'
        }, status=401)
    
    try:
        product = Shop.objects.get(id=id)
        
        if product.user != request.user:
            return JsonResponse({
                'status': 'error',
                'message': 'Not authorized'
            }, status=403)
            
        product.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Product deleted successfully'
        })
    except Shop.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found'
        }, status=404)
    except Exception as e:
        import traceback
        print(f"Error deleting product: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def login_ajax(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': 'Successfully logged in!'
            })
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid username or password.'
        }, status=401)

@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Username already exists'
            }, status=400)
        
        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': 'Successfully registered!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return render(request, 'register.html')

@csrf_exempt
def logout_ajax(request):
    logout(request)
    return JsonResponse({
        'status': 'success',
        'message': 'Successfully logged out!'
    })