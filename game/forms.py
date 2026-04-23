from django import forms
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "phone", "delivery_type", "delivery_details"]
        widgets = {
            "customer_name": forms.TextInput(attrs={
                "placeholder": "Например: Георги Ангелов",
                "class": "form-input",
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "Например: 0888123456",
                "class": "form-input",
            }),
            "delivery_type": forms.Select(attrs={
                "class": "form-input",
                "id": "delivery-type",
            }),
            "delivery_details": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Въведи данни за доставка",
                "class": "form-input",
                "id": "delivery-details",
            }),
        }
        labels = {
            "customer_name": "Име",
            "phone": "Телефон",
            "delivery_type": "Тип доставка",
            "delivery_details": "Детайли за доставка",
        }

    def clean_customer_name(self):
        name = self.cleaned_data["customer_name"].strip()
        if not name:
            raise forms.ValidationError("Името е задължително.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not phone:
            raise forms.ValidationError("Телефонът е задължителен.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        delivery_type = cleaned_data.get("delivery_type")
        delivery_details = (cleaned_data.get("delivery_details") or "").strip()

        if delivery_type == "econt" and not delivery_details:
            self.add_error("delivery_details", "Моля, въведи офис на Еконт.")
        elif delivery_type == "address" and len(delivery_details) < 10:
            self.add_error("delivery_details", "Адресът трябва да е поне 10 символа.")

        return cleaned_data


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Потребителско име",
                "class": "form-input",
            }),
        }

        labels = {
            "username": "Потребителско име",
            "password1": "Парола",
            "password2": "Потвърди паролата",
        }