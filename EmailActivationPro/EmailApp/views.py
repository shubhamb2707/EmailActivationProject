from django.shortcuts import render
from .models import User, Product ,Order , Promo_codes, Wish
from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .forms import *
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
#for Email varification line no 13 to 19
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
#from django.contrib.auth.models import User
from django.core.mail import EmailMessage


from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib import messages

#@login_required(login_url='/login/')
def index(request):
	if request.method == "POST":
		name = request.POST.get("name")
		product = request.POST.get("product")
		shubh=request.user.username
		cart = request.session.get("cart")
		if cart:
			# quantity = cart.get("cart")
			# if quantity:
			#   cart[product] = quantity+1
			if product in cart:
				val = cart[product]
				if val:
					cart[product]= val+1
				else:
					cart[product] = 1
			else:
				cart.update({product:1}) 
		else:
			
			cart = {}
			cart[product] = 1

		request.session["cart"] = cart
		# x=(request.session["cart"])
		# c_id = int(product)
		# m=cart[product]
		# product = Product.objects.get(id = c_id)
		# return render(request,"cart.html",{"m":m,"x":product,'media_url':settings.MEDIA_URL})
		return redirect("/cart/")
	else:
		wishdata = Wish.objects.all()
		datalist=[]
		for k in wishdata:
			datalist.append(int(k.product))
		product = Product.objects.all()
		return render(request,"index.html",{"datalist":datalist,"product":product,'media_url':settings.MEDIA_URL})



# def cart(request):
#   # import pdb;
#   # pdb.set_trace()
#   x=(request.session["cart"])
#   o=list(x.keys())
#   NewList=[]
#   for val in o:
#       nval = Product.objects.get(id=int(val))
#       NewList.append(nval)

#   valueList = list(x.values())
#   res = dict(zip(NewList, valueList)) 
#   New = res.items()

#   totalprice  = 0
#   for key, value in x.items():
#       getid = Product.objects.get(id = int(key))
#       product_price = (getid.price)
#       multiplication = (product_price*value)
#       totalprice = (totalprice + multiplication)
#   return render(request, "cart.html", {"New":New, "totalprice":totalprice, 'media_url':settings.MEDIA_URL})

def cart(request):
	x=(request.session["cart"])
	o=list(x.keys())
	NewList=[]
	for val in o:
		nval = Product.objects.get(id=int(val))
		NewList.append(nval)

	valueList = list(x.values())
	res = dict(zip(NewList, valueList)) 
	New = res.items()

	totalprice  = 0
	for key, value in x.items():
		getid = Product.objects.get(id = int(key))
		product_price = (getid.price)
		multiplication = (product_price*value)
		totalprice = (totalprice + multiplication)

	# import pdb;
	# pdb.set_trace()

	var_promo = request.POST.get("promo_code")
	
	
	Dict = {}
	all_promo_code=Promo_codes.objects.all()
	for x in all_promo_code:
		Dict.update({x.code : x.value})
	request.session["Dict"] = Dict

	SessionVar = request.session.get("Dict")

	discount = 0
	Total = totalprice+10

	discountsession = request.session.get("discountsession")

	# import pdb; pdb.set_trace()
	if var_promo in SessionVar:
		discount = SessionVar[var_promo]
		
		# mssg = "promo code is applicable"

		if discountsession:
			discountsession.update({"discount":discount})

		else:
			discountsession = {}
			discountsession["discount"]=discount
			request.session["discountsession"]=discountsession
		varr = discountsession["discount"]
	else:       
		
		discountsession = {}
		discountsession["discount"]=discount
		if discountsession["discount"] != 0:
			varr = discountsession["discount"]
			# mssg = "promo code is applicable"
		else:
			varr = 0
			# mssg = "promo code is not applicable"
	
	
	removediscount = request.POST.get("remove_btn")
	if removediscount:
		discountsession.update({"discount":0})
		# discountsession["discount"]=0
		request.session["discountsession"] = discountsession
		varr = discountsession["discount"]

	Total = Total-varr
	User_Name = request.user.first_name
	return render(request, "cart.html", {"User_Name":User_Name,"discountsession":varr,"New":New, "Total":Total, "totalprice":totalprice, 'media_url':settings.MEDIA_URL})

	
	

	# Dis_session = all_promo_code[0]
	# Dis_session = request.session.get("Dis_session")
	
	# discount = 0
	# Total = totalprice+10
	# if var_promo in Dis_session:
	#   discount = discount + Dis_session[var_promo]
	#   Total = Total-discount
	#   mssg = "promo code is applicable"
	# else:
	#   mssg = "promo code is not applicable"



	# var_promo = request.POST.get("promo_code")
	# all_promo_code=Promo_codes.objects.all().filter(code=var_promo)
	# Total=totalprice+10
	
	# if len(all_promo_code) != 0:
	#   promo_code_value = all_promo_code[0].value
	#   print(promo_code_value)
	#   taxes = 10
	#   Total = Total - promo_code_value
	#   mssg = "Promo code is Applied"
	#   discount = all_promo_code[0].value

	# else:
	#   mssg = "Promo Code is not Applicable"
	#   discount = 0


	# return render(request, "cart.html", {"discount":discount,"mssg":mssg,"New":New, "Total":Total, "totalprice":totalprice, 'media_url':settings.MEDIA_URL})


