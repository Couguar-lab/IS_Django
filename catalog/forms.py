from django import forms
from django.core.exceptions import ValidationError

from .models import Product

# Список запрещённых слов (константа для переиспользования)
BANNED_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def clean_name(self):
        """Валидация имени на запрещённые слова."""
        name = self.cleaned_data["name"].lower()
        for word in BANNED_WORDS:
            if word in name:
                raise ValidationError("Имя содержит запрещённое слово.")
        return self.cleaned_data["name"]

    def clean_description(self):
        """Валидация описания на запрещённые слова."""
        description = self.cleaned_data["description"].lower()
        for word in BANNED_WORDS:
            if word in description:
                raise ValidationError("Описание содержит запрещённое слово.")
        return self.cleaned_data["description"]

    def clean_price(self):
        """Кастомная валидация цены — не отрицательная."""
        price = self.cleaned_data["price"]
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация полей
        self.fields["name"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "rows": 5}
        )
        self.fields["image"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs.update({"class": "form-select"})
        self.fields["price"].widget.attrs.update({"class": "form-control"})

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            # Проверка формата
            if not image.name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise ValidationError("Допустимы только JPEG или PNG файлы.")
            # Проверка размера (5 МБ = 5 * 1024 * 1024 байт)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер файла не должен превышать 5 МБ.")
        return image
