
from django.shortcuts import render, redirect, reverse
from . forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from accounts.views import *
from datetime import timedelta
from . paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
import string
import random
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

@login_required(login_url='/accounts/login/')
def my_tools(request):
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
                    data = Tool.objects.filter(owner=request.user,category=seleted_category,to_date__lte=selected_fromdate)
                    return render(request, 'index.html',{'loc': loc,'data': data,'data1': data1,'cat_data':cat_data})

    # data = Tool.objects.exclude(owner=request.user)
    data = Tool.objects.filter(owner=request.user)
    return render(request,'index.html',{'data': data,'data1': data1,'cat_data':cat_data})


@login_required(login_url='/accounts/login/')
def edit_tools(request,id):
    if request.method == 'POST':
        obj = Tool.objects.get(id=id)
        data1 = Location.objects.all()
        form = MapToolCreationForm(request.POST, request.FILES,instance=obj)
        if form.is_valid():
            form.save()
            return redirect(home)
        else:
            selected_location = request.POST.get('loation')
            if not selected_location == "none":
                loc = Location.objects.get(id=selected_location)
                form = MapToolCreationForm()
                edit = 'edit'
                return render(request, 'tools/add_tools.html',
                              {'loc': loc, 'data1': data1, 'form': form,'edit':edit})

            messages.error(request, 'Invalid')
            obj = Tool.objects.get(id=id)
            form = MapToolCreationForm(instance=obj)
            edit = 'edit'
            return render(request, 'tools/add_tools.html', {'form': form, 'data1': data1,'edit':edit})
    else:
        data1 = Location.objects.all()
        obj = Tool.objects.get(id=id)
        form = MapToolCreationForm(instance=obj)
        edit = 'edit'
        return render(request, 'tools/add_tools.html', {'form': form,'data1':data1,'edit':edit})

@login_required(login_url='/accounts/login/')
def delete_tools(request,id):
    obj=Tool.objects.get(id=id)
    obj.delete()
    return  redirect(home)

@login_required(login_url='/accounts/login/')
def add_tools(request):
    if request.method == 'POST':
        data1 = Location.objects.all()
        form = MapToolCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            messages.success(request, 'Successfully')
            return redirect(home)
        else:

            selected_location = request.POST.get('loation')
            if not selected_location == "none":
                loc = Location.objects.get(id=selected_location)
                form = MapToolCreationForm()
                return render(request, 'tools/add_tools.html',
                              {'loc': loc, 'data1': data1, 'form': form})


            messages.error(request, 'Invalid ')
            form = MapToolCreationForm()
            return render(request, 'tools/add_tools.html', {'form': form, 'data1': data1})
    else:
        data1 = Location.objects.all()
        form = MapToolCreationForm()
        return render(request, 'tools/add_tools.html', {'form': form,'data1':data1})

@login_required(login_url='/accounts/login/')
def tools_details(request,id):
    form = BooknowCreationForm()
    data = Tool.objects.get(id=id)
    multi = MultiplePhotos.objects.filter(tool=id)
    photos = None
    if multi:
        photos = MultiplePhotos.objects.get(tool=id)
    ratings = Rating.objects.filter(payment__order__tools=id)
    average = None
    if ratings:
        l=[]
        print(ratings)
        for i in ratings:
            l.append(i.rating)
        average = sum(l) / len(l)
        print(average)
    return render(request,'tools/tools_details.html',{'i':data,'form':form,'photos':photos,'rating':average,'review':ratings})

@login_required(login_url='/accounts/login/')
def booknow(request,id):
    if request.method == 'POST':
        mapid = Tool.objects.get(id=id)
        # if Booknow.objects.filter(tools=mapid):
        #     messages.error(request, 'you have already booked')
        #     return redirect(tools_details,id)
        print(mapid)
        form = BooknowCreationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user
            form.tools = mapid

            from_date = form.from_date
            to_date = form.to_date
            difference = to_date - from_date
            days = difference.days
            amount =days * mapid.price
            form.booked_days=days
            form.amount = amount

            user_name = request.user.first_name
            user_upper = user_name.upper()
            N = 8
            res = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=N))
            bookin_id = user_upper + str(res)

            form.booking_id = bookin_id
            form.save()
            print(form.id)

            message = f'Hello {request.user.first_name}  \n\nYour booking request is confirm. please make payment and confirm your booking \n\n Your Booking Details are' \
                      f'Booking ID : {form.booking_id}\n' \
                      f'Booking From Date : {form.from_date} \n' \
                      f'Booking To Date : {form.to_date} \n' \
                      f'Booking Days : {form.booked_days} \n' \
                      f'Amount for payment : {form.amount} \n'

            send_mail('Booking Request', message, settings.EMAIL_HOST_USER, [request.user],
                      fail_silently=True)

            return redirect(booknowdetails,form.id)

@login_required(login_url='/accounts/login/')
def booknowdetails(request,id):
    print(id)
    # mapid = MapTool.objects.get(id=id)
    book = Booking.objects.get(id=id)
    print(book)
    # messages.success(request, 'Successfully Booked')
    return render(request, 'tools/booknow.html',{'book':book})


MERCHANT_KEY='tbQubBXKkCa5IloY'

today = datetime.date.today()

