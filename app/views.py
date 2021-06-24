from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Cart, Customer, OrderPlaced, Mulytic_labs_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from .forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from qrcode import *
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from uuid import uuid4
from io import BytesIO

def mulytic_view(request):
    forms = MulyticForm()
    if request.method == 'POST':     
        forms = MulyticForm(request.POST)
        if forms.is_valid():
            obj = forms.save(commit=False)
            eventid = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            img = make(eventid)
            img.save("media/qr_code/"+eventid+".png")              
            obj.qr_code =  "qr_code/"+eventid+".png"     
            obj.save()

    context = {
        'forms': forms
    }
    return render(request, 'app/mulytic.html', context)

def render_pdf_view(request):
    data = Mulytic_labs_test.objects.all().last()
    # data = Mulytic_labs_test.objects.get(id=1)
    context={
        'data':data
    }
    template_path = 'product_page/convert_to_pdf.html'
    context = {'data':data}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('we had some errors <pre>'+html+'</pre>')
    return response

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type="application/pdf")
#     return None



# def convert_to_pdf(request):
#     data = Mulytic_labs_test.objects.all().last()
#     context={
#         'data':data
#     }
#     pdf = render_to_pdf('product_page/convert_to_pdf.html', context)
#     if pdf:
#         response = HttpResponse(pdf, content_type="application/pdf")
#         content = "inline; filename=contact.pdf"
#         response['Content-Disposition']=content
#         return response
#     return HttpResponse("Not Found")

# def convert_to(request):
#     data = Mulytic_labs_test.objects.all().last()
#     context={
#         'data':data
#     }
#     return render(request, 'product_page/convert_to_pdf.html', context)


def pro_quantity_check(request):
    p_available = True
    if request.method == 'GET':
        pro_quantity = int(request.GET.get('prod_quantity'))
        product_code = int(request.GET.get('product_code'))
        product = Product.objects.get(id=product_code)
        if product.quantity < pro_quantity:
            p_available = False
        data = {
            'product_available':p_available
        }
        return JsonResponse(data)


class ProductView(View):
    def get(self, request):
        top_products = Product.objects.all()
        context ={
         'products': top_products
        }
        return render(request, 'app/home.html', context)


