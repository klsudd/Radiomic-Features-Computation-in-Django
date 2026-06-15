from datetime import datetime
import re

from django.shortcuts import get_object_or_404, render
from django.contrib import messages

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
            messages.success(request, "The image has been successfully added to the database.")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'csrfmiddlewaretoken' in request.POST:
                return JsonResponse({'success': True, 'message': 'Image uploaded successfully'})
            else:
                return redirect('user_panel') # przeskakuje na user panel
        else:
            print(form.errors) # jeśli dane nie są ok, to wyświetla błędy walidacji w konsoli
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'csrfmiddlewaretoken' in request.POST:
                return JsonResponse({'success': False, 'error': str(form.errors)}, status=400)
    
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
from .models import UserMask, UserImage

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
    
    
    
    
def run_pyradiomics(image_path,
                    mask_path):
    img_pil = Image.open(image_path).convert('L')  # Konwersja do odcieni szarości
    img_array = np.array(img_pil)
    
    mask_pil = Image.open(mask_path).convert('L')  # Konwersja do odcieni szarości
    mask_array = np.array(mask_pil)
    
    binary_mask_array = (mask_array > 0).astype(np.uint8)  # Konwersja do maski binarnej (0 i 1)
    
    img_sitk = sitk.GetImageFromArray(img_array)
    mask_sitk = sitk.GetImageFromArray(binary_mask_array)
    
    mask_sitk.CopyInformation(img_sitk)  # Upewnij się, że maska ma te same informacje przestrzenne co obraz

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # USTAWIENIA EKSTRAKTORA CECH POD OBRAZU 2D PNG LUB JPG
    settings = {
        'force2D': True,  # Wymuszanie analizy 2D
        'resampledPixelSpacing': None,  # Brak resamplingu
        'force2Ddimension': 0,  # Analiza wzdłuż osi Z (dla obrazów 3D)
    }
    extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # OBLICZENIA NA BIBLIOTECE PYRADIOMICS
    features = extractor.execute(img_sitk, mask_sitk)
    
    clean_features = {}
    for key, value in features.items():
        if isinstance(value, (int, float, str)):
            clean_features[key] = value
        else:
            clean_features[key] = str(value)
    
    return clean_features
 
    
    
    
    
# @login_required
# def save_mask(request, image_id):
#     if request.method == 'POST':
#         # wyciągam tekst w formacie base64 z danych przesłanych przez użytkownika (mask_base64)
#         mask_base64 = request.POST.get('mask_base64')
        
#         # usuwam prefiks base64, który jest dodawany do danych obrazu, aby uzyskać czyste dane binarne maski
#         mask_data = re.sub('^data:image/.+;base64,', '', mask_base64)
        
#         # zamiana base64 na dane binarne do obrazka png
#         mask_binary = base64.b64decode(mask_data)
        
#         file_name = f"mask_{image_id}_{request.user.id}.png"
#         mask_file = ContentFile(mask_binary, name=file_name)
            
#         # wyświetl błąd w razie problemów z dekodowaniem
#         original_image = get_object_or_404(UserImage, id=image_id)

#         # nowy wiersz w tabeli hello_mask z nazwą maski - w bazie jest tylko ścieżka do tego pliku
#         new_mask = UserMask.objects.create(
#             image=mask_file,
#             user_image=original_image
#         )
#         messages.success(request, "The mask has been successfully uploaded to the database.")
            
#         return redirect('user_panel')
    
# from django.shortcuts import render, get_object_or_404
# from .models import UserImage

# def create_binary_mask_view(request, image_id):  # Django automatycznie przekaże tu '6'
#     # Pobieramy obrazek z bazy, żeby wyświetlić go użytkownikowi do rysowania
#     obrazek = get_object_or_404(UserImage, id=image_id)
    
