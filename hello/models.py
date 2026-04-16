from django.db import models

# Create your models here.

# TO JEST DO ZDJĘĆ W BAZIE DANYCH!!!!!
# klasa opisuje moje zdjęcie w bazie
class UserImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Image Title")
    image = models.ImageField(upload_to='images/', verbose_name="Image File")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
# TO JEST DO MASKI!!!!!!!
# jak ma wyglądać tabela w bazie danych
# etykiety pojawiają się w panelu administratora django
class Mask(models.Model):
    name = models.CharField(max_length=100, verbose_name="Mask Name")
    image = models.ImageField(upload_to='masks/', verbose_name="Mask Image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
