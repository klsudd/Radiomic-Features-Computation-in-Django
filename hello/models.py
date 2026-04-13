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
