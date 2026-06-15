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
class UserMask(models.Model):
    name = models.CharField(max_length=100, verbose_name="Mask Name")
    image = models.ImageField(upload_to='masks/', verbose_name="Mask Image")
    created_at = models.DateTimeField(auto_now_add=True)

    user_image = models.ForeignKey(
        UserImage,
        on_delete=models.CASCADE,
        related_name='masks', # pozwala na łatwy dostęp do masek związanych z danym zdjęciem (np. image.masks.all() zwróci wszystkie maski związane z tym zdjęciem)
        verbose_name="Related User Image",
        null = True,  # pozwala na przechowywanie masek bez przypisanego zdjęcia
        blank = True  # pozwala na pozostawienie tego pola pustym w formularzach admina
    )
    
    # class Meta:
    #     db_table = 'hello_mask'  # nazwa tabeli w bazie danych

    def __str__(self):
        return self.name
    
class RadiomicsResult(models.Model):
    user_mask = models.OneToOneField(
        UserMask,
        on_delete=models.CASCADE,
        related_name='radiomics_result',
        verbose_name="Related User Mask"
    )
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    features = models.JSONField() # przechowuje wyniki obliczeń radiomicznych w formacie JSON, co pozwala na elastyczne przechowywanie różnych cech i ich wartości bez konieczności definiowania osobnych kolumn dla każdej cechy.
    
    class Meta:
        db_table = 'hello_radiomics_result'  # nazwa tabeli w bazie danych
    
    def __str__(self):
        return f"Radiomics Result for Mask: {self.user_mask.name}"
    

