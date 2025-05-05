from django import forms

from .models import Reference
from .models import Staff
from .models import Cost_Model
from .models import Book_model
from .models import Output,Job
from .models import Purchase,Staff_payments
from django.core.exceptions import ValidationError


class OrderForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book_model.objects.all(), label="Kitobni tanlang")
    quantity = forms.IntegerField(min_value=1, label="Soni")


class referenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ['name', 'value']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomi kiriting...',
                'style': 'border: 2px solid #007bff; border-radius: 8px;'
            }),
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Qiymatini kiriting...',
                'style': 'border: 2px solid #007bff; border-radius: 8px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(referenceForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ''



class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            "full_name",
            "birthday",
            "gender",
            "phone_number",
            "experience",
            "hired_date",
            "hourly_rate",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ism va familiya"}), 
            "birthday": forms.DateInput(attrs={"class": "form-control", "type": "date"}), 
            "gender": forms.Select(attrs={"class": "form-control"}),  
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998901234567"}), 
            "experience": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Necha yil tajriba?"}), 
            "hired_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}), 
            "hourly_rate": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Soatlik maosh (UZS)"}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.fields['gender'].queryset = Reference.objects.filter(name="Jinsi")  




class CostModelForm(forms.ModelForm):
    class Meta:
        model = Cost_Model
        exclude = ['is_deleted']
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={  # << o'zgardi
                'class': 'form-control form-control-lg',
                'placeholder': 'Chiqim nomini kiriting'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-control-lg',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Narxni kiriting'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Sonni kiriting'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Chiqim haqida maʼlumot yozing',
                'rows': 4
            }),
            'creat_at': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date',
            }),
        }

        labels = {
            'name': 'Chiqim nomi',
            'category': 'Chiqim kategoriyasi',
            'price': 'Chiqim narxi',
            'quantity': 'Chiqim soni',
            'image': 'Chiqim rasmi',
            'description': 'Chiqim haqida',
            'creat_at': 'Chiqim sanasi',
        }

      






class BookForm(forms.ModelForm):
    class Meta:
        model = Book_model
        fields = ['name', 'category', 'price', 'quantity', 'image', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kitob nomi'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kitob narxi'}),
            'quantity': forms.HiddenInput(),  # Quantity maydonini yashirish
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Kitob haqida', 'rows': 4}),
        }

    
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Agar yangi rasm yuklangan bo‘lsa, eski rasmni o‘chirib tashlash
        if self.cleaned_data.get('image'):
            if instance.pk:
                old_instance = Book_model.objects.get(pk=instance.pk)
                if old_instance.image and old_instance.image != instance.image:
                    old_instance.image.delete(save=False)  # Eski rasmni o‘chirish
        
        if commit:
            instance.save()
        return instance

        
class OutputForm(forms.ModelForm):
    class Meta:
        model = Output
        fields = ['name', 'deckripton', 'price']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'deckripton': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Output nomi',
            'deckripton': 'Tavsif',
            'price': 'Narxi',
        }
        

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['book', 'buyer_name', 'quantity']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'buyer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Xaridor ismi'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Soni'}),
        }

    def save(self, commit=True):
        # Xaridni saqlashdan oldin umumiy narxni hisoblash
        instance = super().save(commit=False)
        
        # Umumiy narxni hisoblash
        instance.total_price = instance.book.price * instance.quantity
        
        # Kitobning mavjud miqdorini kamaytirish
        if instance.book.quantity < instance.quantity:
            raise ValidationError("Yetarli miqdorda kitob mavjud emas!")
        
        # Kitobning miqdorini yangilash
        instance.book.quantity -= instance.quantity
        instance.book.save()

        if commit:
            instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.fields['book'].queryset = Book_model.objects.filter(is_deleted=False)

        
        
class staff_paymentForm(forms.ModelForm):
    class Meta:
        model = Staff_payments
        fields = ['staff', 'price']
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'To‘lov summasi'}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['staff', 'hourly_rate', 'hired_date']
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Soatlik stavka'}),
            'hired_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }