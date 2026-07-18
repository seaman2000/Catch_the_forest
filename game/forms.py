from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer_name",
            "phone",
            "delivery_type",
            "delivery_details",
        ]

        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "placeholder": "Например: Георги Ангелов",
                    "class": "form-input",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Например: 0888123456",
                    "class": "form-input",
                    "inputmode": "tel",
                }
            ),
            "delivery_type": forms.Select(
                attrs={
                    "class": "form-input",
                    "id": "delivery-type",
                }
            ),
            "delivery_details": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Въведи адрес за доставка",
                    "class": "form-input",
                    "id": "delivery-details",
                }
            ),
        }

        labels = {
            "customer_name": "Име",
            "phone": "Телефон",
            "delivery_type": "Тип доставка",
            "delivery_details": "Адрес за доставка",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["delivery_details"].required = False

    def clean_customer_name(self):
        name = self.cleaned_data.get("customer_name", "").strip()

        if not name:
            raise forms.ValidationError("Името е задължително.")

        if len(name) < 3:
            raise forms.ValidationError(
                "Името трябва да бъде поне 3 символа."
            )

        return name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            raise forms.ValidationError(
                "Телефонът е задължителен."
            )

        normalized_phone = (
            phone.replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        if normalized_phone.startswith("+"):
            digits = normalized_phone[1:]
        else:
            digits = normalized_phone

        if not digits.isdigit():
            raise forms.ValidationError(
                "Телефонът трябва да съдържа само цифри."
            )

        if len(digits) < 9 or len(digits) > 15:
            raise forms.ValidationError(
                "Въведи валиден телефонен номер."
            )

        return normalized_phone

    def clean(self):
        cleaned_data = super().clean()

        delivery_type = cleaned_data.get("delivery_type")
        delivery_details = (
            cleaned_data.get("delivery_details") or ""
        ).strip()

        if delivery_type == "econt":
            econt_city_id = self.data.get(
                "econt_city_id",
                "",
            ).strip()

            econt_city_name = self.data.get(
                "econt_city_name",
                "",
            ).strip()

            econt_office_id = self.data.get(
                "econt_office_id",
                "",
            ).strip()

            econt_office_code = self.data.get(
                "econt_office_code",
                "",
            ).strip()

            econt_office_name = self.data.get(
                "econt_office_name",
                "",
            ).strip()

            econt_office_address = self.data.get(
                "econt_office_address",
                "",
            ).strip()

            if not econt_city_id or not econt_city_name:
                self.add_error(
                    None,
                    "Моля, избери населено място."
                )

            if not econt_office_code or not econt_office_name:
                self.add_error(
                    None,
                    "Моля, избери офис на Еконт."
                )

            if (
                econt_city_id
                and econt_city_name
                and econt_office_code
                and econt_office_name
            ):
                details_parts = [
                    f"Еконт: {econt_office_name}",
                    f"Град: {econt_city_name}",
                ]

                if econt_office_address:
                    details_parts.append(
                        f"Адрес: {econt_office_address}"
                    )

                details_parts.append(
                    f"Код на офис: {econt_office_code}"
                )

                if econt_office_id:
                    details_parts.append(
                        f"ID на офис: {econt_office_id}"
                    )


                cleaned_data["delivery_details"] = " | ".join(
                    details_parts
                )

        elif delivery_type == "address":
            if not delivery_details:
                self.add_error(
                    "delivery_details",
                    "Моля, въведи адрес за доставка."
                )

            elif len(delivery_details) < 10:
                self.add_error(
                    "delivery_details",
                    "Адресът трябва да е поне 10 символа."
                )

            else:
                cleaned_data["delivery_details"] = (
                    delivery_details
                )

        else:
            self.add_error(
                "delivery_type",
                "Моля, избери тип доставка."
            )

        return cleaned_data


class RegisterForm(UserCreationForm):
    class Meta:
        model = User

        fields = [
            "username",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Потребителско име",
                    "class": "form-input",
                }
            ),
        }

        labels = {
            "username": "Потребителско име",
            "password1": "Парола",
            "password2": "Потвърди паролата",
        }