def removecart(request):
	# import pdb;
	# pdb.set_trace()

	query = request.GET.get("query_name")
	x=(request.session["cart"])
	if x[query] > 1:
		x[query]= x[query]-1

	else:
		del x[query]

	request.session["cart"] = x
	return redirect("/cart/")


def increase_cart_item(request):
	# import pdb;
	# pdb.set_trace()
	
	query = request.GET.get("query_name")
	x=(request.session["cart"])
	x[query]= x[query]+1

	request.session["cart"] = x
	return redirect("/cart/")



def checkout(request):
	# import pdb;pdb.set_trace()
	# order = request.session.get("order")
	if request.method == "POST":
		import pdb;
		pdb.set_trace()
		Total = request.POST.get("Total")
		Discount = request.POST.get("Discount")
		Taxes = request.POST.get("Taxes")

		delivery_address = request.POST.get("delivery_address")
		Payment_Options = request.POST.get("Payment_Options")
		BillName = request.POST.get("BillName")
		CartPrice = request.POST.get("Total")
		Email =  request.POST.get("Email")
		totalprice = request.POST.get("Total")

		order = request.session.get("order")
		
		if order:
			
			order.update({BillName:totalprice})
			
		else:
			order = {}
			order[BillName] = totalprice
			
		# x=(request.session["order"])


		request.session["order"] = order
		# x=(request.session["order"])
		dictt = {BillName:int(totalprice)}
		Dicttt = dictt.items()

		order = request.session.get("order")
		cart = request.session.get("cart")

	
		data = Order(
			BillName = BillName,
			Address = delivery_address,
			Email = Email,
			CartPrice = CartPrice,
			Total = Total,
			Discount = Discount,
			Taxes = Taxes
			)

	
		data.save()
		# x=(request.session["order"])

		

		ProDuctName=[]
		
		ProductQuantity=list(cart.values())
		List = list(cart.keys())
		for n in List:
			data.product.add(n)
			data.save()
			ProDuctName.append(Product.objects.get(id=n))


		ProDuct = dict(zip(ProDuctName,ProductQuantity))
		PProduct = ProDuct.items()


		subject = 'Product Delivery Msg'
		message =  render_to_string('OrderEmail.html', {
			"Product" : PProduct,
			"totalprice" : totalprice,
			"OrderBy" : BillName,
			"Address": delivery_address
			})
		plain_message = strip_tags(message)
		# message = 'Thankyou for Buying Our Product your Product details :- Product - {}, OrderBy-{}, Price-{}, Address-{}'.format(ProDuct, BillName ,totalprice, delivery_address)
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [Email, ]
		send_mail( subject, plain_message, email_from, recipient_list )


		return redirect("/process-payment/?data_id=" + str(data.id))
		# return render(request, "checkout.html", {"totalprice":totalprice,"Dicttt":Dicttt})

	else:
		Total = request.GET.get("Total")
		discountsession = request.GET.get("discountsession")
		Taxes = request.GET.get("Taxes")
		totalprice = request.GET.get("totalprice")
		return render(request, "checkout.html", {"Total":Total,"discountsession":discountsession,
			"Taxes":Taxes,"totalprice":totalprice})



