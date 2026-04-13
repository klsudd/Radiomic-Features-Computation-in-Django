from datetime import datetime
import re

from django.shortcuts import render

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