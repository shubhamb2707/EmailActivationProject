from django import forms
from .models import User
from django.forms import ModelForm

CHOICES =( 
    ("student", "student"), 
    ("teacher", "teacher"),
)

class UserForm(forms.Form):
	username = forms.CharField(
		required = True,
		label = 'Username',
		max_length = 32
	)
	
	email = forms.CharField(
		required = True,
		label = 'Email',
		max_length = 32,
		widget = forms.EmailInput()
	)
	
	first_name = forms.CharField(
		required = True,
		label = 'First_name',
		max_length = 32
	)
	
	last_name = forms.CharField(
		required = True,
		label = 'Last_name',
		max_length = 32
	)
	
	UserField = forms.ChoiceField(
		label= "UserField",
		choices = CHOICES,
		widget = forms.Select()
		)

	address = forms.CharField(
		required = True,
		label = 'Address',
		max_length = 50
	) 

	contact_no = forms.IntegerField(
		required = True,
		label = 'Contact_No',
	)

	city = forms.CharField(
		required = True,
		label = 'City',
		max_length = 25
	)

	state = forms.CharField(
		required = True,
		label = 'State',
		max_length = 25
	)
	
	

	def __init__(self, *args, **kwargs):

		super(UserForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control'})


	# def clean(self):
	# 	super(UserForm, self).clean()
	# 	password = self.cleaned_data.get("password")
	# 	Confirm_Password = self.cleaned_data.get("Confirm_Password")

	# 	if password != Confirm_Password:
	# 		self._errors["Confirm_Password"] = self.error_class([
	# 			"password and confirm_password does not match"])
	
	


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)




# here now we are doing admin action customization
