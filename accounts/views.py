from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from tools.models import *
from django.contrib.auth.decorators import login_required

def home(request):
    cat_data = Tool.objects.values('category').distinct()
    data1 = Location.objects.all()

    if request.method == 'POST':
        selected_location = request.POST.get('loation')
        seleted_category = request.POST.get('category')
        selected_fromdate = request.POST.get('from_date')
        selected_todate = request.POST.get('to_date')
        if not selected_location == "none":
            if not selected_todate == None and not selected_fromdate == None:
                if not seleted_category == "none":
                    loc = Location.objects.get(id=selected_location)
                    data = Tool.objects.exclude(owner=request.user).filter(category=seleted_category,to_date__lte=selected_fromdate)
                    return render(request, 'index.html',{'loc': loc,'data': data,'data1': data1,'cat_data':cat_data})

    data = Tool.objects.exclude(owner=request.user)
    # data = Tool.objects.all()
    return render(request,'index.html',{'data': data,'data1': data1,'cat_data':cat_data})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.email = form.username
            form.save()
            messages.success(request, 'Account Created Successfully')
            return redirect(login_user)
        else:
            form = UserRegistrationForm()
            messages.error(request, 'Invalid')
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

# def customer_register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form=form.save(commit=False)
#             form.is_customer=True
#             form.email = form.username
#             form.save()
#             messages.success(request, 'Account Created Successfully')
#             return redirect(home)
#         else:
#             form = UserRegistrationForm()
#             messages.error(request, 'Invalid')
#             return render(request, 'accounts/customer_register.html', {'form': form})
#     else:
#         form = UserRegistrationForm()
#         return render(request, 'accounts/customer_register.html', {'form': form})

def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successfully')
            return redirect(home)
        else:
            messages.error(request,'Invalid email or Password')
            return render(request, 'accounts/login.html')
    else:
        return render(request,'accounts/login.html')

@login_required(login_url='/accounts/login/')
def logout_user(request):
    logout(request)
    return redirect(login_user)