def product_details(request, pk):
    check = False
    if request.user.is_authenticated:
        check = Cart.objects.filter(product=pk, user=request.user).exists()
    product = Product.objects.get(pk=pk)
    context = {
        'product': product,
        'item_already_in_cart': check
    }
    return render(request, 'product_page/productdetails.html', context)

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('showcart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        if cart:
            amount = 0.0
            shipping_amt = 70.0
            for c in cart:
                amount += c.quantity * c.product.selling_price
            total_amt=amount+shipping_amt
            context ={
                'carts': cart,
                'amount': amount,
                'total_amt': total_amt,
            }
            return render(request, 'app/addtocart.html', context)
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == "GET":
        pro_id=request.GET['prod_id']
        print(pro_id, "PRODUCT ID")
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        cart = Cart.objects.filter(user=request.user)
        amount = 0.0
        shipping_amt = 70.0
        for c in cart:
            amount += c.quantity * c.product.selling_price
        total_amt = amount + shipping_amt
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amt
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        print(prod_id, "PRODUCT ID")
        p = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        p.quantity-=1
        p.save()
        products = Cart.objects.filter(user=request.user)
        amount = 0.0
        shipping_amt = 70.0
        for c in products:
            amount += c.quantity * c.product.selling_price
        total_amt = amount + shipping_amt
        data = {
            'quantity': p.quantity,
            'amount': amount,
            'total_amount': total_amt
        }
        return JsonResponse(data)


def remove_item(request):
    prod_id = request.GET['prod_id']
    prod_obj = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    prod_obj.delete()
    cart = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amt = 70.0
    for c in cart:
        amount += c.quantity * c.product.selling_price
    total_amt = amount + shipping_amt
    data = {
        'amount': amount,
        'total_amount': total_amt
    }
    return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

@method_decorator(login_required, name='dispatch')
class CustomerView(View):
    def get(self, request):
        forms = CustomerForm()
        context = {
            'forms': forms
        }
        return render(request, 'app/profile_address.html', context)

    def post(self, request):
        forms = CustomerForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            district = forms.cleaned_data['district']
            city = forms.cleaned_data['city']
            zipcode = forms.cleaned_data['zipcode']
            Customer.objects.create(
                user=request.user,
                name = name,
                address = address,
                district = district,
                city = city,
                zipcode = zipcode
            )
            return redirect('home')
        context = {
            'forms':forms
        }
        return render(request, 'app/profile_address.html', context)

@login_required
def address(request):
    address = Customer.objects.filter(user=request.user)
    context={
        'address':address
    }
    return render(request, 'app/address.html', context)

@login_required
def orders(request):
    orderplaced= OrderPlaced.objects.filter(user=request.user)
    context={
        'order_placed': orderplaced
    }
    return render(request, 'app/orders.html', context)

def change_password(request):
    if request.method == 'POST':
        forms = UserPasswordChangeForm(request.user, request.POST)
        if forms.is_valid():
            forms.save()
            update_session_auth_hash(request, request.user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changepassword')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        forms = UserPasswordChangeForm(request.user)
    context = {
        'forms': forms
    }
    return render(request, 'app/changepassword.html', context)


def mobile(request, data=None):
    if data == 'samsung' or data == 'redme':
        mobiles = Product.objects.filter(category='mobile', brand=data)
    elif data == 'below_10000':
        mobiles = Product.objects.filter(category='mobile', selling_price__lte=10000)
    elif data == 'above_10000':
        mobiles = Product.objects.filter(category='mobile', selling_price__gte=10000)
    else:
        mobiles = Product.objects.filter(category='mobile')
    return render(request, 'product_page/mobile.html', {'mobile':mobiles})


def ware(request, data=None):
    if data == 'top_wear' or data == 'bottom_wear':
        ware = Product.objects.filter(category=data)
    else:
        top_ware = Product.objects.filter(category='top_wear')
        bottom_ware = Product.objects.filter(category='bottom_wear')
        ware = top_ware | bottom_ware
    return render(request, 'product_page/top_wear.html', {'wares': ware})


class Userlogin(View):
    def get(self, request):
        forms = LoginForm()
        print("GET METHOD")
        context = {
            'forms':forms
        }
        return render(request, 'app/login.html', context)

    def post(self, request):
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Invalid Username or Password")
                return redirect('login')
        return render(request, 'app/home.html', {'forms': forms})


    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(username=username, password=password)
    #     print("USER", user)
    #     if user:
    #         login(request,user)
    #         messages.success(request, "Welcome to Online Shop.")
    #         return redirect('home')
    #     else:
    #         print("Errors")
    # return render(request, 'app/login.html')


def userlogout(request):
    logout(request)
    return redirect('home')

class Registration(View):
    def get(self, request):
        forms = RegistrationForm()
        context = {
            'forms': forms
        }
        return render(request, 'app/customerregistration.html', context)
    def post(self, request):
        forms = RegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Congratulations,Registration Success.")
            return redirect('customerregistration')
        context = {
            'forms': forms
        }
        return render(request, 'app/customerregistration.html', context)


# def customerregistration(request):
#     if request.method == 'POST':
#         email = request.POST['Email']
#         pass1 = request.POST['Password1']
#         pass2 = request.POST['Password2']
#         if pass1 == pass2:
#             print("Email:", email)
#         else:
#             messages.error(request, "Two passwords are different")
#     return render(request, 'app/customerregistration.html')

@login_required
def checkout(request):
    user = request.user
    carts_products = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_price = 70.0
    for c in carts_products:
        amount += c.quantity * c.product.selling_price
    total_amount = amount + shipping_price
    addresses = Customer.objects.filter(user=user)
    context = {
        'total_amount': total_amount,
        'carts_products': carts_products,
        'addresses': addresses
    }
    return render(request, 'app/checkout.html', context)


def payment_done(request):
    user = request.user
    cust_id = request.GET.get('custid')
    customer = Customer.objects.get(id=cust_id)
    carts = Cart.objects.filter(user=user)
    for c in carts:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')