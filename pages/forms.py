from django.forms import ModelForm
from pages.models import User


class User_Profile_Form(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','address','unit_number','postal_code']
