from datetime import datetime
import re

from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse

def home(request):
    return render(request, "hello/home.html")

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")

def login(request):
    return render(request, "registration/login.html")

from django.contrib.auth.decorators import login_required

@login_required
def user_panel(request):
    return render(request, "hello/user_panel.html")

@login_required
def create_mask(request):
    return render(request, "hello/create_mask.html")

def hello_there(request, name):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )
    
print("http://127.0.0.1:8000/hello/friend")

# TUTAJ DO WGRYWANIA ZDJĘĆ DO BAZY PRZEZ UŻYTKOWNIKA!!!!!!!!
from django.shortcuts import redirect
from .forms import ImageUploadForm

# obsługa formularza z wczytywaniem plików

@login_required
def upload_image(request):
    if request.method == 'POST': # POST oznacza, że użytkownik kliknął przycisk i przesyła dane na serwer
        form = ImageUploadForm(request.POST, request.FILES)
        # request.FILES to specjalny obiekt, który zawiera wszystkie pliki przesłane przez użytkownika.
        # request.POST zawiera dane z formularza, takie jak tytuł zdjęcia, a request.FILES zawiera przesłany plik obrazu.
        
        if form.is_valid(): # czy dane są ok?
            form.save()
            return redirect('user_panel') # przeskakuje na user panel
        else:
            print(form.errors) # jeśli dane nie są ok, to wyświetla błędy walidacji w konsoli
    
    else: # GET oznacza, że uzytkownik dopiero wszedł na stronę, django tworzy pusty formularz i sysyła go do szablonu
        form = ImageUploadForm()
        
    # render to składanie get i post w jedno, czyli jeśli jest post to przetwarzamy dane, a jeśli get to tworzymy pusty formularz i wysyłamy go do szablonu
    # składanie gotowej strony z kawałków kodu
    
    # reguest - czy użytkownik jest zalogowany, czy nie, jakie ma uprawnienia, itp.
    # 'hello/upload_image.html' - szablon, który ma być użyty do renderowania strony
    # {'form': form} - słownik, który zawiera dane, które mają być przekazane do szablonu. W tym przypadku przekazujemy obiekt form, który może być użyty w szablonie do wyświetlenia formularza i obsługi błędów walidacji.
    
    # silnik szuka miejsc oznaczonych jako {{ form }} w szablonie upload_image.html i tam wstawia kod HTML wygenerowany przez formę, który zawiera pola formularza i ewentualne komunikaty o błędach.  
    
    return render(request, 'hello/upload_image.html', {'form': form})


# POBIERAM ZDJĘCIA Z BAZY DANYCH I WYSWIETLAM JE!!!!!!!!
from .models import Mask, UserImage

import base64

@login_required
def select_image_for_binary_mask(request):
    images = UserImage.objects.all() # wszystkie zdjęcia z bazy danych, które są przechowywane w modelu UserImage (czyli w tabeli UserImage w bazie danych)
    return render(request, "hello/select_image_for_binary_mask.html", {'images': images})

# TUTAJ WIDOK DO TWORZENIA MASKI NA PODSTAWIE WYBRANEGO ZDJĘCIA, ALE TO JEST W SZABLONIE, BO TAM JEST JS, A NIE PYTHON
@login_required
def create_binary_mask(request, image_id):
    image = UserImage.objects.get(id=image_id) # wybrane zdjęcie z bazy danych, które ma być użyte do tworzenia maski, image_id to parametr przekazywany w URL, który identyfikuje konkretne zdjęcie w bazie danych
    
    return render(request, "hello/create_binary_mask.html", {
        'image_url': image.image.url,
        'image_id': image_id
    })
    
import re
from django.core.files.base import ContentFile
    
@login_required
def save_mask(request, image_id):
    if request.method == 'POST':
        # wyciągam tekst w formacie base64 z danych przesłanych przez użytkownika (mask_base64)
        mask_base64 = request.POST.get('mask_base64')
        
        # usuwam prefiks base64, który jest dodawany do danych obrazu, aby uzyskać czyste dane binarne maski
        mask_data = re.sub('^data:image/.+;base64,', '', mask_base64)
        
        # zamiana base64 na dane binarne do obrazka png
        mask_binary = base64.b64decode(mask_data)
        
        file_name = f"mask_{image_id}_{request.user.id}.png"
        mask_file = ContentFile(mask_binary, name=file_name)
            
        # wyświetl błąd w razie problemów z dekodowaniem
        original_image = get_object_or_404(UserImage, id=image_id)

        # nowy wiersz w tabeli hello_mask z nazwą maski - w bazie jest tylko ścieżka do tego pliku
        new_mask = Mask.objects.create(
            image=mask_file,
        )
            
        return redirect('user_panel')