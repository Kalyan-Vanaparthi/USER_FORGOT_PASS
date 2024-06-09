
from django import forms
from app.models import *


class User_Form(forms.ModelForm):
    class Meta:
        model  = User
        #fields = "__all__"
        fields = ["username", "email", "password"]
        


class Profile_Form(forms.ModelForm):
    class Meta:
        model = Profile 
        #fields = "__all__"
        fields = ["address", "pic"]