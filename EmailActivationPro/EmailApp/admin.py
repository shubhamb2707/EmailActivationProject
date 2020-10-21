from django.contrib import admin
from .models import User, Product , Order, Promo_codes, Wish
admin.site.register(User)
admin.site.register(Product)

admin.site.register(Promo_codes)
admin.site.register(Wish)


from django.urls import reverse
from django.contrib import admin
from django.urls import path
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from .models import *
from django.shortcuts import render

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	# change_form_template = "changeform.html"
	list_display = ("BillName", "status", "account_actions")
	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path(
				'<int:cart_id>/invoice',
				self.admin_site.admin_view(self.invoice),
				name='send_invoice',
			),
			path(
				'<int:cart_id>/shipping',
				self.admin_site.admin_view(self.shipping),
				name='shipping',
			),
			
		]
		return custom_urls + urls



	def shipping(self,request,cart_id):
		# import pdb;pdb.set_trace()
		
		order = Order.objects.get(id = cart_id)
		print(order.status)
		order.status = 'SHIPPED'
		order.save()
		print(order.status)

		subject = 'order confirmed'
		html_message = render_to_string('shipping_mail.html', {'order': order})
		plain_message = strip_tags(html_message)
		from_email = 'gstanupamt@gmail.com'
		to = ('shubhamkbillore@gmail.com',)

		send_mail(subject, plain_message, from_email, to, html_message=html_message)

		return HttpResponse("Shipping order sent")
		

	def invoice(self,request,cart_id):
		# import pdb;pdb.set_trace()
		
		order = Order.objects.get(id = cart_id)
		print(order.status)
		order.status = 'PROCESS'
		order.save()
		print(order.status)

		subject = 'Subject'
		html_message = render_to_string('Invoice_mail.html', {'order': order})
		plain_message = strip_tags(html_message)
		from_email = 'gstshubhamb@gmail.com'
		to = ('shubhamkbillore@gmail.com',)

		send_mail(subject, plain_message, from_email, to, html_message=html_message)

		
		return HttpResponse("Invoice detail sent")

 

	def account_actions(self, obj):
		return format_html(
			'<a class="button" style = "padding:6px; background-color: green;" href="{}">Send Invoice</a>&nbsp;'
			'<a class="button" style = "padding:6px; background-color: green; margin:10px;" href="{}">Shipping</a>',
			reverse('admin:send_invoice',args = [obj.id] ),
			reverse('admin:shipping',args =  [obj.id] ),
			
		)
	account_actions.short_description = 'Account Actions'
	account_actions.allow_tags = True
# admin.site.register(Order)
