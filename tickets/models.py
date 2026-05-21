from django.db import models
from django.contrib.auth.models import User # Sisteme kayıtlı yolcular için Django'nun hazır kullanıcı modeli

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Şehir Adı")

    class Meta:
        verbose_name = "Şehir"
        verbose_name_plural = "Şehirler"

    def __str__(self):
        return self.name

class Bus(models.Model):
    # Otobüs tipi için seçenekler (Dropdown menü olacak)
    BUS_TYPES = (
        ('2+1', '2+1 VIP'),
        ('2+2', '2+2 Standart'),
    )
    
    plate_number = models.CharField(max_length=20, unique=True, verbose_name="Plaka Numarası")
    bus_type = models.CharField(max_length=10, choices=BUS_TYPES, default='2+2', verbose_name="Otobüs Tipi")
    capacity = models.PositiveIntegerField(default=40, verbose_name="Kapasite (Koltuk Sayısı)")

    class Meta:
        verbose_name = "Otobüs"
        verbose_name_plural = "Otobüsler"

    def __str__(self):
        return f"{self.plate_number} ({self.bus_type})"

class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name="Otobüs")
    departure_city = models.ForeignKey(City, related_name='departures', on_delete=models.CASCADE, verbose_name="Kalkış Şehri")
    arrival_city = models.ForeignKey(City, related_name='arrivals', on_delete=models.CASCADE, verbose_name="Varış Şehri")
    departure_time = models.DateTimeField(verbose_name="Kalkış Zamanı")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Bilet Fiyatı (TL)")
    
    class Meta:
        verbose_name = "Sefer"
        verbose_name_plural = "Seferler"

    def __str__(self):
        return f"{self.departure_city} -> {self.arrival_city} | {self.departure_time.strftime('%d.%m.%Y %H:%M')}"

class Ticket(models.Model):
    # Biletin durumu
    STATUS_CHOICES = (
        ('aktif', 'Aktif'),
        ('iptal', 'İptal Edildi'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Satın Alan Üye")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Sefer")
    seat_number = models.PositiveIntegerField(verbose_name="Koltuk Numarası")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Satın Alma Tarihi")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aktif', verbose_name="Durum")

    GENDER_CHOICES = (
        ('E', 'Erkek'),
        ('K', 'Kadın'),
    )
    passenger_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Yolcu Cinsiyeti", default='E')
    passenger_name = models.CharField(max_length=100, verbose_name="Yolcu Adı Soyadı", null=True)
    tc_no = models.CharField(max_length=11, verbose_name="TC Kimlik No", null=True)

    PAYMENT_METHODS = (
        ('kart', 'Kredi / Banka Kartı'),
        ('nakit', 'Nakit (Terminalde Ödeme)'),
    )
    payment_method = models.CharField(
        max_length=10, 
        choices=PAYMENT_METHODS, 
        default='kart', 
        verbose_name="Ödeme Yöntemi"
    )

    class Meta:
        verbose_name = "Bilet"
        verbose_name_plural = "Biletler"
        # Aynı seferde, aynı koltuğun 2 kez satılmasını veritabanı seviyesinde engelleme
        unique_together = ['trip', 'seat_number'] 

    def __str__(self):
        isim = self.passenger_name if self.passenger_name else self.user.username
        return f"{isim} - {self.trip} - Koltuk: {self.seat_number}"