def wishlist(request):
	if request.method == "POST":
		# import pdb;pdb.set_trace()
		product_id = request.POST.get("product")

		productdata = Wish.objects.filter(product=product_id).count()
		if productdata > 0 :
			productdataa = Wish.objects.filter(product=product_id)
			delvar = productdataa.delete()
			product = Product.objects.all()
			wishdata = Wish.objects.all()
			datalist=[]
			for k in wishdata:
				datalist.append(int(k.product))
			return render(request,"index.html",{"datalist":datalist,"product":product,'media_url':settings.MEDIA_URL})
		else:
			data = Wish()
			data.product = product_id
			addvar = data.save()
			product = Product.objects.all()
			wishdata = Wish.objects.all()
			datalist=[]
			for k in wishdata:
				datalist.append(int(k.product))
			return render(request,"index.html",{"datalist":datalist,"product":product,'media_url':settings.MEDIA_URL})
	else:
		return redirect("/index/")


def wishlistdetails(request):
	# import pdb; pdb.set_trace()
	wishes = Wish.objects.all()
	List=[]
	for k in wishes:
		List.append(k.product)
	List2=[]
	if len(List)>0:
		for i in List:
			productFilter = Product.objects.filter(id=i)
			List2.append(productFilter[0])
		return render(request,"wishlist.html", {"wishes":List2,'media_url':settings.MEDIA_URL})
	else:
		return render(request,"wishlist.html",{"wishes":List2,'media_url':settings.MEDIA_URL})


def product_compare(request):
	import pdb;
	pdb.set_trace()
	productquery = Product.objects.all()
	List=[]
	for j in productquery:
		List.append(j)
	return render(request, "compare.html", {"productquery":List,'media_url':settings.MEDIA_URL})


from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import redirect
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

def process_payment(request):
	import pdb;
	pdb.set_trace()
	
	data_id = request.GET.get('data_id')
	order = request.session.get('order')
	get_order = request.GET.get('order')
	t = order.values()
	m = list(t)
	Amount = m[0]
	host = request.get_host()

	paypal_dict = {
		'business': settings.PAYPAL_RECEIVER_EMAIL,
		'amount': Amount,
		'item_name': 'NotSHown',
		'invoice': Amount,
		'currency_code': 'INR',
		'data_id':data_id,
		'notify_url': 'http://{}{}'.format(host,
										   reverse('paypal-ipn')),
		'return_url': 'http://{}{}'.format(host,
										   reverse('payment_done')),
		'cancel_return': 'http://{}{}'.format(host,
											  reverse('payment_cancelled',args=(), kwargs={'data_id': data_id})),
	}


	form = PayPalPaymentsForm(initial=paypal_dict)
	
	return render(request, 'process_payment.html', {'order': order, 'form': form})


@csrf_exempt
def payment_done(request):
	import pdb; pdb.set_trace()
	return render(request, 'paymentdone.html')


@csrf_exempt
def payment_canceled(request, data_id):
	import pdb; pdb.set_trace()
	order = Order.objects.get(id = data_id)
	print(order.status)
	order.status = 'CANCELLED'
	order.save()
	print(order.status)
	subject = 'Subject'
	html_message = render_to_string('cancel_order_mail.html', {'order': order})
	plain_message = strip_tags(html_message)
	from_email = 'gstshubhamb@gmail.com'
	to = (order.Email,)
	send_mail(subject, plain_message, from_email, to, html_message=html_message)
	return HttpResponse("Cancellation mail sent")

# def register(request):
	
#   if request.method == "POST":
		
#       form = UserForm(request.POST)
#       if form.is_valid():
#           # import pdb;
#           # pdb.set_trace()
#           first_name = request.POST.get('first_name')
#           last_name = request.POST.get('last_name')
#           username = request.POST.get('username')
#           email = request.POST.get('email')
#           UserField = request.POST.get('UserField')
#           password = request.POST.get("password")

#           user=User(
#               first_name = first_name,
#               last_name = last_name,
#               username = username,
#               email = email,
#               UserField = UserField,
#               )
#           user.set_password(password)
#           user.is_active = False
#           user.save()

#           current_site = get_current_site(request)
#           email_subject = 'Activate your blog account.'
#           message = render_to_string('activate_account.html', {
#               'user': user,
#               'domain': current_site.domain,
#               'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
#               'token':account_activation_token.make_token(user),
#               })

#           to_email = form.cleaned_data.get('email')
			
#           email = EmailMessage(email_subject, message, to=[to_email])
#           email.send()

#           return HttpResponse('Please confirm your email address to complete the registration')   
			
#   else:
#       form = UserForm()
#       return render(request,"UserRegistration.html", {"form":form})


# def loginn(request):

#   if request.method=='POST':
		
#       lform = LoginForm(request.POST)
#       if lform.is_valid():
#           username = request.POST.get('username')
#           password = request.POST.get('password')
#           user = authenticate(request, username=username, password=password)