#     # Przekazujemy 'image_id' oraz cały obiekt 'obrazek' do pliku HTML
#     return render(request, 'create_binary_mask.html', {
#         'image_id': image_id, 
#         'obrazek': obrazek
#     })
    
    
    
    
from django.http import JsonResponse
from .models import UserImage, UserMask


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# PYRADIOMICS LIBRARY
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import SimpleITK as sitk
import numpy as np

from PIL import Image

from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import UserMask, UserImage, RadiomicsResult

from radiomics import featureextractor


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WIDOK DO ZAPISYWANIA MASKI I WYNIKÓW RADIOMICS DO BAZY DANYCH
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@login_required
def save_mask(request, image_id):
    
    img_original = get_object_or_404(UserImage, id=image_id)
    
    if request.method == 'POST':
        # Odbieramy przesłane dane z JavaScriptu
        user_image_id = request.POST.get('user_image_id')
        
        # mask_file = request.FILES.get('image')
        image_data_base64 = request.POST.get('mask_base64')
        
        mask_name = request.POST.get('name') or f"Mask for Image {user_image_id}"
        
        # odkodowanie base64 do binarnego pliku obrazu
        format, imgstr = image_data_base64.split(';base64,')
        ext = format.split('/')[-1]
        
        mask_file = ContentFile(base64.b64decode(imgstr), name=f"mask_{user_image_id}.{ext}")

        # zapisanie maski do bazy danych i powiązanie jej z odpowiednim obrazkiem
        new_mask = UserMask(
            name=mask_name,
            image=mask_file,
            user_image=img_original  # <--- Przypisanie klucza obcego!
        )
        new_mask.save()
        
        messages.success(request, "The mask has been successfully uploaded to the database.")

        try:
            path_to_image = img_original.image.path
            path_to_mask = new_mask.image.path
            
            # uruchomienie funkcji run_pyradiomics
            features = run_pyradiomics(path_to_image, path_to_mask)
            
            results_db = RadiomicsResult(
                user_mask=new_mask,
                features=features
            )
            results_db.save()
        
        except Exception as e:
            print(f"Error during radiomics feature extraction: {e}")
            return HttpResponse(f"Mask was saved, but the radiomic calculations failed: {e}", status=500)
        
        return redirect('user_panel')  # Przekierowanie do panelu użytkownika po zapisaniu maski i wyników radiomics

    return JsonResponse({'status': 'error', 'message': 'Invalid request type.'}, status=400)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WIDOK DO WYBIERANIA MASKI Z WYNIKAMI RADIOMICS
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@login_required
def view_radiomics_results(request):
    masks = UserMask.objects.filter(radiomics_result__isnull=False).select_related('user_image')
    return render(request, "hello/select_mask_for_radiomics.html", {
        'masks': masks
    })

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WIDOK DO WYŚWIETLANIA WYNIKÓW RADIOMICS DLA KONKRETNEJ MASKI
# SORTOWANIE PO TEKŚCIE, LICZBIE
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@login_required
def view_radiomics_result(request, mask_id):
    mask = get_object_or_404(UserMask, id=mask_id)
    
    try:
        radiomics_result = mask.radiomics_result
    except RadiomicsResult.DoesNotExist:
        return HttpResponse("No radiomics results found for this mask.", status=404)
    
    features = []
    for key, value in radiomics_result.features.items():
        if key.startswith('diagnostics_') or 'diagnostics' in key:
            category = 'diagnostic'
        elif 'shape2D' in key or 'shape_2d' in key or 'shape' in key:
            category = 'shape_2d'
        elif 'firstorder' in key or 'first_order' in key:
            category = 'first_order'
        elif 'glcm' in key:
            category = 'glcm'
        elif 'glrlm' in key:
            category = 'glrlm'
        elif 'other' in key:
            category = 'other'
        else:
            category = 'other'

        numeric_value = None
        if isinstance(value, (int, float)):
            numeric_value = float(value)
        elif isinstance(value, str):
            try:
                numeric_value = float(value)
            except ValueError:
                numeric_value = None

        features.append({
            'feature_name': key,
            'feature_value': value,
            'feature_value_numeric': numeric_value,
            'category': category
        })

    search_text = request.GET.get('search_text', '').strip()
    min_value = request.GET.get('min_value', '').strip()
    per_page = request.GET.get('per_page', '10')
    page_number = request.GET.get('page', '1')

    if search_text:
        features = [
            f for f in features
            if search_text.lower() in f['feature_name'].lower()
        ]

    if min_value:
        try:
            min_val_float = float(min_value)
            features = [
                f for f in features
                if f['feature_value_numeric'] is not None and f['feature_value_numeric'] >= min_val_float
            ]
        except ValueError:
            min_value = ''

    try:
        per_page = int(per_page)
    except (ValueError, TypeError):
        per_page = 10

    if per_page <= 0:
        per_page = 10
    if per_page > 100:
        per_page = 100

    paginator = Paginator(features, per_page)
    page_obj = paginator.get_page(page_number)

    return render(request, "hello/view_radiomics_result.html", {
        'mask': mask,
        'radiomics_result': radiomics_result,
        'features': page_obj,
        'page_obj': page_obj,
        'search_text': search_text,
        'min_value': min_value,
        'per_page': per_page,
    })


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WIDOK GO GENEROWANIA HISTOGRAMU INTENSYWNOŚCI FIRST ORDER
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Użycie backendu, który nie wymaga wyświetlania okien
import io
import numpy as np

