from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Handle Login baik jika Flutter mengirim Form Data maupun JSON
        username = ""
        password = ""
        
        # Cek apakah request berupa JSON
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except (json.JSONDecodeError, AttributeError):
            # Jika bukan JSON, coba ambil dari Form Data (fallback)
            username = request.POST.get('username')
            password = request.POST.get('password')

        # Autentikasi
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login successful!"
                }, status=200)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Account is disabled."
                }, status=401)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, check your credentials."
            }, status=401)

    return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # INIT VARIABLE
        username = ""
        password = ""
        
        # --- HYBRID DATA LOADING (JSON OR FORM DATA) ---
        try:
            # Coba baca sebagai JSON dulu
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except (json.JSONDecodeError, AttributeError, TypeError):
            # Jika gagal decode JSON, berarti dikirim sebagai Form Data (request.post default Flutter)
            # Fallback ke request.POST
            username = request.POST.get('username')
            password = request.POST.get('password')
        
        # --- VALIDATION ---
        if not username or not password:
            return JsonResponse({
                "status": False, 
                "message": "Username and password required"
            }, status=400)

        # --- BUSINESS LOGIC ---
        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": False, "message": "Username already exists"}, status=409)

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "User created successfully!"
            }, status=201)
        except Exception as e:
             return JsonResponse({"status": False, "message": f"Error creating user: {str(e)}"}, status=500)

    return JsonResponse({"status": False, "message": "Invalid method"}, status=405)

@csrf_exempt
def logout(request):
    # Ambil username sebelum logout untuk pesan (opsional, handle jika user belum login)
    username = request.user.username if request.user.is_authenticated else "Guest"
    
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)