#           if user.UserField == "student":
#               auth_login(request,user)
#               return redirect("register")
#           elif user.UserField == "teacher":
#               auth_login(request,user)
#               return redirect("index")
#           else:
#               return HttpResponse("galat hai")
#       else:
#           return HttpResponse("Login Data Sahi Nahi Hai")

#   else:
#       lform = LoginForm()
#       return render(request, 'login.html', {'lform': lform})



def register(request):
	
	if request.method == "POST":
		
		form = UserForm(request.POST)
		if form.is_valid():
			import pdb;
			pdb.set_trace()
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			username = request.POST.get('username')
			email = request.POST.get('email')
			UserField = request.POST.get('UserField')
			password = request.POST.get("password")
			Confirm_Password = request.POST.get("Confirm_Password")
			address = request.POST.get("address")
			contact_no = request.POST.get("contact_no")
			city = request.POST.get("city")
			state = request.POST.get("state")
			
			
			# line no 117 evam 118 isliye likhi h kyoki ek email se ek hi bar register hona chahiye.
			if User.objects.filter(email=email).exists():
				return HttpResponse("you have allready registered")
			else:
				user=User(
					first_name = first_name,
					last_name = last_name,
					username = username,
					email = email,
					UserField = UserField,
					address = address,
					contact_no = contact_no,
					city = city,
					state = state,
					)
				user.set_password(password)
				user.is_active = False
				user.save()

				current_site = get_current_site(request)
				email_subject = 'Activate your blog account.'
				message = render_to_string('activate_account.html', {
					'user': user,
					'domain': current_site.domain,
					'uid':urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
					})

				to_email = form.cleaned_data.get('email')
				
				email = EmailMessage(email_subject, message, to=[to_email])
				email.send()

				return HttpResponse('Please confirm your email address to complete the registration')   
			
	else:
		form = UserForm()
		return render(request,"UserRegistration.html", {"form":form})



def activate_account(request, uidb64, token):
	# import pdb;pdb.set_trace()
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if account_activation_token.check_token(user, token):

		user.is_active = True
		user.save()
		auth_login(request, user)
		# return redirect('home')
		return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
	else:
		return HttpResponse('Activation link is invalid!')


def loginn(request):

	if request.method=='POST':
		
		lform = LoginForm(request.POST)
		if lform.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)

			if user.UserField == "student":
				auth_login(request,user)
				var1 = User.objects.filter(username=username)
				product = Product.objects.all()
				return render(request,"index.html",{"var1":var1,"product":product,'media_url':settings.MEDIA_URL})
			elif user.UserField == "teacher":
				auth_login(request,user)
				var1 = User.objects.filter(username = username)
				product = Product.objects.all()
				
				#return redirect("/index/?var1=" + str(var1))
				return render(request,"index.html",{"var1":var1,"product":product,'media_url':settings.MEDIA_URL})
			else:
				return HttpResponse("galat hai")
		else:
			return HttpResponse("Login Data Sahi Nahi Hai")

	else:
		lform = LoginForm()
		return render(request, 'login.html', {'lform': lform})



from django.views.generic.base import TemplateView
class StripeView(TemplateView):
	template_name = 'stripe.html'

from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

@csrf_exempt
def stripe_config(request):
	if request.method == 'GET':
		stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
		return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
	import pdb;pdb.set_trace()

	if request.method == 'GET':
		domain_url = 'http://localhost:8000/'
		stripe.api_key = settings.STRIPE_SECRET_KEY
		try:
			# Create new Checkout Session for the order
			# Other optional params include:
			# [billing_address_collection] - to display billing address details on the page
			# [customer] - if you have an existing Stripe Customer ID
			# [payment_intent_data] - capture the payment later
			# [customer_email] - prefill the email input in the form
			# For full details see https://stripe.com/docs/api/checkout/sessions/create

			# ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
			checkout_session = stripe.checkout.Session.create(
				success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
				cancel_url=domain_url + 'cancelled/',
				payment_method_types=['card'],
				mode='payment',
				line_items=[
					{
						'name': 'T-shirt',
						'quantity': 1,
						'currency': 'usd',
						'amount': '20',
					}
				]
			)
			return JsonResponse({'sessionId': checkout_session['id']})
		except Exception as e:
			return JsonResponse({'error': str(e)})

class SuccessView(TemplateView):
	template_name = 'stripe_success.html'
class CancelledView(TemplateView):
	template_name = 'stripe_cancelled.html'




