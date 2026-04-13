from django.contrib import admin

# Register your models here.


# TO JEST DO ZDJĘĆ W BAZIE DANYCH!!!!!
# klasa opisuje moje zdjęcie w bazie
# klasa UserImage jest modelem, który reprezentuje strukturę danych dla przechowywania informacji o zdjęciach w bazie danych. 
# Zawiera trzy pola: title (tytuł zdjęcia), image (plik obrazu) oraz uploaded_at (data i czas przesłania zdjęcia). 
# Metoda __str__ zwraca tytuł zdjęcia jako reprezentację tekstową obiektu.
from .models import UserImage

admin.site.register(UserImage)