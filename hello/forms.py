from django import forms
from .models import UserImage

# kod mówi django, jakie pola z modelu UserImage (czyli title i image) mają być wyświetlane w formularzu, który będzie używany do przesyłania zdjęć przez użytkowników.
# UserImage to klasa z biblioteki models (zaimplementowana w models.py)
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['title', 'image'] # to dla użytkownika do wypełnienia
        