# Create your models here.
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES =( 
	("student", "student"), 
	("teacher", "teacher"),
)

class User(AbstractUser):
	UserField = models.CharField(max_length=20,choices = CHOICES ,blank=False)
	address = models.CharField(max_length = 50 , blank=False)
	contact_no = models.BigIntegerField(null=True)
	city = models.CharField(max_length=25, blank=False)
	state = models.CharField(max_length=25 ,blank=False)

class Product(models.Model):
	name = models.CharField(max_length=50)
	price = models.IntegerField()
	image = models.FileField()
	def __str__(self):
		return self.name
STATUS = (
		("PROCESS", 'Process'),
		("PENDING", 'Pending'),
		("SHIPPED", 'Shipped'),
		("CANCELLED","Cancelled"),
	)	
class Order(models.Model):
	product = models.ManyToManyField(Product)
	order_date = models.DateTimeField(auto_now_add = True)
	BillName = models.CharField(max_length = 100)
	Address = models.CharField(max_length = 200)
	Email  = models.EmailField(max_length=100)
	CartPrice = models.CharField(max_length=10)
	Discount = models.CharField(max_length=10, default="")
	Total = models.CharField(max_length=10, default="")
	Taxes = models.CharField(max_length=10, default="")
	
	status = models.CharField(max_length=20, choices=STATUS, default="PENDING")
	def __str__(self):
		return self.BillName


class Promo_codes(models.Model):
	code = models.CharField(max_length=6)
	value = models.IntegerField()

	def __str__(self):
		return self.code


wish_CHOICES =( 
	("wish", "wish"), 
	("unwished", "unwished"),
)

class Wish(models.Model):
	product = models.CharField(max_length=100)

	wish = models.CharField(choices=wish_CHOICES, default='unwished',max_length=10)
	def __str__(self):
		return self.product