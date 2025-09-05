from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'appname' : 'Mpruy United Shop',
        'name': 'Abid Dayyan Putra Rahardjo',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)

