from .models import Category,Products
from django import forms

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name','category','price','description','image','tag']


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name','category','price','description','image','tag']

