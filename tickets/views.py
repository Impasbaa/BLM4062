from django.shortcuts import render
from django.shortcuts import redirect
from .models import Trip, Ticket, City
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def turkce(sehir):
    cevir = {
        ord('ç'): 'c~', ord('ğ'): 'g~', ord('ı'): 'h~',
        ord('ö'): 'o~', ord('ş'): 's~', ord('ü'): 'u~',
        ord('Ç'): 'C~', ord('Ğ'): 'G~', ord('İ'): 'I~',
        ord('Ö'): 'O~', ord('Ş'): 'S~', ord('Ü'): 'U~'
    }
    return sehir.name.translate(cevir)

def home_view(request):
    # Veritabanındaki tüm şehirleri çekiyoruz
    sehirler = City.objects.all()
    # Çektiğimiz şehirleri yukarıdaki fonksiyona göre sıralıyoruz
    sirali_sehirler = sorted(sehirler, key=turkce)
    # Şehirleri 'context' adında bir paketle HTML'e gönderiyoruz
    context = {
        'sehirler': sirali_sehirler,
        'bugun': date.today()
    }
    return render(request, 'index.html', context)

def search_view(request):
    kalkis_id = request.GET.get('nereden')
    varis_id = request.GET.get('nereye')
    secilen_tarih = request.GET.get('tarih')

    seferler = Trip.objects.filter(
        departure_city_id=kalkis_id, 
        arrival_city_id=varis_id
    )

    kalkis_sehir = City.objects.get(id=kalkis_id) if kalkis_id else None
    varis_sehir = City.objects.get(id=varis_id) if varis_id else None

    if secilen_tarih and secilen_tarih != "":
        seferler = seferler.filter(departure_time__date=secilen_tarih)

    seferler = seferler.order_by('departure_time')

    context = {
        'seferler': seferler,
        'secilen_tarih': secilen_tarih,
        'kalkis_sehir': kalkis_sehir,
        'varis_sehir': varis_sehir,
    }
    return render(request, 'sefer_listesi.html', context)

def koltuk_secimi_view(request, sefer_id):
    sefer = Trip.objects.get(id=sefer_id)
    # Sefere ait satılmış biletlerin koltuk numaralarını bir listeye alıyoruz
    satilan_biletler = Ticket.objects.filter(trip=sefer, status='aktif')
    erkek_koltuklar = [bilet.seat_number for bilet in satilan_biletler if bilet.passenger_gender == 'E']
    kadin_koltuklar = [bilet.seat_number for bilet in satilan_biletler if bilet.passenger_gender == 'K']
    
    koltuk_matrisi = []
    kapasite = sefer.bus.capacity
    tip = sefer.bus.bus_type
    koltuk_no = 1

    if tip == '2+2':
        # 2+2 Düzeni: Son satır 5 koltuk, diğerleri 4 koltuk
        normal_koltuk_sayisi = kapasite - 5 
        
        while koltuk_no <= normal_koltuk_sayisi:
            koltuk_matrisi.append([koltuk_no, koltuk_no+1, None, koltuk_no+2, koltuk_no+3])
            koltuk_no += 4
            
        # En Arka Satır: Koridor boşluğu yok, 5 koltuk bitişik
        son_satir = []
        for _ in range(5):
            if koltuk_no <= kapasite:
                son_satir.append(koltuk_no)
                koltuk_no += 1
        koltuk_matrisi.append(son_satir)

    elif tip == '2+1':
        # 2+1 Düzeni: Son satır 4 koltuk, diğerleri 3 koltuk
        normal_koltuk_sayisi = kapasite - 4
        
        while koltuk_no <= normal_koltuk_sayisi:
            koltuk_matrisi.append([koltuk_no, None, koltuk_no+1, koltuk_no+2])
            koltuk_no += 3
            
        # En Arka Satır: Koridor boşluğu yok, 4 koltuk bitişik
        son_satir = []
        for _ in range(4):
            if koltuk_no <= kapasite:
                son_satir.append(koltuk_no)
                koltuk_no += 1
        koltuk_matrisi.append(son_satir)
    
    context = {
        'sefer': sefer,
        'koltuk_matrisi': koltuk_matrisi,
        'erkek_koltuklar': erkek_koltuklar,
        'kadin_koltuklar': kadin_koltuklar,
    }
    return render(request, 'koltuk_secimi.html', context)

