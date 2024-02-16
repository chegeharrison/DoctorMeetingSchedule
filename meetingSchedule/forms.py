from django import forms
from .models import Doctor, Meeting

class AddProfileForm(forms.ModelForm):
    doctor_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width : 17rem','placeholder':'Name'}), required=True, max_length=50)
    doctor_email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','style':'width : 17rem','placeholder':'Email Id'}), required=True, max_length=50)
    doctor_phone = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','style':'width : 17rem','placeholder':'Phone Number'}), required=True, max_length=10)
    doctor_image = forms.FileField(required=True)
    doctor_desc = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width : 17rem','placeholder':'Role'}), required=True, max_length=50)
    available = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width : 28rem','placeholder':'Monday - Friday'}), required=True, max_length=50)

    class Meta:
        model = Doctor
        fields = ['doctor_name', 'doctor_email', 'doctor_phone', 'doctor_image', 'doctor_desc', 'available']

# Meeting form
class MeetingForm(forms.ModelForm):
    visitor_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}), required=True, max_length=50)
    visitor_email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Id'}), required=True, max_length=50)
    visitor_phone = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Phone Number'}), required=True, max_length=10)
    
    class Meta:
        model = Meeting
        fields = ['visitor_name', 'visitor_email', 'visitor_phone']
