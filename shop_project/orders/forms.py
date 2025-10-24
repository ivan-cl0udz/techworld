from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name',
            'email',
            'address_line1',  # ✅ correct field name
            'address_line2',  # ✅ correct field name
            'city',
            'postal_code',
            'country',
            'phone',
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ім’я та прізвище'}),
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Електрона пошта'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Вулиця, будинок'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Квартира, поверх (необов’язково)'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Місто'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Поштовий індекс'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Країна'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Номер телефону'}),
        }