from .models import UserMask, RadiomicsResult

@login_required
def view_intensity_histogram(request, mask_id):
    mask = get_object_or_404(UserMask, id = mask_id)
    image = mask.user_image
    
    img_array = np.array(Image.open(image.image.path).convert('L'))
    mask_array = np.array(Image.open(mask.image.path).convert('L'))
    
    masked_pixels = img_array[mask_array > 128]
    
    
    fig, ax = plt.subplots(figsize = (7, 4))
    ax.hist(masked_pixels, bins = 32, range = (0, 256), color = "#1E55BC", edgecolor = 'black', alpha = 0.8)
    
    ax.set_title(f"Pixel intensity distribution - {mask.name}")
    ax.set_xlabel("Pixel value (0 - 255)")
    ax.set_ylabel("Number of pixels")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()

    # zapisywanie do ramu
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig)

    # zwrócenie obrazka do przeglądarki
    return HttpResponse(buf, content_type='image/png')


@login_required
def bar_plot(request, mask_id):
    mask = get_object_or_404(UserMask, id=mask_id)
    return render(request, 'hello/bar_plot.html', {
        'mask': mask
    })
    

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# PAGINACJA I RESZTA BAJERÓW
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from django.core.paginator import Paginator

from .models import RadiomicsResult

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RadiomicsResult

@login_required
def view_radiomics_detail(request, mask_id):
    result = get_object_or_404(RadiomicsResult, user_mask_id=mask_id)
    
    features_list = []
    for key, val in result.features.items():
        features_list.append({
            'name': key,
            'value': float(val) if isinstance(val, (int, float)) else val
        })

    search_text = request.GET.get('search_text', '')
    min_value = request.GET.get('min_value', '')
    per_page = request.GET.get('per_page', '10')
    page_number = request.GET.get('page', '1')

    if search_text:
        features_list = [f for f in features_list if search_text.lower() in f['name'].lower()]
    
    if min_value:
        try:
            min_val_float = float(min_value)
            features_list = [
                f for f in features_list 
                if isinstance(f['value'], (int, float)) and f['value'] >= min_val_float
            ]
        except ValueError:
            pass

    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10

    paginator = Paginator(features_list, per_page)
    page_obj = paginator.get_page(page_number)

    return render(request, 'hello/radiomics_detail.html', {
        'page_obj': page_obj,
        'wynik': result,
        'search_text': search_text,
        'min_value': min_value,
        'per_page': per_page,
    })