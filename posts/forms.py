from django import forms
from .models import Product


class ProductCreateForm(forms.Form):
    image = forms.FileField(required=False)
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea())
    price = forms.FloatField()

class ReviewCreateForm(forms.Form):
    text = forms.CharField(max_length=255)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False)