@login_required(login_url='/accounts/login/')
def order(request,id):
    obj = Booking.objects.get(id=id)
    print(obj)
    user_name =  obj.tools.owner.first_name
    cus_name = request.user.first_name
    user_upper = user_name.upper()
    cus_upper = cus_name.upper()
    print(user_upper[0] + cus_upper)
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    orderid = user_upper[0] + cus_upper + str(res)

    s1 = orderid
    s2 = obj.amount

    Payment.objects.create(order=obj,amount=obj.amount,payment_id=orderid)

    param_dict = {
        'MID': 'soObkr88054489271706',
        'ORDER_ID': str(s1),
        'TXN_AMOUNT': str(s2),
        'CUST_ID': '5',
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',  # for testing
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/tools/handlerequest/',
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'payment/paytm.html', {'param_dict': param_dict})

@csrf_exempt
def handlerequest(request):  # paytm will send POST request herre
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            a = response_dict['ORDERID']
            b = response_dict['TXNID']
            c = response_dict['BANKTXNID']
            d = response_dict['TXNDATE']

            obj = Payment.objects.get(payment_id=a)
            print(obj)

            obj.status ='success'
            obj.txn_id = b
            obj.bank_txn_id = c
            obj.txn_date = d
            obj.save()

            map = Tool.objects.get(id=obj.order.tools.id)
            map.to_date = obj.order.to_date+timedelta(days=1)
            map.save()

            book = Booking.objects.get(id=obj.order.id)
            book.pay_status = 'success'
            book.save()

            message = f'Hello {book.customer.first_name}  \n\nYour booking is Confirm \n\n Your Booking Details are' \
                      f'Booking ID : {book.booking_id}\n' \
                      f'Booking From Date : {book.from_date} \n' \
                      f'Booking To Date : {book.to_date} \n' \
                      f'Booking Days : {book.booked_days} \n' \
                      f'Amount for payment : {book.amount} \n' \
                      f'Payment Status : {obj.status}\n' \
                      f'Transaction Id : {obj.txn_id} \n' \
                      f'Bank Transaction Id: {obj.bank_txn_id} \n' \
                      f'Bank Transaction Date : {obj.txn_date} \n' \
                      f'Paied Amount : {obj.amount} \n'
            send_mail('Booking Confirmation', message, settings.EMAIL_HOST_USER, [book.customer],
                              fail_silently=True)


        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return redirect('show_payment') 

@login_required(login_url='/accounts/login/')
def show_my_booking(request):
    data= Booking.objects.filter(customer=request.user)
    return render(request, 'tools/show_my_booking.html',{'data':data})

@login_required(login_url='/accounts/login/')
def complete_payment(request, id):
    try:
        booking = Booking.objects.get(id=id)
        if booking.from_date >= booking.tools.to_date:
            return render(request, 'tools/booknow.html',{'book':booking})
        else:
            messages.error(request, "Tool is not available on selected dates.")
            return redirect('show_my_booking')
    except:
        messages.error(request, "Booking Not Found.")
        return redirect('show_my_booking')


@login_required(login_url='/accounts/login/')
def show_payment(request):
    data= Payment.objects.filter(order__customer=request.user)
    return render(request, 'tools/show_payment.html',{'data':data})

@login_required(login_url='/accounts/login/')
def owner_payment(request):
    data= Payment.objects.filter(order__tools__owner=request.user,status='successful')
    print(data)
    return render(request, 'tools/owner_payment.html',{'data':data})

@login_required(login_url='/accounts/login/')
def add_multipleimages(request,id):
    obj = Tool.objects.get(id=id)
    if request.method == 'POST':
        form = MultiplePhotosForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.tool = obj
            form.save()
            messages.success(request, 'Successfully')
            return redirect(tools_details,id)
        else:
            messages.error(request, 'Invalid ')
            form = MultiplePhotosForm()
            return render(request, 'tools/add_multipleimages.html', {'form': form})
    else:
        form = MultiplePhotosForm()
        return render(request, 'tools/add_multipleimages.html', {'form': form})

@login_required(login_url='/accounts/login/')
def save_tools(request,id):
    tools = Tool.objects.get(id=id)
    save = Save_Tools.objects.create(customer=request.user,tool=tools,)
    save.save()
    messages.success(request, 'Saved Successfully')
    return redirect(tools_details,id)

@login_required(login_url='/accounts/login/')
def save_for_later(request):
    data = Save_Tools.objects.filter(customer=request.user)
    return render(request,'tools/save_for_later.html',{'data': data})

@login_required(login_url='/accounts/login/')
def delete_save(request,id):
    obj=Save_Tools.objects.get(id=id)
    obj.delete()
    messages.success(request, 'Remove Successfully')
    return redirect(home)

@login_required(login_url='/accounts/login/')
def rating(request,id):
    if request.method == 'POST':
        selected_rating = request.POST.get('star')
        selected_review = request.POST.get('review')
        print(selected_rating)

        obj = Payment.objects.get(id=id)
        if Rating.objects.filter(customer=request.user, payment=obj):
            messages.error(request, 'already Rated')
            return redirect(show_payment)
        Rating.objects.create(customer=request.user,payment=obj,rating=selected_rating,review=selected_review)

        ratings = Rating.objects.filter(payment__order__tools=obj.order.tools)
        average = None
        if ratings:
            l = []
            print(ratings)
            for i in ratings:
                l.append(i.rating)
            average = sum(l) / len(l)
            tools = Tool.objects.get(id=obj.order.tools.id)
            tools.rating=average
            tools.save()
            print(average)

        messages.success(request, 'Rate Successfully')
        return redirect(show_payment)
    else:
        return render(request, 'tools/rating.html')