# @login_required(login_url='/login/')
def odeme_view(request, sefer_id):
    sefer = Trip.objects.get(id=sefer_id)
    
    if request.method == 'POST':
        if 'secilen_koltuk' in request.POST:
            koltuk_no = request.POST.get('secilen_koltuk')
            cinsiyet = request.POST.get('secilen_cinsiyet')
            
            context = {
                'sefer': sefer,
                'koltuk_no': koltuk_no,
                'cinsiyet': cinsiyet
            }
            return render(request, 'odeme.html', context)
        
        else:
            koltuk_no = request.POST.get('koltuk_no') 
            cinsiyet = request.POST.get('cinsiyet')
            yolcu_isim = request.POST.get('yolcu_isim')
            tc_no = request.POST.get('tc_no')
            payment_method = request.POST.get('payment_method')
          
            if Ticket.objects.filter(trip=sefer, seat_number=koltuk_no, status='aktif').exists():
                context = {
                    'sefer': sefer,
                    'koltuk_no': koltuk_no,
                    'cinsiyet': cinsiyet,
                    'hata': "Bu koltuk başkası tarafından satın alındı. Lütfen farklı bir koltuk seçiniz."
                }
                return render(request, 'odeme.html', context)
            
            bilet_sahibi = request.user if request.user.is_authenticated else None

            yeni_bilet = Ticket.objects.create(
                user=bilet_sahibi, 
                trip=sefer,
                seat_number=koltuk_no,
                passenger_gender=cinsiyet,
                passenger_name=yolcu_isim,
                tc_no=tc_no,
                payment_method=payment_method,
                status='aktif'
            )
            return redirect(f'/basarili/?sefer={sefer.id}&koltuk={koltuk_no}&bilet={yeni_bilet.id}')
    return redirect('home')

# @login_required(login_url='/login/')
def basarili_view(request):
    sefer_id = request.GET.get('sefer')
    koltuk_no = request.GET.get('koltuk')
    bilet_id = request.GET.get('bilet')
    sefer = Trip.objects.get(id=sefer_id)
    
    context = {
        'sefer': sefer,
        'koltuk_no': koltuk_no,
        'bilet_id': bilet_id
    }
    return render(request, 'basarili.html', context)

def bilet_pdf_indir_view(request, bilet_id):
    # Bileti veritabanından buluyoruz
    bilet = Ticket.objects.get(id=bilet_id)

    template = get_template('bilet_pdf_sablonu.html')
    context = {'bilet': bilet}
    html = template.render(context)
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        # Dosya adını dinamik olacak
        filename = f"bilet_{bilet.trip.departure_city}_{bilet.trip.arrival_city}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse("PDF oluşturulurken hata oluştu.", status=400)

def bilet_yazdir_view(request, bilet_id):
    bilet = Ticket.objects.get(id=bilet_id)

    context = {
        'bilet': bilet
    }
    return render(request, 'bilet_yazdir.html', context)

def register_view(request):
    hata = None
    if request.method == 'POST':
        kullanici_adi = request.POST.get('username')
        eposta = request.POST.get('email')
        sifre = request.POST.get('password')
        sifre_tekrar = request.POST.get('password_confirm')

        if sifre != sifre_tekrar:
            hata = "Şifre eşleşmiyor!"
        elif User.objects.filter(username=kullanici_adi).exists():
            hata = "Bu kullanıcı adı zaten mevcut!"
        elif User.objects.filter(email=eposta).exists():
            hata = "Bu e-posta adresi zaten kayıtlı!"
        else:
            yeni_kullanici = User.objects.create_user(
                username=kullanici_adi, 
                email=eposta, 
                password=sifre
            )
            login(request, yeni_kullanici)
            return redirect('home')
    return render(request, 'register.html', {'hata': hata})

def login_view(request):
    hata = None
    if request.method == 'POST':
        kullanici_adi = request.POST.get('username')
        sifre = request.POST.get('password')
    
        user = authenticate(request, username=kullanici_adi, password=sifre)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            hata = "Kullanıcı adı veya şifre hatalı!"
            
    return render(request, 'login.html', {'hata': hata})

def logout_view(request):
    logout(request)
    return redirect('home')